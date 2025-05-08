from typing import Any, Callable, Dict, List, Optional, Union, Awaitable
import threading
import asyncio
from enum import Enum

class ZMQTopic(Enum):
    """ZMQ notification topics published by Evrmore nodes."""
    HASH_BLOCK: bytes
    HASH_TX: bytes
    RAW_BLOCK: bytes
    RAW_TX: bytes

class ZMQNotification:
    """Representation of a ZMQ notification from an Evrmore node."""
    topic: str
    body: bytes
    sequence: int
    hex: str
    timestamp: Any

class EvrmoreZMQClient:
    """Client for receiving ZMQ notifications from an Evrmore node with a seamless API."""
    
    zmq_host: str
    zmq_port: int
    topics: List[ZMQTopic]
    context: Any
    socket: Any
    handlers: Dict[bytes, List[Callable]]
    _running: bool
    _task: Optional[asyncio.Task]
    _thread: Optional[threading.Thread]
    _async_mode: Optional[bool]
    _sync_context: Any
    _sync_socket: Any
    _linger: int
    _thread_join_timeout: float
    _task_cancel_timeout: float
    
    def __init__(self, zmq_host: str = "127.0.0.1", zmq_port: int = 28332, topics: Optional[List[ZMQTopic]] = None) -> None:
        """Initialize the ZMQ client."""
        pass
    
    def set_lingering(self, value: int) -> None:
        """
        Set the socket linger value in milliseconds.
        
        The linger value determines how long the socket will try to deliver
        pending messages when closed. Setting to 0 means no lingering and
        enables fast shutdown.
        
        Args:
            value: The linger value in milliseconds (0 for no lingering)
        """
        pass
    
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
        pass
    
    def on(self, topic: ZMQTopic) -> Callable[[Callable], Callable]:
        """Decorator for registering a handler for a ZMQ topic."""
        pass
    
    def start(self, **kwargs: Any) -> Union[None, Awaitable[None]]:
        """
        Start the ZMQ client. Works in both synchronous and asynchronous contexts.
        
        In synchronous context, starts a background thread to handle ZMQ messages.
        In asynchronous context, starts an asyncio task to handle ZMQ messages.
        
        Returns:
            None in synchronous context, Awaitable in asynchronous context.
        """
        pass
    
    def start_sync(self) -> None:
        """
        Start the ZMQ client synchronously.
        
        This method creates a standard ZMQ socket and starts a background thread
        to receive and process ZMQ messages.
        """
        pass
    
    async def start_async(self) -> None:
        """
        Start the ZMQ client asynchronously.
        
        This method creates a ZMQ socket, subscribes to the specified topics,
        and starts a background task to receive notifications.
        """
        pass
    
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
        pass
    
    def stop_sync(self) -> None:
        """
        Stop the ZMQ client synchronously.
        
        This method stops the background thread, closes the socket, and cleans up resources.
        """
        pass
    
    async def stop_async(self) -> None:
        """
        Stop the ZMQ client asynchronously.
        
        This method cancels the background task and closes the ZMQ socket.
        """
        pass
    
    def _receive_loop_sync(self) -> None:
        """
        Background thread for receiving ZMQ notifications synchronously.
        
        This method continuously receives notifications from the ZMQ socket
        and dispatches them to the appropriate handlers.
        """
        pass
    
    async def _receive_loop_async(self) -> None:
        """
        Background task for receiving ZMQ notifications asynchronously.
        
        This method continuously receives notifications from the ZMQ socket
        and dispatches them to the appropriate handlers.
        """
        pass
    
    def force_sync(self) -> None:
        """
        Force the client to use synchronous mode.
        
        This method sets the client to always use synchronous operations,
        regardless of the execution context.
        """
        pass
    
    def force_async(self) -> None:
        """
        Force the client to use asynchronous mode.
        
        This method sets the client to always use asynchronous operations,
        regardless of the execution context.
        """
        pass
    
    def reset(self) -> None:
        """
        Reset the client's mode to auto-detect.
        
        This method resets the client to automatically detect the execution
        context and use the appropriate operations.
        """
        pass
        
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
        pass 