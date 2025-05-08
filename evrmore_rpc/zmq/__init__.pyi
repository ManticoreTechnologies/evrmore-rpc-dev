from typing import Any, Callable, Coroutine, List, Optional, Union, Awaitable
from evrmore_rpc.zmq.models import ZMQNotification, ZMQDecodedBlockNotification, ZMQDecodedTxNotification
from evrmore_rpc.zmq.client import ZMQTopic

class EvrmoreZMQClient:
    def __init__(self, zmq_host: str = "127.0.0.1", zmq_port: int = 28332, topics: Optional[List[ZMQTopic]] = None, rpc_client: Any = None, auto_decode: bool = True, auto_create_rpc: bool = True) -> None:
        """Initialize the ZMQ client."""
        pass

    def on(self, topic: ZMQTopic) -> Callable:
        """Decorator for registering a handler for a ZMQ topic."""
        pass

    def start(self) -> Union[None, Awaitable[None]]:
        """
        Start the ZMQ client. Works in both synchronous and asynchronous contexts.
        """
        pass
        
    def start_sync(self) -> None:
        """Start the ZMQ client synchronously."""
        pass
        
    async def start_async(self) -> None:
        """Start the ZMQ client asynchronously."""
        pass

    def stop(self, force: bool = False) -> Union[None, Awaitable[None]]:
        """
        Stop the ZMQ client. Works in both synchronous and asynchronous contexts.
        
        Args:
            force: If True, exits the program immediately without cleanup
        """
        pass
        
    def stop_sync(self) -> None:
        """Stop the ZMQ client synchronously."""
        pass
        
    async def stop_async(self) -> None:
        """Stop the ZMQ client asynchronously."""
        pass
        
    def set_lingering(self, value: int) -> None:
        """
        Set the socket linger value in milliseconds.
        
        Args:
            value: The linger value in milliseconds (0 for no lingering)
        """
        pass
        
    def set_cleanup_timeouts(self, thread_timeout: float = 0.1, task_timeout: float = 0.1) -> None:
        """
        Set timeouts for cleanup operations.
        
        Args:
            thread_timeout: Timeout for thread join operations
            task_timeout: Timeout for task cancellation operations
        """
        pass
        
    def force_sync(self) -> None:
        """Force the client to use synchronous mode."""
        pass
        
    def force_async(self) -> None:
        """Force the client to use asynchronous mode."""
        pass
        
    def reset(self) -> None:
        """Reset the client's mode to auto-detect."""
        pass
        
    def force_exit(self, exit_code: int = 0) -> None:
        """Force an immediate program exit."""
        pass

    def _receive_loop(self) -> Coroutine[Any, Any, None]:
        pass
    
    def _parse_message(self, msg: bytes) -> ZMQNotification:
        """Parse a ZMQ message into a ZMQNotification object."""
        pass

class ZMQTopic:
    """ZMQ notification topics from an Evrmore node."""
    # Standard Evrmore ZMQ topics
    HASH_BLOCK: bytes
    HASH_TX: bytes
    RAW_BLOCK: bytes
    RAW_TX: bytes
    
    # Enhanced topics with automatic decoding
    BLOCK: bytes  # Automatically decoded block data
    TX: bytes     # Automatically decoded transaction data

