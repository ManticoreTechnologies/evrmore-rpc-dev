# evrmore-rpc: Python Client for Evrmore Blockchain

[![PyPI version](https://badge.fury.io/py/evrmore-rpc.svg)](https://badge.fury.io/py/evrmore-rpc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/evrmore-rpc.svg)](https://pypi.org/project/evrmore-rpc/)

A high-performance, full-featured Python client for the [Evrmore](https://evrmore.com) blockchain. Designed for real-world applications like wallets, explorers, and exchanges, it includes synchronous and asynchronous RPC support, auto-decoding ZMQ streams, rich asset tracking, and powerful dev tools.

---

## 🚀 Features

- **🔄 Context-Aware**: Auto-adapts between sync and async execution
- **⚙️ Flexible Config**: Load from `evrmore.conf`, environment, or args
- **🔐 Cookie & Auth**: Supports `.cookie` file and manual RPC credentials
- **💡 Complete RPC Coverage**: All RPC methods typed and structured
- **⚡ Connection Pooling**: Blazing fast requests with reuse support
- **🧠 Asset Intelligence**: Detects and decodes asset transactions with extras
- **📡 ZMQ Real-Time Streams**: Receive HASH_*, RAW_*, BLOCK, TX
- **🧪 Fully Tested Tools**: Built-in stress test, coverage audit, flexible demos

---

## 📦 Installation

```bash
pip install evrmore-rpc
```

---

## 🧪 Quick Start

```python
from evrmore_rpc import EvrmoreClient

client = EvrmoreClient()
info = client.getblockchaininfo()
print("Height:", info['blocks'])
```

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

| File                  | Purpose                                     |
|-----------------------|---------------------------------------------|
| `readme_test.py`      | Basic synchronous and async usage demo      |
| `stress_test.py`      | Performance benchmark w/ metrics            |
| `connection_pooling.py`| Show pooling vs no-pooling RPC comparisons |
| `flexible_config.py`  | Load settings from multiple sources         |
| `rpc_coverage.py`     | Validate RPC method coverage + docs         |
| `zmq_notifications.py`| Listen to real-time decoded blockchain txs  |

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

`evrmore-rpc` is a production-grade toolkit for Evrmore developers. Whether you're building block explorers, trading platforms, or indexers, it's engineered to deliver speed, reliability, and seamless integration with the Evrmore chain.

# WebSocket Integration Guide

This guide covers how to use WebSocket notifications with the `evrmore-rpc` package to receive real-time blockchain updates.

## Overview

The `EvrmoreWebSocketClient` provides a modern interface for receiving real-time blockchain notifications via WebSocket. It supports:

- Automatic context detection (sync/async)
- Enhanced asset metadata in decoded transactions
- Automatic reconnection on connection loss
- Clean shutdown and resource management
- Typed notification data with structured fields

## Configuration

### Required evrmore.conf Settings

Add these lines to your `evrmore.conf`:

```ini
server=1
rpcallowip=127.0.0.1
rpcbind=127.0.0.1
```

### Client Setup

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.websocket import EvrmoreWebSocketClient, WebSocketTopic

# Create RPC client for auto-decoding
rpc = EvrmoreClient()

# Create WebSocket client
ws = EvrmoreWebSocketClient(
    ws_host="127.0.0.1",
    ws_port=8332,
    topics=[WebSocketTopic.BLOCK, WebSocketTopic.TX],
    rpc_client=rpc,
    auto_decode=True
)
```

## Available Topics

| Topic | Description | Requires RPC |
|-------|-------------|-------------|
| `BLOCK` | Block notifications | Yes |
| `TX` | Transaction notifications | Yes |
| `ASSET` | Asset notifications | Yes |
| `ADDRESS` | Address notifications | Yes |

## Event Handlers

### Block Notifications

```python
@ws.on(WebSocketTopic.BLOCK)
def handle_block(notification):
    print(f"Block #{notification.height}")
    print(f"Hash: {notification.hash}")
    print(f"Transactions: {len(notification.tx)}")
    
    # Access block data
    block = notification.block
    print(f"Size: {block.get('size', 'N/A')} bytes")
    print(f"Time: {block.get('time', 'N/A')}")
    print(f"Difficulty: {block.get('difficulty', 'N/A')}")
```

### Transaction Notifications

```python
@ws.on(WebSocketTopic.TX)
def handle_tx(notification):
    print(f"TX {notification.txid}")
    print(f"Size: {notification.size} bytes")
    print(f"Version: {notification.version}")
    
    # Check for asset data
    if notification.has_assets:
        print("\nAsset Information:")
        for asset in notification.asset_info:
            print(f"Asset: {asset.name}")
            print(f"Amount: {asset.amount}")
            print(f"Type: {asset.type}")
```

## Usage Examples

### Synchronous Usage

```python
import signal
import sys
from evrmore_rpc.websocket import EvrmoreWebSocketClient, WebSocketTopic

# Initialize client
ws = EvrmoreWebSocketClient()

# Handle Ctrl+C
def signal_handler(sig, frame):
    print("\nShutting down...")
    ws.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Register handlers
@ws.on(WebSocketTopic.BLOCK)
def handle_block(notification):
    print(f"Block #{notification.height}")

@ws.on(WebSocketTopic.TX)
def handle_tx(notification):
    print(f"TX {notification.txid}")

# Start the client
ws.start()

# Keep running
while True:
    import time
    time.sleep(1)
```

### Asynchronous Usage

```python
import asyncio
from evrmore_rpc.websocket import EvrmoreWebSocketClient, WebSocketTopic

async def main():
    # Initialize client
    ws = EvrmoreWebSocketClient()

    # Register handlers
    @ws.on(WebSocketTopic.BLOCK)
    async def handle_block(notification):
        print(f"Block #{notification.height}")

    @ws.on(WebSocketTopic.TX)
    async def handle_tx(notification):
        print(f"TX {notification.txid}")

    # Start the client
    await ws.start()
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await ws.stop()

asyncio.run(main())
```

## Advanced Features

### Custom Message Processing

```python
class BlockchainMonitor:
    def __init__(self):
        self.ws_client = EvrmoreWebSocketClient()
        self.rpc_client = EvrmoreClient()
        self.blocks_processed = 0
        self.transactions_processed = 0
        self.asset_transfers = []
        
    async def start(self):
        # Register handlers
        self.ws_client.on_block(self.handle_block)
        self.ws_client.on_transaction(self.handle_transaction)
        
        # Start the WebSocket client
        await self.ws_client.start()
        print("Blockchain monitor started")
        
    async def stop(self):
        await self.ws_client.stop()
        print("Blockchain monitor stopped")
        
    async def handle_block(self, notification):
        block_hash = notification.hash
        block = self.rpc_client.getblock(block_hash)
        
        self.blocks_processed += 1
        print(f"New block: {block.hash} (height: {block.height})")
        print(f"Block contains {len(block.tx)} transactions")
        
        # Analyze block data
        if len(block.tx) > 100:
            print(f"Large block detected: {len(block.tx)} transactions")
        
    async def handle_transaction(self, notification):
        txid = notification.txid
        
        try:
            tx = self.rpc_client.getrawtransaction(txid, True)
            self.transactions_processed += 1
            
            # Check for asset transfers
            for vout in tx.vout:
                if "asset" in vout.get("scriptPubKey", {}).get("asset", {}):
                    asset = vout["scriptPubKey"]["asset"]
                    print(f"Asset transfer detected: {asset['name']} ({asset['amount']})")
                    
                    self.asset_transfers.append({
                        "txid": txid,
                        "asset": asset["name"],
                        "amount": asset["amount"],
                        "time": tx.time if hasattr(tx, "time") else None
                    })
        except Exception as e:
            print(f"Error processing transaction {txid}: {e}")
```

## Error Handling

```python
from evrmore_rpc.websocket import EvrmoreWebSocketError

try:
    ws.start()
except EvrmoreWebSocketError as e:
    print(f"WebSocket error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Considerations

- Use appropriate reconnection settings
- Set appropriate cleanup timeouts
- Consider using async mode for better performance
- Monitor memory usage with large transaction volumes
- Use connection pooling for multiple clients

## See Also

- [Getting Started](getting-started.md) for basic usage
- [API Reference](api-reference.md) for detailed API docs
- [Examples](examples.md) for more code samples
- [Advanced Usage](advanced.md) for production patterns
