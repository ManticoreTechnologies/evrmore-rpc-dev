# examples/features/zmq_notifications.py

"""
📌 Feature: ZMQ Notifications
-----------------------------
This example demonstrates how to use the `EvrmoreZMQClient` to receive real-time
blockchain notifications from an Evrmore node via ZeroMQ.

Features:
- Automatic context detection (sync/async)
- Enhanced asset metadata in decoded transactions
- Automatic reconnection on connection loss
- Clean shutdown and resource management
- Typed notification data with structured fields
- Seamless API that works in both sync and async contexts

Available Topics:
- HASH_BLOCK: Block hash notifications
- HASH_TX: Transaction hash notifications
- RAW_BLOCK: Raw serialized block data
- RAW_TX: Raw serialized transaction data
- BLOCK: Auto-decoded block data (requires RPC)
- TX: Auto-decoded transaction data (requires RPC)

✅ Requires `zmqpub*` entries in your `evrmore.conf`:
    zmqpubhashblock=tcp://127.0.0.1:28332
    zmqpubhashtx=tcp://127.0.0.1:28332
    zmqpubrawblock=tcp://127.0.0.1:28332
    zmqpubrawtx=tcp://127.0.0.1:28332

✅ Requires a running Evrmore node with ZMQ enabled.
"""

from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Create a synchronous RPC client
rpc = EvrmoreClient()

# Create a ZMQ client with auto-decoding enabled
zmq = EvrmoreZMQClient(
    zmq_host="127.0.0.1",
    zmq_port=28332,
    topics=[ZMQTopic.BLOCK, ZMQTopic.TX],
    rpc_client=rpc,
    auto_decode=True
)

# Subscribe to decoded blocks
@zmq.on(ZMQTopic.BLOCK)
def handle_block(notification):
    print("\n📦 [Block Notification]")
    print(f"  ➤ Block height: {notification.height}")
    print(f"  ➤ Hash: {notification.hex}")
    print(f"  ➤ Transactions: {len(notification.block['tx'])}")
    
    # Access block data
    block = notification.block
    print(f"  ➤ Size: {block.get('size', 'N/A')} bytes")
    print(f"  ➤ Time: {block.get('time', 'N/A')}")
    print(f"  ➤ Difficulty: {block.get('difficulty', 'N/A')}")

# Subscribe to decoded transactions
@zmq.on(ZMQTopic.TX)
def handle_tx(notification):
    print("\n💸 [Transaction Notification]")
    print(f"  ➤ TXID: {notification.tx['txid']}")
    print(f"  ➤ Size: {notification.tx.get('size', 'N/A')} bytes")
    print(f"  ➤ Version: {notification.tx.get('version', 'N/A')}")
    
    # Check for asset data
    if notification.has_assets:
        print("\n  📊 [Asset Information]")
        for asset in notification.asset_info:
            print(f"    ➤ Asset: {asset.get('name', 'N/A')}")
            print(f"    ➤ Amount: {asset.get('amount', 'N/A')}")
            print(f"    ➤ Type: {asset.get('type', 'N/A')}")

# Start the ZMQ client
# This will auto-detect if we're in an async context
zmq.start()

# For async usage:
"""
async def main():
    zmq = EvrmoreZMQClient(
        zmq_host="127.0.0.1",
        zmq_port=28332,
        topics=[ZMQTopic.BLOCK, ZMQTopic.TX],
        rpc_client=rpc,
        auto_decode=True
    )
    
    @zmq.on(ZMQTopic.BLOCK)
    async def handle_block(notification):
        # Async handlers work too!
        print(f"Block #{notification.height}")
    
    await zmq.start()
    
    # Keep running
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
"""
