# evrmore-rpc: Python Client for Evrmore Blockchain

[![PyPI version](https://badge.fury.io/py/evrmore-rpc.svg)](https://badge.fury.io/py/evrmore-rpc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/evrmore-rpc.svg)](https://pypi.org/project/evrmore-rpc/)

A high-performance, full-featured Python client for the [Evrmore](https://evrmore.com) blockchain. Designed for real-world applications like wallets, explorers, and exchanges, it includes synchronous and asynchronous RPC support, auto-decoding ZMQ streams, typed WebSocket communication, structured data models, and powerful developer tools.

---

## 🚀 Features

- **🔄 Context-Aware**: Auto-adapts between sync and async execution
- **⚙️ Flexible Config**: Load from `evrmore.conf`, environment, or arguments
- **🔐 Cookie & Auth**: Supports `.cookie` file and manual RPC credentials
- **💡 Typed RPC Coverage**: All RPC methods typed with Pydantic models
- **⚡ Connection Pooling**: Fast RPC calls with keep-alive sessions
- **🧠 Asset Intelligence**: Decodes asset transactions, supply, metadata
- **📡 ZMQ Real-Time Streams**: HASH_*, RAW_*, BLOCK, TX w/ decoding
- **🌐 WebSocket Support**: Realtime server and client push subscriptions
- **📊 CLI & Stress Tools**: Benchmark, test, and audit performance
- **🧪 Extensive Examples**: From zero to production-ready integrations

---

## 📦 Installation

```bash
pip install evrmore-rpc
```

Optional extras:

```bash
pip install evrmore-rpc[websockets]     # For WebSocket support
pip install evrmore-rpc[full]           # All optional dependencies
```

---

## 🧪 Quick Start

```python
from evrmore_rpc import EvrmoreClient

client = EvrmoreClient()
info = client.getblockchaininfo()
print("Height:", info['blocks'])
```

---

## 🧭 Synchronous API Example

```python
from evrmore_rpc import EvrmoreClient

client = EvrmoreClient()
info = client.getblockchaininfo()
print(f"Block height: {info.blocks}")

asset_info = client.getassetdata("INFERNA")
print(asset_info.amount)

client.transfer("INFERNA", 10, "EVRAddress")
```

---

## 🔁 Async Usage

```python
import asyncio
from evrmore_rpc import EvrmoreClient

async def main():
    client = EvrmoreClient()
    info = await client.getblockchaininfo()
    print("Height:", info['blocks'])
    await client.close()

asyncio.run(main())
```

---

## 🔧 Configuration Examples

```python
# From evrmore.conf
client = EvrmoreClient()

# From env vars (EVR_RPC_*)
client = EvrmoreClient()

# Manual override
client = EvrmoreClient(url="http://localhost:8819", rpcuser="user", rpcpassword="pass")

# Testnet flag
client = EvrmoreClient(testnet=True)
```

---

## 💰 Asset Support

```python
info = client.getassetdata("INFERNA")
print(info['amount'])

client.transfer("INFERNA", 10, "EVRAddress")
```

---

## 📡 Real-Time ZMQ Notifications

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

rpc = EvrmoreClient()
zmq = EvrmoreZMQClient(rpc_client=rpc)

@zmq.on(ZMQTopic.BLOCK)
def handle_block(n):
    print(f"[BLOCK] #{n.height} with {len(n.block['tx'])} txs")

@zmq.on(ZMQTopic.TX)
def handle_tx(n):
    print(f"[TX] {n.tx['txid']} → {len(n.tx['vout'])} outputs")

zmq.start()
```

Supports:
- `HASH_BLOCK`, `HASH_TX`, `RAW_BLOCK`, `RAW_TX`
- Enhanced `BLOCK`, `TX` (auto-decoded)
- Asset-aware TX parsing

---

## 🌐 WebSocket Subscriptions

```python
from evrmore_rpc.websockets import EvrmoreWebSocketClient
import asyncio

async def main():
    client = EvrmoreWebSocketClient(uri="ws://localhost:8765")
    await client.connect()
    await client.subscribe("blocks")
    await client.subscribe("transactions")

    async for message in client:
        print(f"{message.type}: {message.data}")

asyncio.run(main())
```

Server available via `EvrmoreWebSocketServer` with ZMQ -> WS bridge built-in.

---

## 📊 Stress Test Benchmarks

From `python3 -m evrmore_rpc.stress_test`, 100 calls to `getblockcount`, 10 concurrency:

| Mode            | Time    | RPS      | Avg (ms) | Median | Min  | Max  |
|-----------------|---------|----------|----------|--------|------|------|
| Local Async     | 0.01 s  | 10442.42 | 0.59     | 0.50   | 0.39 | 1.84 |
| Local Sync      | 0.06 s  | 1861.26  | 1.52     | 1.42   | 0.43 | 3.40 |
| Remote Async    | 1.75 s  | 57.31    | 167.77   | 155.93 | 111  | 324  |
| Remote Sync     | 1.86 s  | 53.83    | 160.39   | 163.26 | 112  | 310  |

---

## 🧰 Examples

```bash
python3 -m evrmore_rpc.stress_test --sync --remote
```

| File                     | Purpose                                        |
|--------------------------|------------------------------------------------|
| `features/contextuality.py` | Auto detect sync/async usage context         |
| `features/connection_pooling.py` | Demonstrate connection reuse efficiency     |
| `features/complete_rpc_coverage.py` | Validate RPC method coverage             |
| `features/flexible_config.py` | Load configuration from various sources     |
| `features/basic_type_safety.py` | Showcase type-safe access and results      |
| `features/zmq_notifications.py` | Decoded ZMQ block/tx notifications         |
| `asset_operations.py`    | Asset transfers and issuance                   |
| `basic_queries.py`       | Query blockchain data (blocks, balance, etc)   |
| `cookie_auth.py`         | Authentication using .cookie file              |
| `async_example.py`       | Async API interaction                          |
| `test_cookie_auth.py`    | Auth unit test with .cookie                    |
| `zmq_auto_decode.py`     | Deep decoding of tx/block via ZMQ              |

---

## ✅ Requirements

- Python 3.8 or higher
- Evrmore daemon with RPC and optional ZMQ enabled

---

## 🪪 License

MIT — See [LICENSE](LICENSE)

---

## 🤝 Contributing

PRs welcome!

```bash
git clone https://github.com/manticoretechnologies/evrmore-rpc-dev
cd evrmore-rpc
python3 -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

Run tests:

```bash
python3 -m evrmore_rpc.stress_test
```

---

## 🧭 Summary

`evrmore-rpc` is a production-grade toolkit for Evrmore developers. Whether you're building block explorers, trading platforms, indexers, or decentralized tools, it's engineered to deliver speed, type-safety, real-time insight, and robust integration with the Evrmore chain.

# Code Examples

This guide provides practical examples of using the `evrmore-rpc` package for common blockchain operations.

## Basic Usage

### Initialize Client

```python
from evrmore_rpc import EvrmoreClient

# Basic initialization
client = EvrmoreClient()

# With custom configuration
client = EvrmoreClient(
    host="127.0.0.1",
    port=8332,
    username="rpcuser",
    password="rpcpass",
    ssl=True
)
```

### Get Blockchain Info

```python
# Get basic blockchain info
info = client.getblockchaininfo()
print(f"Chain: {info.chain}")
print(f"Blocks: {info.blocks}")
print(f"Headers: {info.headers}")
print(f"Best block hash: {info.bestblockhash}")
print(f"Difficulty: {info.difficulty}")
print(f"Verification progress: {info.verificationprogress}")
```

### Get Block Information

```python
# Get block by height
block = client.getblock(1000)
print(f"Block hash: {block.hash}")
print(f"Previous block: {block.previousblockhash}")
print(f"Time: {block.time}")
print(f"Transactions: {len(block.tx)}")

# Get block by hash
block = client.getblock("0000000000000000000000000000000000000000000000000000000000000000")
```

### Get Transaction Information

```python
# Get transaction by ID
tx = client.getrawtransaction("txid", True)
print(f"Transaction ID: {tx.txid}")
print(f"Version: {tx.version}")
print(f"Size: {tx.size}")
print(f"Inputs: {len(tx.vin)}")
print(f"Outputs: {len(tx.vout)}")

# Get transaction details
for vin in tx.vin:
    print(f"Input: {vin.txid}:{vin.vout}")
    print(f"Sequence: {vin.sequence}")

for vout in tx.vout:
    print(f"Output value: {vout.value}")
    print(f"Script: {vout.scriptPubKey.hex}")
```

## Asset Operations

### Get Asset Information

```python
# Get asset info
asset = client.getassetinfo("ASSET_NAME")
print(f"Asset name: {asset.name}")
print(f"Amount: {asset.amount}")
print(f"Units: {asset.units}")
print(f"Reissuable: {asset.reissuable}")
print(f"Has IPFS: {asset.has_ipfs}")
if asset.has_ipfs:
    print(f"IPFS hash: {asset.ipfs_hash}")
```

### Transfer Assets

```python
# Create asset transfer
txid = client.transferasset(
    "ASSET_NAME",
    "DESTINATION_ADDRESS",
    1.0,  # amount
    "COMMENT",
    "COMMENT_TO"
)
print(f"Transfer transaction ID: {txid}")
```

## Real-Time Notifications

### ZMQ Notifications

```python
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Initialize ZMQ client
zmq = EvrmoreZMQClient()

# Register handlers
@zmq.on(ZMQTopic.BLOCK)
def handle_block(notification):
    print(f"New block: {notification.height}")

@zmq.on(ZMQTopic.TX)
def handle_tx(notification):
    print(f"New transaction: {notification.txid}")

# Start the client
zmq.start()
```

### WebSocket Notifications

```python
from evrmore_rpc.websocket import EvrmoreWebSocketClient, WebSocketTopic

# Initialize WebSocket client
ws = EvrmoreWebSocketClient()

# Register handlers
@ws.on(WebSocketTopic.BLOCK)
def handle_block(notification):
    print(f"New block: {notification.height}")

@ws.on(WebSocketTopic.TX)
def handle_tx(notification):
    print(f"New transaction: {notification.txid}")

# Start the client
ws.start()
```

## Advanced Examples

### Block Explorer

```python
class BlockExplorer:
    def __init__(self):
        self.client = EvrmoreClient()
        self.blocks_processed = 0
        self.transactions_processed = 0
        
    def get_block_info(self, height):
        block = self.client.getblock(height)
        print(f"\nBlock #{height}")
        print(f"Hash: {block.hash}")
        print(f"Time: {block.time}")
        print(f"Size: {block.size} bytes")
        print(f"Transactions: {len(block.tx)}")
        
        # Get transaction details
        for txid in block.tx:
            tx = self.client.getrawtransaction(txid, True)
            print(f"\nTransaction: {txid}")
            print(f"Size: {tx.size} bytes")
            print(f"Inputs: {len(tx.vin)}")
            print(f"Outputs: {len(tx.vout)}")
            
            # Check for asset transfers
            for vout in tx.vout:
                if "asset" in vout.get("scriptPubKey", {}).get("asset", {}):
                    asset = vout["scriptPubKey"]["asset"]
                    print(f"Asset transfer: {asset['name']} ({asset['amount']})")
```

### Asset Tracker

```python
class AssetTracker:
    def __init__(self):
        self.client = EvrmoreClient()
        self.assets = {}
        
    def track_asset(self, asset_name):
        # Get asset info
        asset = self.client.getassetinfo(asset_name)
        self.assets[asset_name] = {
            "name": asset.name,
            "amount": asset.amount,
            "units": asset.units,
            "reissuable": asset.reissuable,
            "transfers": []
        }
        
    def get_asset_transfers(self, asset_name, start_block=0):
        if asset_name not in self.assets:
            self.track_asset(asset_name)
            
        current_height = self.client.getblockcount()
        
        for height in range(start_block, current_height + 1):
            block = self.client.getblock(height)
            
            for txid in block.tx:
                tx = self.client.getrawtransaction(txid, True)
                
                for vout in tx.vout:
                    if "asset" in vout.get("scriptPubKey", {}).get("asset", {}):
                        asset = vout["scriptPubKey"]["asset"]
                        if asset["name"] == asset_name:
                            self.assets[asset_name]["transfers"].append({
                                "txid": txid,
                                "amount": asset["amount"],
                                "block": height,
                                "time": block.time
                            })
```

### Transaction Monitor

```python
class TransactionMonitor:
    def __init__(self):
        self.client = EvrmoreClient()
        self.watched_addresses = set()
        self.transactions = {}
        
    def watch_address(self, address):
        self.watched_addresses.add(address)
        
    def get_address_transactions(self, address):
        if address not in self.watched_addresses:
            self.watch_address(address)
            
        # Get all transactions for address
        txs = self.client.getaddresstxids({"addresses": [address]})
        
        for txid in txs:
            if txid not in self.transactions:
                tx = self.client.getrawtransaction(txid, True)
                self.transactions[txid] = {
                    "txid": txid,
                    "time": tx.time,
                    "inputs": [],
                    "outputs": []
                }
                
                # Process inputs
                for vin in tx.vin:
                    if "coinbase" not in vin:
                        prev_tx = self.client.getrawtransaction(vin.txid, True)
                        prev_vout = prev_tx.vout[vin.vout]
                        self.transactions[txid]["inputs"].append({
                            "address": prev_vout.scriptPubKey.addresses[0],
                            "amount": prev_vout.value
                        })
                
                # Process outputs
                for vout in tx.vout:
                    if "addresses" in vout.scriptPubKey:
                        self.transactions[txid]["outputs"].append({
                            "address": vout.scriptPubKey.addresses[0],
                            "amount": vout.value
                        })
```

## Error Handling

```python
from evrmore_rpc import EvrmoreRPCError

try:
    # Make RPC call
    result = client.getblockchaininfo()
except EvrmoreRPCError as e:
    print(f"RPC error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Optimization

```python
# Use connection pooling
from evrmore_rpc import EvrmoreClient, ConnectionPool

# Create connection pool
pool = ConnectionPool(
    host="127.0.0.1",
    port=8332,
    username="rpcuser",
    password="rpcpass",
    max_connections=10
)

# Get client from pool
client = pool.get_client()

# Use client
result = client.getblockchaininfo()

# Return client to pool
pool.return_client(client)

# Batch process blocks
def process_blocks(start_height, end_height):
    for height in range(start_height, end_height + 1):
        block = client.getblock(height)
        # Process block data
```

## See Also

- [Getting Started](getting-started.md) for basic usage
- [API Reference](api-reference.md) for detailed API docs
- [ZMQ Guide](zmq.md) for real-time notifications
- [WebSocket Guide](websockets.md) for WebSocket integration
- [Advanced Usage](advanced.md) for production patterns
