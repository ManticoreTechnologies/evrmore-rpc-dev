"""
ZMQ client for receiving Evrmore blockchain notifications in real-time.

This module provides a high-level, asynchronous interface to the Evrmore ZMQ notifications.
The Evrmore node can publish notifications about various blockchain events through ZMQ,
and this client allows subscribing to those events and handling them in real-time.

Features:
- Asynchronous API with asyncio integration
- Event-based handling with decorator-based registration
- Support for all standard Evrmore ZMQ notification topics
- Automatic reconnection on connection loss
- Clean shutdown and resource management
- Typed notification data with structured fields
- Seamless API that works in both sync and async contexts
- Auto-decoding of block and transaction data using enhanced topics

Available notification topics:
- HASH_BLOCK: New block hash (lightweight notification of new blocks)
- HASH_TX: New transaction hash (lightweight notification of new transactions)
- RAW_BLOCK: Complete serialized block data
- RAW_TX: Complete serialized transaction data
- BLOCK: Automatically decoded complete block data (enhanced topic)
- TX: Automatically decoded complete transaction data (enhanced topic)

Enhanced topics (BLOCK, TX) require an RPC client to be provided when creating
the ZMQ client, or auto_create_rpc=True to automatically create one.

Example with auto-decoding:

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Create RPC client for decoding
rpc = EvrmoreClient()

# Create ZMQ client with RPC client for auto-decoding
zmq = EvrmoreZMQClient(rpc_client=rpc)

# Register handler for automatically decoded blocks
@zmq.on(ZMQTopic.BLOCK)
def on_block(notification):
    print(f"New block at height {notification.height}")
    print(f"Has {len(notification.block['tx'])} transactions")

# Register handler for automatically decoded transactions
@zmq.on(ZMQTopic.TX)
def on_tx(notification):
    print(f"New transaction: {notification.tx['txid']}")
    print(f"With {len(notification.tx['vin'])} inputs and {len(notification.tx['vout'])} outputs")

# Start the ZMQ client
zmq.start()
```

Usage requires ZMQ to be enabled in the Evrmore node configuration (evrmore.conf):
    zmqpubhashtx=tcp://127.0.0.1:28332
    zmqpubhashblock=tcp://127.0.0.1:28332
    zmqpubrawtx=tcp://127.0.0.1:28332
    zmqpubrawblock=tcp://127.0.0.1:28332

Using with RPC client:
When using the ZMQ client alongside the EvrmoreClient for RPC calls, follow these best practices:

1. Both the ZMQ client and RPC client use a seamless API that works in both contexts:
   ```
   # Works in both sync and async contexts
   from evrmore_rpc import EvrmoreClient
   from evrmore_rpc.zmq import EvrmoreZMQClient
   
   # Create clients
   rpc_client = EvrmoreClient()
   zmq_client = EvrmoreZMQClient()
   
   # Start ZMQ client (will auto-detect context)
   zmq_client.start()
   
   # In async contexts:
   await zmq_client.start()
   ```

2. Always await all RPC calls inside ZMQ handlers:
   ```
   @zmq_client.on(ZMQTopic.HASH_BLOCK)
   async def handle_block(notification):
       block_data = await rpc_client.getblock(notification.hex)  # Note the await
   ```

3. Always properly close both clients when shutting down:
   ```
   # In async contexts:
   await zmq_client.stop()
   await rpc_client.close()
   
   # In sync contexts:
   zmq_client.stop()
   rpc_client.close_sync()
   ```

4. Handle exceptions in your notification handlers to prevent crashes:
   ```
   @zmq_client.on(ZMQTopic.HASH_BLOCK)
   async def handle_block(notification):
       try:
           block_data = await rpc_client.getblock(notification.hex)
       except Exception as e:
           print(f"Error handling block: {e}")
   ```

Dependencies:
- pyzmq: Python bindings for ZeroMQ
"""

import asyncio
import binascii
import enum
import logging
import signal
import threading
import time
import sys
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Union, Awaitable

import zmq
import zmq.asyncio

from evrmore_rpc.utils import is_async_context
from evrmore_rpc.zmq.models import ZMQNotification, ZMQDecodedBlockNotification, ZMQDecodedTxNotification

# Set up logging
logger = logging.getLogger("evrmore_rpc.zmq")


