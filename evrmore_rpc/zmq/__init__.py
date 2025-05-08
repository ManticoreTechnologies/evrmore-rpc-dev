"""
ZMQ client for receiving Evrmore blockchain notifications.

This module provides functionality for subscribing to ZMQ notifications from an Evrmore node.

Fast Cleanup & Shutdown:
The ZMQ client is optimized for fast shutdown with these options:
- Default linger time is now 0ms (no waiting for message delivery)
- Default thread join timeout is 0.1s
- Default task cancel timeout is 0.1s
- Use stop(force=True) for immediate exit without waiting for cleanup

Enhanced ZMQ Topics:
In addition to standard ZMQ topics (HASH_BLOCK, HASH_TX, RAW_BLOCK, RAW_TX),
this module provides enhanced topics that automatically decode the data:
- ZMQTopic.BLOCK: Automatically fetches and decodes full block data
- ZMQTopic.TX: Automatically fetches and decodes full transaction data

Asset Detection & Tracking:
The enhanced ZMQ topics now include automatic detection of asset-related transactions:
- Detects asset transfers, issuances, and reissuances
- Identifies asset name, type, amount, and receiving address
- Fetches additional asset information using the RPC client
- Includes current address balances for assets when available

Example:
```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic, ZMQDecodedBlockNotification, ZMQDecodedTxNotification

# Create RPC client for decoding (required for enhanced topics)
rpc = EvrmoreClient()

# Create ZMQ client with RPC for automatic decoding
zmq = EvrmoreZMQClient(
    rpc_client=rpc,                     # Required for auto-decoding
    topics=[ZMQTopic.BLOCK, ZMQTopic.TX]  # Enhanced topics
)

# Register for enhanced topics with decoded data
@zmq.on(ZMQTopic.BLOCK)
def on_block(notification: ZMQDecodedBlockNotification):
    # Access full block data with notification.block
    print(f"New block at height {notification.height}")
    print(f"Contains {notification._tx_count} transactions")

@zmq.on(ZMQTopic.TX)
def on_tx(notification: ZMQDecodedTxNotification):
    # Access full transaction data with notification.tx
    print(f"New transaction: {notification.hex}")
    print(f"Has {notification._vin_count} inputs and {notification._vout_count} outputs")
    
    # Check for asset transactions
    if notification.has_assets:
        print(f"Asset transaction detected with {len(notification.asset_info)} operations")
        for asset_info in notification.asset_info:
            print(f"Asset: {asset_info['asset_name']}, Type: {asset_info['type']}")
            print(f"Amount: {asset_info['amount']}, Address: {asset_info['address']}")
            
            # Access additional asset details
            if 'asset_details' in asset_info:
                details = asset_info['asset_details']
                print(f"Total supply: {details['amount']}, Units: {details['units']}")

# Start the client and wait for notifications
zmq.start()  # Use await zmq.start() in async context
```

Fast Exit:
```python
# Exit immediately anytime
zmq.stop(force=True)
```
"""

from evrmore_rpc.zmq.client import EvrmoreZMQClient, ZMQTopic
from evrmore_rpc.zmq.models import ZMQNotification, ZMQDecodedBlockNotification, ZMQDecodedTxNotification

__all__ = [
    "EvrmoreZMQClient",
    "ZMQTopic",
    "ZMQNotification",
    "ZMQDecodedBlockNotification",
    "ZMQDecodedTxNotification"
] 