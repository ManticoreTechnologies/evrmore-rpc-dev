### ZMQ Client API

The ZMQ client provides a seamless API that works in both synchronous and asynchronous contexts.

#### Initialization

```python
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Default initialization
zmq = EvrmoreZMQClient()  # Default host: 127.0.0.1, port: 28332

# Custom ZMQ endpoint
zmq = EvrmoreZMQClient(zmq_host="192.168.1.100", zmq_port=28333)

# Specific topics (default is all topics)
zmq = EvrmoreZMQClient(topics=[ZMQTopic.HASH_BLOCK, ZMQTopic.HASH_TX])
```

#### Configuration

```python
# Set lingering time for fast shutdown (0 = no lingering)
zmq.set_lingering(0)

# Set cleanup timeouts for graceful shutdown
zmq.set_cleanup_timeouts(thread_timeout=0.1, task_timeout=0.1)

# Force synchronous mode regardless of context
zmq.force_sync()

# Force asynchronous mode regardless of context
zmq.force_async()

# Reset to auto-detect mode (default behavior)
zmq.reset()
```

#### Starting and Stopping

```python
# Start the client - works in both sync and async contexts
zmq.start()  # In sync context
await zmq.start()  # In async context

# Stop the client - works in both sync and async contexts
zmq.stop()  # In sync context
await zmq.stop()  # In async context

# Force immediate exit (for emergencies)
zmq.stop(force=True)  # Exits program immediately
```

#### Event Handlers

```python
# Register a handler for a topic with decorator
@zmq.on(ZMQTopic.HASH_BLOCK)
def on_new_block(notification):
    print(f"New block: {notification.hex}")

@zmq.on(ZMQTopic.HASH_TX)
def on_new_tx(notification):
    print(f"New transaction: {notification.hex}")
```

#### Example: ZMQ Synchronous Usage

```python
import signal
import sys
import time
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Initialize client
zmq = EvrmoreZMQClient()
zmq.set_lingering(0)  # For fast shutdown

# Handle Ctrl+C for clean shutdown
def signal_handler(sig, frame):
    print("\nShutting down...")
    zmq.stop()
    print("Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Register handlers
@zmq.on(ZMQTopic.HASH_BLOCK)
def on_new_block(notification):
    print(f"New block: {notification.hex}")

@zmq.on(ZMQTopic.HASH_TX)
def on_new_transaction(notification):
    print(f"New transaction: {notification.hex}")

# Start the client
zmq.start()

# Main loop
try:
    while True:
        print("Waiting for events...")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nShutting down...")
    zmq.stop()

#### Example: ZMQ Asynchronous Usage

```python
import asyncio
import signal
import sys
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Create event for shutdown
shutdown_event = asyncio.Event()

# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\nShutdown initiated...")
    if not shutdown_event.is_set():
        shutdown_event.set()

signal.signal(signal.SIGINT, signal_handler)

async def main():
    # Initialize client
    zmq = EvrmoreZMQClient()
    zmq.set_lingering(0)  # For fast shutdown

    # Register handlers
    @zmq.on(ZMQTopic.HASH_BLOCK)
    def on_new_block(notification):
        print(f"New block: {notification.hex}")

    @zmq.on(ZMQTopic.HASH_TX)
    def on_new_transaction(notification):
        print(f"New transaction: {notification.hex}")

    # Start the client
    await zmq.start()
    
    try:
        # Wait for shutdown signal
        while not shutdown_event.is_set():
            print("Waiting for events...")
            try:
                await asyncio.wait_for(shutdown_event.wait(), timeout=5)
            except asyncio.TimeoutError:
                continue
    except asyncio.CancelledError:
        pass
    finally:
        # Stop the client
        await zmq.stop()
        print("Client stopped cleanly.")

# Run the main function
if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("Clean exit.")
    except KeyboardInterrupt:
        print("Forced exit.")

#### Example: Emergency Fast Exit

```python
import signal
import sys
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Initialize client
zmq = EvrmoreZMQClient()
zmq.set_lingering(0)  # Try to set fast shutdown

# Track if first Ctrl+C press
first_interrupt = True

# Handle Ctrl+C
def signal_handler(sig, frame):
    global first_interrupt
    
    if first_interrupt:
        print("\nPress Ctrl+C again for immediate exit")
        print("Attempting normal shutdown...")
        first_interrupt = False
        zmq.stop()  # Try normal shutdown
    else:
        print("\nForce exiting immediately!")
        zmq.stop(force=True)  # Force immediate exit

signal.signal(signal.SIGINT, signal_handler)

# Register handler
@zmq.on(ZMQTopic.HASH_BLOCK)
def on_new_block(notification):
    print(f"New block: {notification.hex}")

# Start the client
zmq.start()

# Main loop (never reached with double Ctrl+C)
print("Press Ctrl+C once for normal exit, twice for immediate exit")
try:
    import time
    while True:
        time.sleep(1)
except Exception:
    pass 