class ZMQTopic(enum.Enum):
    """
    ZMQ notification topics published by Evrmore nodes.
    
    See https://github.com/EVR-git/EVR/blob/master/doc/zmq.md for more information.
    
    Standard topics from Evrmore node:
    - HASH_BLOCK: Block hash only
    - HASH_TX: Transaction hash only
    - RAW_BLOCK: Raw serialized block data
    - RAW_TX: Raw serialized transaction data
    
    Enhanced topics (evrmore-rpc extensions):
    - BLOCK: Automatically decoded block data using RPC
    - TX: Automatically decoded transaction data using RPC
    """
    # Standard Evrmore ZMQ topics
    HASH_BLOCK = b"hashblock"
    HASH_TX = b"hashtx"
    RAW_BLOCK = b"rawblock"
    RAW_TX = b"rawtx"
    
    # Enhanced topics with automatic decoding
    BLOCK = b"block"  # Special topic that automatically decodes blocks
    TX = b"tx"        # Special topic that automatically decodes transactions

    # Messaging topics
    MESSAGE = b"message"


class EvrmoreZMQClient:
    """
    Client for receiving ZMQ notifications from an Evrmore node.
    
    This class provides a simple interface for subscribing to ZMQ notifications
    from an Evrmore node. It works in both synchronous and asynchronous contexts.
    
    In synchronous mode, it creates a background thread for handling messages.
    In asynchronous mode, it creates a background task for handling messages.
    
    The client supports both standard ZMQ topics from the Evrmore node and
    enhanced topics that provide automatic decoding of data:
    
    Standard topics:
    - HASH_BLOCK: Provides just the block hash
    - HASH_TX: Provides just the transaction hash
    - RAW_BLOCK: Provides the raw serialized block data
    - RAW_TX: Provides the raw serialized transaction data
    
    Enhanced topics:
    - BLOCK: Automatically fetches and decodes the full block data
    - TX: Automatically fetches and decodes the full transaction data
    
    For enhanced topics, the client needs an RPC connection to fetch the data.
    """
    
    def __init__(self, 
                 zmq_host: str = "127.0.0.1", 
                 zmq_port: int = 28332, 
                 topics: Optional[List[ZMQTopic]] = None,
                 rpc_client: Any = None,
                 auto_decode: bool = True,
                 auto_create_rpc: bool = True) -> None:
        """
        Initialize the ZMQ client.
        
        Args:
            zmq_host: The host of the ZMQ endpoint (default: 127.0.0.1)
            zmq_port: The port of the ZMQ endpoint (default: 28332)
            topics: The topics to subscribe to (default: all topics)
            rpc_client: Optional RPC client for auto-decoding data (default: None)
            auto_decode: Whether to automatically decode data for enhanced topics (default: True)
            auto_create_rpc: Whether to automatically create an RPC client if none provided (default: True)
        """
        self.zmq_host = zmq_host
        self.zmq_port = zmq_port
        self.topics = topics or list(ZMQTopic)
        self.auto_decode = auto_decode
        
        # Handle RPC client for auto-decoding
        self.rpc_client = rpc_client
        
        # Check if we have enhanced topics but no RPC client
        needs_rpc = any(topic in [ZMQTopic.BLOCK, ZMQTopic.TX] for topic in self.topics)
        
        # Auto-create RPC client if needed and allowed
        if needs_rpc and not rpc_client and auto_decode and auto_create_rpc:
            try:
                # Try to import and create an RPC client
                from evrmore_rpc import EvrmoreClient
                self.rpc_client = EvrmoreClient()
                logger.info("Auto-created RPC client for decoding")
            except Exception as e:
                logger.warning(f"Failed to auto-create RPC client: {e}")
        
        if needs_rpc and not self.rpc_client and auto_decode:
            logger.warning("Enhanced ZMQ topics (BLOCK, TX) require an RPC client for decoding. "
                           "Auto-decoding is enabled but no RPC client was provided.")
        
        # Create the ZMQ context
        self.context = zmq.asyncio.Context()
        self.socket = None
        
        # For handlers
        self.handlers: Dict[bytes, List[Callable]] = {}
        
        # For state management
        self._running = False
        self._task = None
        self._thread = None
        self._async_mode = None  # None = auto-detect, True = force async, False = force sync
        
        # For synchronous use
        self._sync_context = None
        self._sync_socket = None
        
        # For cleanup management
        self._linger = 0  # Default to 0 for fast exit
        self._thread_join_timeout = 0.1  # Default timeout for joining threads
        self._task_cancel_timeout = 0.1  # Default timeout for canceling tasks
        
        # Initialize handlers for all topics
        for topic in ZMQTopic:
            self.handlers[topic.value] = []
            
        # Map enhanced topics to base topics for internal subscription
        self._enhanced_topic_map = {
            ZMQTopic.BLOCK.value: ZMQTopic.HASH_BLOCK.value,
            ZMQTopic.TX.value: ZMQTopic.HASH_TX.value
        }
        
        # Internal subscription tracking for enhanced topics
        self._internal_subscriptions = set()
        
        # Register all enhanced topics with their base topics
        for enhanced_topic, base_topic in self._enhanced_topic_map.items():
            if enhanced_topic in [t.value for t in self.topics]:
                self._internal_subscriptions.add(base_topic)
        
        # Auto-detect context
        self._async_mode = None
    
    def set_lingering(self, value: int) -> None:
        """
        Set the socket linger value in milliseconds.
        
        The linger value determines how long the socket will try to deliver
        pending messages when closed. Setting to 0 means no lingering and
        enables fast shutdown.
        
        Args:
            value: The linger value in milliseconds (0 for no lingering)
        """
        self._linger = value
        logger.debug(f"ZMQ socket linger set to {value} ms")

    def set_cleanup_timeouts(self, thread_timeout: float = 0.1, task_timeout: float = 0.1) -> None:
        """
        Set timeouts for cleanup operations.
        
        This controls how long the client will wait for threads and tasks to complete
        during shutdown. Lower values mean faster shutdown but may leave some
        resources uncleaned. Higher values are more thorough but slower.
        
        Args:
            thread_timeout: Timeout in seconds to wait for threads to join (default: 0.1)
            task_timeout: Timeout in seconds to wait for tasks to cancel (default: 0.1)
        """
        self._thread_join_timeout = thread_timeout
        self._task_cancel_timeout = task_timeout
        logger.debug(f"ZMQ cleanup timeouts set: thread={thread_timeout}s, task={task_timeout}s")
    
    def on(self, topic: ZMQTopic) -> Callable:
        """
        Decorator for registering a handler for a ZMQ topic.
        
        Args:
            topic: The ZMQ topic to handle.
            
        Returns:
            A decorator function that takes a handler function and registers it.
        """
        def decorator(handler: Callable) -> Callable:
            if topic.value not in self.handlers:
                self.handlers[topic.value] = []
            self.handlers[topic.value].append(handler)
            return handler
        return decorator
    
    def start(self) -> Union[None, Awaitable[None]]:
        """
        Start the ZMQ client. Works in both synchronous and asynchronous contexts.
        
        In synchronous context, starts a background thread for handling messages.
        In asynchronous context, starts an asyncio task for handling messages.
        
        Returns:
            None in synchronous context, Awaitable in asynchronous context.
        """
        from evrmore_rpc.utils import AwaitableResult, is_async_context
        
        # If _async_mode is explicitly set, use that
        if self._async_mode is not None:
            if self._async_mode:
                return self.start_async()
            else:
                return self.start_sync()
                
        # If not explicitly set, detect context
        if is_async_context():
            # In async context, return the coroutine directly
            return self.start_async()
        else:
            # In sync context, start synchronously
            sync_result = self.start_sync()
            # Create a coroutine for the async method
            async_coro = self.start_async()
            # Return an AwaitableResult that works in both contexts
            return AwaitableResult(
                sync_result, 
                async_coro,
                cleanup_func=None  # No cleanup needed here
            )
    
    def start_sync(self) -> None:
        """
        Start the ZMQ client synchronously.
        
        This method creates a standard ZMQ socket and starts a background thread
        to receive and process ZMQ messages.
        """
        if self._running:
            logger.warning("ZMQ client is already running.")
            return
        
        # Create ZMQ context and socket
        self._sync_context = zmq.Context()
        self._sync_socket = self._sync_context.socket(zmq.SUB)
        
        # Set socket options
        self._sync_socket.setsockopt(zmq.LINGER, self._linger)
        self._sync_socket.setsockopt(zmq.RCVTIMEO, 1000)  # 1 second timeout
        
        # Connect to the ZMQ endpoint
        endpoint = f"tcp://{self.zmq_host}:{self.zmq_port}"
        try:
            self._sync_socket.connect(endpoint)
            logger.info(f"Connected to ZMQ endpoint: {endpoint}")
        except zmq.error.ZMQError as e:
            logger.error(f"Failed to connect to ZMQ endpoint {endpoint}: {e}")
            self._sync_socket.close()
            self._sync_context.term()
            self._sync_socket = None
            self._sync_context = None
            raise
        
        # Subscribe to topics
        for topic in self.topics:
            try:
                self._sync_socket.setsockopt(zmq.SUBSCRIBE, topic.value)
                logger.debug(f"Subscribed to topic: {topic.name}")
            except Exception as e:
                logger.error(f"Failed to subscribe to topic {topic.name}: {e}")
                raise
        
        # Subscribe to internal topics needed for enhanced topics
        for internal_topic in self._internal_subscriptions:
            if internal_topic not in [t.value for t in self.topics]:
                try:
                    self._sync_socket.setsockopt(zmq.SUBSCRIBE, internal_topic)
                    logger.debug(f"Subscribed to internal topic: {internal_topic}")
                except Exception as e:
                    logger.error(f"Failed to subscribe to internal topic {internal_topic}: {e}")
        
        # Start the message loop in a background thread
        self._running = True
        self._thread = threading.Thread(target=self._receive_loop_sync, daemon=True)
        self._thread.start()
        logger.info("ZMQ client started in synchronous mode.")
    
    async def start_async(self) -> None:
        """
        Start the ZMQ client asynchronously.
        
        This method creates a ZMQ socket, subscribes to the specified topics,
        and starts a background task to receive notifications.
        """
        if self._running:
            logger.warning("ZMQ client already running")
            return
        
        self._async_mode = True
        
        # Create async ZMQ context if needed
        if not self.context:
            self.context = zmq.asyncio.Context.instance()
        
        # Create socket
        self.socket = self.context.socket(zmq.SUB)
        
        # Set socket options
        self.socket.setsockopt(zmq.LINGER, self._linger)
        
        # Connect to ZMQ endpoint
        endpoint = f"tcp://{self.zmq_host}:{self.zmq_port}"
        logger.debug(f"Connecting to ZMQ endpoint: {endpoint}")
        self.socket.connect(endpoint)
        
        # Subscribe to topics
        for topic in self.topics:
            try:
                self.socket.setsockopt(zmq.SUBSCRIBE, topic.value)
                logger.debug(f"Subscribed to topic: {topic.name}")
            except Exception as e:
                logger.error(f"Failed to subscribe to topic {topic.name}: {e}")
                raise
    
    def stop(self, force: bool = False) -> Union[None, Awaitable[None]]:
        """
        Stop the ZMQ client. Works in both synchronous and asynchronous contexts.
        
        In synchronous context, stops the background thread and cleans up resources.
        In asynchronous context, stops the asyncio task and cleans up resources.
        
        Args:
            force: If True, exits the program immediately without cleanup (default: False)
            
        Returns:
            None in synchronous context, Awaitable in asynchronous context.
        """
        # Check if we should force exit immediately
        if force:
            print("Force stopping ZMQ client - exiting program immediately...")
            import sys
            
            # Try to close sockets quickly
            try:
                if self._sync_socket:
                    self._sync_socket.close(linger=0)
                if self.socket:
                    self.socket.close(linger=0)
            except Exception:
                pass
            
            # Exit immediately
            sys.exit(0)

        from evrmore_rpc.utils import AwaitableResult, is_async_context
            
        # If _async_mode is explicitly set, use that
        if self._async_mode is not None:
            if self._async_mode:
                return self.stop_async()
            else:
                return self.stop_sync()
                
        # If not explicitly set, detect context
        if is_async_context():
            # In async context, return the coroutine directly
            return self.stop_async()
        else:
            # In sync context, stop synchronously
            sync_result = self.stop_sync()
            # Create a coroutine for the async method
            async_coro = self.stop_async()
            # Return an AwaitableResult that works in both contexts
            return AwaitableResult(
                sync_result, 
                async_coro,
                cleanup_func=None  # No cleanup needed here
            )
    
    def stop_sync(self) -> None:
        """
        Stop the ZMQ client synchronously.
        
        This method stops the background thread, closes the socket, and cleans up resources.
        """
        if not self._running:
            logger.warning("ZMQ client not running")
            return
        
        # Indicate that we're stopping
        self._running = False
        
        # Stop the background thread if it's running
        if self._thread and self._thread.is_alive():
            logger.debug("Waiting for background thread to finish...")
            try:
                self._thread.join(timeout=self._thread_join_timeout)
            except Exception as e:
                logger.error(f"Error joining background thread: {e}")
            self._thread = None
        
        # Close socket immediately
        if self.socket:
            try:
                self.socket.close(linger=0)
            except Exception as e:
                logger.error(f"Error closing ZMQ socket: {e}")
            self.socket = None
        
        # Terminate context - cannot set linger on context
        if self.context:
            try:
                self.context.term()
            except Exception as e:
                logger.error(f"Error terminating ZMQ context: {e}")
            self.context = None
    
    async def stop_async(self) -> None:
        """
        Stop the ZMQ client asynchronously.
        
        This method cancels the background task and closes the ZMQ socket.
        """
        if not self._running:
            return
            
        # Cancel background task
        self._running = False
        if self._task:
            try:
                self._task.cancel()
                # Use shorter timeout for faster shutdown
                await asyncio.wait([self._task], timeout=self._task_cancel_timeout)
            except (asyncio.CancelledError, Exception) as e:
                if not isinstance(e, asyncio.CancelledError):
                    logger.error(f"Error cancelling task: {e}")
            
        # Close socket immediately
        if self.socket:
            try:
                self.socket.close(linger=0)
            except Exception as e:
                logger.error(f"Error closing ZMQ socket: {e}")
            
        # Terminate context - cannot set linger on context
        if self.context:
            try:
                self.context.term()
            except Exception as e:
                logger.error(f"Error terminating ZMQ context: {e}")
    
    def _receive_loop_sync(self) -> None:
        """
        Background thread for receiving ZMQ notifications synchronously.
        
        This method continuously receives notifications from the ZMQ socket
        and dispatches them to the appropriate handlers.
        """
        while self._running:
            try:
                # Receive message with timeout
                msg = self._sync_socket.recv_multipart()
                
                # Parse message
                topic, body, sequence = msg
                sequence = int.from_bytes(sequence, byteorder="little")
                hex_data = binascii.hexlify(body).decode("utf-8")
                
                # Create notification
                notification = ZMQNotification(
                    topic=topic.decode("utf-8"),
                    body=body,
                    sequence=sequence,
                    hex=hex_data,
                )
                
                # Handle standard topics directly
                if topic in self.handlers:
                    self._dispatch_to_handlers_sync(topic, notification)
                
                # Check for enhanced topics that need decoding
                if self.auto_decode:
                    # Handle BLOCK topic (needs hash_block notifications)
                    if ZMQTopic.BLOCK.value in self.handlers and topic == ZMQTopic.HASH_BLOCK.value:
                        # Decode block and dispatch to handlers
                        decoded_notification = self._decode_block_sync(hex_data)
                        self._dispatch_to_handlers_sync(ZMQTopic.BLOCK.value, decoded_notification)
                    
                    # Handle TX topic (needs hash_tx notifications)
                    if ZMQTopic.TX.value in self.handlers and topic == ZMQTopic.HASH_TX.value:
                        # Decode transaction and dispatch to handlers
                        decoded_notification = self._decode_transaction_sync(hex_data)
                        self._dispatch_to_handlers_sync(ZMQTopic.TX.value, decoded_notification)
                
            except zmq.error.Again:
                # Timeout, just continue
                pass
            except Exception as e:
                if self._running:  # Only log if still running
                    logger.error(f"Error receiving ZMQ message: {e}")
                    # Short delay before retrying
                    time.sleep(1)

    def _dispatch_to_handlers_sync(self, topic: bytes, notification: Union[ZMQNotification, ZMQDecodedBlockNotification, ZMQDecodedTxNotification]) -> None:
        """
        Dispatch a notification to all registered handlers synchronously.
        
        Args:
            topic: The topic to dispatch to
            notification: The notification to dispatch
        """
        for handler in self.handlers[topic]:
            try:
                # Check if handler is async or sync
                if asyncio.iscoroutinefunction(handler):
                    # For async handlers, we need a running event loop
                    # Create a new event loop for this handler
                    loop = asyncio.new_event_loop()
                    try:
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(handler(notification))
                    finally:
                        loop.close()
                else:
                    # For sync handlers, just call directly
                    handler(notification)
            except Exception as e:
                logger.error(f"Error in handler: {e}")
    
    async def _receive_loop_async(self) -> None:
        """
        Background task for receiving ZMQ notifications asynchronously.
        
        This method continuously receives notifications from the ZMQ socket
        and dispatches them to the appropriate handlers.
        """
        logger.debug("Starting async receive loop")
        
        # Set running flag
        self._running = True
        
        # Process messages until stop is called
        while self._running:
            try:
                # Receive message with timeout
                multipart = await asyncio.wait_for(
                    self.socket.recv_multipart(),
                    timeout=1.0
                )
                
                # Decode the message
                topic, data, sequence = multipart
                sequence_num = int.from_bytes(sequence, byteorder='little')
                
                # Create notification
                notification = ZMQNotification(
                    topic=topic.decode('ascii'),
                    body=data,
                    sequence=sequence_num,
                    hex=data.hex()
                )
                
                # Dispatch notification to handlers
                await self._dispatch_to_handlers_async(topic, notification)
            except asyncio.TimeoutError:
                # This is expected, just continue
                continue
            except asyncio.CancelledError:
                # Task was cancelled, exit the loop
                logger.debug("Async receive loop cancelled")
                break
            except Exception as e:
                if self._running:  # Only log if still running
                    logger.error(f"Error receiving ZMQ message: {e}")
    
    async def _dispatch_to_handlers_async(self, topic: bytes, notification: Union[ZMQNotification, ZMQDecodedBlockNotification, ZMQDecodedTxNotification]) -> None:
        """
        Dispatch a notification to all registered handlers asynchronously.
        
        Args:
            topic: The topic to dispatch to
            notification: The notification to dispatch
        """
        for handler in self.handlers[topic]:
            try:
                # Check if handler is async or sync
                if asyncio.iscoroutinefunction(handler):
                    # For async handlers, await them
                    await handler(notification)
                else:
                    # For sync handlers, run in executor
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, handler, notification)
            except Exception as e:
                logger.error(f"Error in handler: {e}")
    
    def force_sync(self) -> None:
        """
        Force the client to use synchronous mode.
        
        This method sets the client to always use synchronous operations,
        regardless of the execution context.
        """
        self._async_mode = False
    
    def force_async(self) -> None:
        """
        Force the client to use asynchronous mode.
        
        This method sets the client to always use asynchronous operations,
        regardless of the execution context.
        """
        self._async_mode = True
    
    def reset(self) -> None:
        """
        Reset the client's mode to auto-detect.
        
        This method resets the client to automatically detect the execution
        context and use the appropriate operations.
        """
        self._async_mode = None
    
    def force_exit(self, exit_code: int = 0) -> None:
        """
        Force an immediate program exit without waiting for cleanup.
        
        This method is useful when you need to shut down immediately without
        waiting for ZMQ to clean up its resources, which can be slow even with
        linger set to 0.
        
        WARNING: This method calls sys.exit() which will terminate the entire program
        immediately. Any pending operations will be abandoned. Use only when
        quick shutdown is more important than clean shutdown.
        
        Args:
            exit_code: The exit code to use when terminating the program (default: 0)
        """
        logger.info(f"Force exiting with code {exit_code}")
        
        # Try to close sockets quickly without lingering
        try:
            if self._sync_socket:
                self._sync_socket.close(linger=0)
            if self.socket:
                self.socket.close(linger=0)
        except Exception as e:
            logger.debug(f"Error during forced socket close: {e}")
        
        # Exit immediately
        sys.exit(exit_code)
    
    async def _decode_block_async(self, block_hash: str) -> ZMQDecodedBlockNotification:
        """
        Decode a block using the RPC client asynchronously.
        
        Args:
            block_hash: The hash of the block to decode
            
        Returns:
            ZMQDecodedBlockNotification with the decoded block data
        """
        if not self.rpc_client:
            return ZMQDecodedBlockNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash,
                is_valid=False,
                error="No RPC client available for decoding. Use rpc_client parameter when creating ZMQ client."
            )
        
        try:
            # Create a base notification first
            notification = ZMQNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash
            )
            
            # Ensure the RPC client is in async mode
            if hasattr(self.rpc_client, 'force_async'):
                self.rpc_client.force_async()
            
            # Fetch block with full transaction data (verbosity=2)
            try:
                block_data = await self.rpc_client.getblock(block_hash, 2)
            except Exception as e:
                # Try with lower verbosity if full transactions fail
                try:
                    block_data = await self.rpc_client.getblock(block_hash, 1)
                except Exception as inner_e:
                    # Both attempts failed
                    logger.error(f"Failed to get block data for {block_hash}: {inner_e}")
                    return ZMQDecodedBlockNotification(
                        topic="block",
                        body=bytes.fromhex(block_hash),
                        sequence=0,
                        hex=block_hash,
                        is_valid=False,
                        error=f"RPC error: {str(e)}. Check if Evrmore node is running and accessible."
                    )
            
            # Get the block height - handle both dict and object responses
            height = None
            if isinstance(block_data, dict):
                height = block_data.get('height')
            else:
                # It might be a Pydantic model or other object
                height = getattr(block_data, 'height', None)
            
            # Create enhanced notification
            return ZMQDecodedBlockNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash,
                block=block_data,
                height=height,
                is_valid=True
            )
        except Exception as e:
            logger.error(f"Error decoding block {block_hash}: {e}")
            return ZMQDecodedBlockNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash,
                is_valid=False,
                error=f"Decoding error: {str(e)}"
            )
    
    def _decode_block_sync(self, block_hash: str) -> ZMQDecodedBlockNotification:
        """
        Decode a block using the RPC client synchronously.
        
        Args:
            block_hash: The hash of the block to decode
            
        Returns:
            ZMQDecodedBlockNotification with the decoded block data
        """
        if not self.rpc_client:
            return ZMQDecodedBlockNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash,
                is_valid=False,
                error="No RPC client available for decoding. Use rpc_client parameter when creating ZMQ client."
            )
        
        try:
            # Create a base notification first
            notification = ZMQNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash
            )
            
            # Ensure the RPC client is in sync mode
            if hasattr(self.rpc_client, 'force_sync'):
                self.rpc_client.force_sync()
            
            # Fetch block with full transaction data (verbosity=2)
            try:
                block_data = self.rpc_client.getblock(block_hash, 2)
            except Exception as e:
                # Try with lower verbosity if full transactions fail
                try:
                    block_data = self.rpc_client.getblock(block_hash, 1)
                except Exception as inner_e:
                    # Both attempts failed
                    logger.error(f"Failed to get block data for {block_hash}: {inner_e}")
                    return ZMQDecodedBlockNotification(
                        topic="block",
                        body=bytes.fromhex(block_hash),
                        sequence=0,
                        hex=block_hash,
                        is_valid=False,
                        error=f"RPC error: {str(e)}. Check if Evrmore node is running and accessible."
                    )
            
            # Get the block height - handle both dict and object responses
            height = None
            if isinstance(block_data, dict):
                height = block_data.get('height')
            else:
                # It might be a Pydantic model or other object
                height = getattr(block_data, 'height', None)
            
            # Create enhanced notification
            return ZMQDecodedBlockNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash,
                block=block_data,
                height=height,
                is_valid=True
            )
        except Exception as e:
            logger.error(f"Error decoding block {block_hash}: {e}")
            return ZMQDecodedBlockNotification(
                topic="block",
                body=bytes.fromhex(block_hash),
                sequence=0,
                hex=block_hash,
                is_valid=False,
                error=f"Decoding error: {str(e)}"
            )
    
    async def _decode_transaction_async(self, tx_hash: str) -> ZMQDecodedTxNotification:
        """
        Decode a transaction using the RPC client asynchronously.
        
        This method fetches and decodes transaction data, with special handling for asset transactions.
        It detects asset transfers, creations, reissuances and other asset operations.
        
        Args:
            tx_hash: The hash of the transaction to decode
            
        Returns:
            ZMQDecodedTxNotification with the decoded transaction data and asset information
        """
        if not self.rpc_client:
            return ZMQDecodedTxNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash,
                is_valid=False,
                error="No RPC client available for decoding. Use rpc_client parameter when creating ZMQ client."
            )
        
        try:
            # Create a base notification first
            notification = ZMQNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash
            )
            
            # Ensure the RPC client is in async mode
            if hasattr(self.rpc_client, 'force_async'):
                self.rpc_client.force_async()
            
            # Fetch transaction with full details
            try:
                tx_data = await self.rpc_client.getrawtransaction(tx_hash, True)
            except Exception as e:
                logger.error(f"Failed to get transaction data for {tx_hash}: {e}")
                return ZMQDecodedTxNotification(
                    topic="tx",
                    body=bytes.fromhex(tx_hash),
                    sequence=0,
                    hex=tx_hash,
                    is_valid=False,
                    error=f"RPC error: {str(e)}. Check if Evrmore node is running and accessible."
                )
            
            # Create enhanced notification
            result = ZMQDecodedTxNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash,
                tx=tx_data,
                is_valid=True
            )
            
            # If the transaction has assets, enhance asset data
            if result.has_assets and len(result.asset_info) > 0:
                try:
                    # Enhance asset data with additional information
                    await self._enhance_asset_info_async(result)
                except Exception as e:
                    logger.error(f"Error enhancing asset info for tx {tx_hash}: {e}")
            
            return result
        except Exception as e:
            logger.error(f"Error decoding transaction {tx_hash}: {e}")
            return ZMQDecodedTxNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash,
                is_valid=False,
                error=f"Decoding error: {str(e)}"
            )
                        

    async def _enhance_asset_info_async(self, notification: ZMQDecodedTxNotification) -> None:
        """
        Enhance asset information in a transaction notification.
        
        This method adds additional information to asset data, such as:
        - Full asset details from getassetdata
        - Current unspent outputs for the asset
        - Historical data about the asset
        
        Args:
            notification: The transaction notification to enhance
            
        Returns:
            None - The notification is modified in place
        """
        if not self.rpc_client or not notification.has_assets:
            return
            
        # Process each asset in the transaction
        for asset_info in notification.asset_info:
            asset_name = asset_info.get('asset_name')
            if not asset_name:
                continue
                
            try:
                # Get full asset data
                asset_data = await self.rpc_client.getassetdata(asset_name)
                
                # Add asset data to the asset info
                asset_info['asset_details'] = asset_data
                
                # Add additional asset metadata
                if asset_info.get('address'):
                    # Try to get the address's asset balance
                    try:
                        balance = await self.rpc_client.listassetbalancesbyaddress(asset_info['address'])
                        if asset_name in balance:
                            asset_info['address_balance'] = balance[asset_name]
                    except Exception:
                        pass
            except Exception as e:
                logger.debug(f"Error enhancing asset {asset_name}: {e}")
                
    def _enhance_asset_info_sync(self, notification: ZMQDecodedTxNotification) -> None:
        """
        Enhance asset information in a transaction notification synchronously.
        
        This method adds additional information to asset data in synchronous context.
        
        Args:
            notification: The transaction notification to enhance
            
        Returns:
            None - The notification is modified in place
        """
        if not self.rpc_client or not notification.has_assets:
            return
            
        # Process each asset in the transaction
        for asset_info in notification.asset_info:
            asset_name = asset_info.get('asset_name')
            if not asset_name:
                continue
                
            try:
                # Get full asset data
                asset_data = self.rpc_client.getassetdata(asset_name)
                
                # Add asset data to the asset info
                asset_info['asset_details'] = asset_data
                
                # Add additional asset metadata
                if asset_info.get('address'):
                    # Try to get the address's asset balance
                    try:
                        balance = self.rpc_client.listassetbalancesbyaddress(asset_info['address'])
                        if asset_name in balance:
                            asset_info['address_balance'] = balance[asset_name]
                    except Exception:
                        pass
            except Exception as e:
                logger.debug(f"Error enhancing asset {asset_name}: {e}")
    
    def _decode_transaction_sync(self, tx_hash: str) -> ZMQDecodedTxNotification:
        """
        Decode a transaction using the RPC client synchronously.
        
        This method fetches and decodes transaction data, with special handling for asset transactions.
        It detects asset transfers, creations, reissuances and other asset operations.
        
        Args:
            tx_hash: The hash of the transaction to decode
            
        Returns:
            ZMQDecodedTxNotification with the decoded transaction data and asset information
        """
        if not self.rpc_client:
            return ZMQDecodedTxNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash,
                is_valid=False,
                error="No RPC client available for decoding. Use rpc_client parameter when creating ZMQ client."
            )
        
        try:
            # Create a base notification first
            notification = ZMQNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash
            )
            
            # Ensure the RPC client is in sync mode
            if hasattr(self.rpc_client, 'force_sync'):
                self.rpc_client.force_sync()
            
            # Fetch transaction with full details
            try:
                tx_data = self.rpc_client.getrawtransaction(tx_hash, True)
            except Exception as e:
                logger.error(f"Failed to get transaction data for {tx_hash}: {e}")
                return ZMQDecodedTxNotification(
                    topic="tx",
                    body=bytes.fromhex(tx_hash),
                    sequence=0,
                    hex=tx_hash,
                    is_valid=False,
                    error=f"RPC error: {str(e)}. Check if Evrmore node is running and accessible."
                )
            
            # Create enhanced notification
            result = ZMQDecodedTxNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash,
                tx=tx_data,
                is_valid=True
            )
            
            # If the transaction has assets, enhance asset data
            if result.has_assets and len(result.asset_info) > 0:
                try:
                    # Enhance asset data with additional information
                    self._enhance_asset_info_sync(result)
                except Exception as e:
                    logger.error(f"Error enhancing asset info for tx {tx_hash}: {e}")
            
            return result
        except Exception as e:
            logger.error(f"Error decoding transaction {tx_hash}: {e}")
            return ZMQDecodedTxNotification(
                topic="tx",
                body=bytes.fromhex(tx_hash),
                sequence=0,
                hex=tx_hash,
                is_valid=False,
                error=f"Decoding error: {str(e)}"
            )
    
    def __del__(self):
        """Cleanup resources when this object is garbage collected."""
        if self._running:
            try:
                if self._async_mode is True:
                    # We can't await in __del__, so we just cancel the task
                    if self._task and not self._task.done():
                        self._task.cancel()
                else:
                    # Try to clean up sync resources
                    self.stop_sync()
            except Exception as e:
                logger.error(f"Error in __del__: {e}") 