# examples/features/zmq_notifications.py

"""
📌 Feature: ZMQ Notifications
-----------------------------
This example demonstrates how to use the `EvrmoreZMQClient` to receive real-time
blockchain notifications from an Evrmore node via ZeroMQ.

Evrmore supports several notification topics including:
- HASH_BLOCK: Block hashes
- HASH_TX: Transaction hashes
- BLOCK: Fully decoded blocks (requires RPC)
- TX: Fully decoded transactions (requires RPC)

This example:
1. Subscribes to all enhanced topics (BLOCK, TX)
2. Uses a provided RPC client to decode notification payloads
3. Shows both block and transaction information

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

# Create a ZMQ client, requesting decoded data for enhanced topics
zmq = EvrmoreZMQClient(
    zmq_host="127.0.0.1",
    zmq_port=28332,
    topics=[ZMQTopic.BLOCK, ZMQTopic.TX],
    rpc_client=rpc
)

# Subscribe to decoded blocks
@zmq.on(ZMQTopic.BLOCK)
def handle_block(notification):
    print("\n📦 [Block Notification]")
    print(f"  ➤ Block height: {notification.height}")
    print(f"  ➤ Hash: {notification.hex}")
    print(f"  ➤ Transactions: {len(notification.block['tx'])}")

# Subscribe to decoded transactions
@zmq.on(ZMQTopic.TX)
def handle_tx(notification):
    print("\n🔄 [Transaction Notification]")
    print(f"  ➤ TXID: {notification.tx['txid']}")
    print(f"  ➤ Inputs: {len(notification.tx['vin'])}, Outputs: {len(notification.tx['vout'])}")
    if notification.has_assets:
        print("  ➤ Contains asset operations:")
        for asset in notification.asset_info:
            print(f"    - {asset['asset_name']} ({asset['type']}) x{asset['amount']}")

# Start listening for messages
print("📡 Listening for ZMQ notifications... Press Ctrl+C to stop.")
try:
    zmq.start()  # Works in both sync and async
    input("\n⏳ Press Enter to exit...\n")
finally:
    zmq.stop()
    rpc.close_sync()
