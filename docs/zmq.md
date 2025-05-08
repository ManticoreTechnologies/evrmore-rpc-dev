# evrmore-rpc: Python Client for Evrmore Blockchain

[![PyPI version](https://badge.fury.io/py/evrmore-rpc.svg)](https://badge.fury.io/py/evrmore-rpc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/evrmore-rpc.svg)](https://pypi.org/project/evrmore-rpc/)

A high-performance, fully featured Python client for the [Evrmore](https://evrmore.com) blockchain. Designed for both synchronous and asynchronous environments, it includes full RPC and ZMQ support, automatic decoding of blocks and transactions, intelligent asset detection, and robust configuration options.

---

## 🚀 Features

- **🔄 Context-Aware**: Automatically switches between sync and async modes
- **⚙️ Flexible Configuration**: Load settings from `evrmore.conf`, env vars, or manual args
- **💡 Smart RPC Handling**: Full method coverage with type hints and structured responses
- **⚡ Fast + Efficient**: Connection pooling for low-latency concurrent RPC calls
- **🧠 Asset Intelligence**: Auto-parses asset transactions with enhanced metadata
- **📡 ZMQ Notifications**: Real-time support for BLOCK, TX, HASH_*, RAW_*, and asset events
- **🧰 Fully Tested Utilities**: Includes stress test, coverage audit, pooling demo, and more

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
print("Difficulty:", info['difficulty'])
```

## 🔁 Asynchronous Usage

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

## 🧩 Configuration Options

```python
# Default (evrmore.conf)
client = EvrmoreClient()

# Env vars (EVR_RPC_*)
client = EvrmoreClient()

# Manual args
client = EvrmoreClient(url="http://localhost:8819", rpcuser="user", rpcpassword="pass")

# Testnet toggle
client = EvrmoreClient(testnet=True)
```

Supports cookie authentication and auto-parsing of `.cookie` file.

---

## 💰 Asset Support

```python
# Get asset info
info = client.getassetdata("MYTOKEN")
print(info['amount'], info['reissuable'])

# Transfer asset
txid = client.transfer("MYTOKEN", 100, "EVRAddress")
```

---

## 📡 ZMQ Notifications (Real-Time)

# ZMQ Notifications Guide

This guide covers how to use ZeroMQ (ZMQ) notifications with the `evrmore-rpc` package to receive real-time blockchain updates.

## Overview

The `EvrmoreZMQClient` provides a seamless interface for receiving real-time blockchain notifications via ZeroMQ. It supports:

- Automatic context detection (sync/async)
- Enhanced asset metadata in decoded transactions
- Automatic reconnection on connection loss
- Clean shutdown and resource management
- Typed notification data with structured fields

## Configuration

### Required evrmore.conf Settings

Add these lines to your `evrmore.conf`:

```ini
zmqpubhashblock=tcp://127.0.0.1:28332
zmqpubhashtx=tcp://127.0.0.1:28332
zmqpubrawblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28332
```

### Client Setup

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Create RPC client for auto-decoding
rpc = EvrmoreClient()

# Create ZMQ client
zmq = EvrmoreZMQClient(
    zmq_host="127.0.0.1",
    zmq_port=28332,
    topics=[ZMQTopic.BLOCK, ZMQTopic.TX],
    rpc_client=rpc,
    auto_decode=True
)
```

## Available Topics

| Topic | Description | Requires RPC |
|-------|-------------|-------------|
| `HASH_BLOCK` | Block hash notifications | No |
| `HASH_TX` | Transaction hash notifications | No |
| `RAW_BLOCK` | Raw serialized block data | No |
| `RAW_TX` | Raw serialized transaction data | No |
| `BLOCK` | Auto-decoded block data | Yes |
| `TX` | Auto-decoded transaction data | Yes |

## Event Handlers

### Block Notifications

```python
@zmq.on(ZMQTopic.BLOCK)
def handle_block(notification):
    print(f"Block #{notification.height}")
    print(f"Hash: {notification.hex}")
    print(f"Transactions: {len(notification.block['tx'])}")
    
    # Access block data
    block = notification.block
    print(f"Size: {block.get('size', 'N/A')} bytes")
    print(f"Time: {block.get('time', 'N/A')}")
    print(f"Difficulty: {block.get('difficulty', 'N/A')}")
```

### Transaction Notifications

```python
@zmq.on(ZMQTopic.TX)
def handle_tx(notification):
    print(f"TX {notification.tx['txid']}")
    print(f"Size: {notification.tx.get('size', 'N/A')} bytes")
    print(f"Version: {notification.tx.get('version', 'N/A')}")
    
    # Check for asset data
    if notification.has_assets:
        print("\nAsset Information:")
        for asset in notification.asset_info:
            print(f"Asset: {asset.get('name', 'N/A')}")
            print(f"Amount: {asset.get('amount', 'N/A')}")
            print(f"Type: {asset.get('type', 'N/A')}")
```

## Usage Examples

### Synchronous Usage

```python
import signal
import sys
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Initialize client
zmq = EvrmoreZMQClient()
zmq.set_lingering(0)  # For fast shutdown

# Handle Ctrl+C
def signal_handler(sig, frame):
    print("\nShutting down...")
    zmq.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Register handlers
@zmq.on(ZMQTopic.BLOCK)
def handle_block(notification):
    print(f"Block #{notification.height}")

@zmq.on(ZMQTopic.TX)
def handle_tx(notification):
    print(f"TX {notification.tx['txid']}")

# Start the client
zmq.start()

# Keep running
while True:
    import time
    time.sleep(1)
```

### Asynchronous Usage

```python
import asyncio
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

async def main():
    # Initialize client
    zmq = EvrmoreZMQClient()
    zmq.set_lingering(0)

    # Register handlers
    @zmq.on(ZMQTopic.BLOCK)
    async def handle_block(notification):
        print(f"Block #{notification.height}")

    @zmq.on(ZMQTopic.TX)
    async def handle_tx(notification):
        print(f"TX {notification.tx['txid']}")

    # Start the client
    await zmq.start()
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await zmq.stop()

asyncio.run(main())
```

## Advanced Features

### Custom Message Processing

```python
class BlockchainMonitor:
    def __init__(self):
        self.zmq_client = EvrmoreZMQClient()
        self.rpc_client = EvrmoreClient()
        self.blocks_processed = 0
        self.transactions_processed = 0
        self.asset_transfers = []
        
    async def start(self):
        # Register handlers
        self.zmq_client.on_block(self.handle_block)
        self.zmq_client.on_transaction(self.handle_transaction)
        
        # Start the ZMQ client
        await self.zmq_client.start()
        print("Blockchain monitor started")
        
    async def stop(self):
        await self.zmq_client.stop()
        print("Blockchain monitor stopped")
        
    async def handle_block(self, notification):
        block_hash = notification.hex
        block = self.rpc_client.getblock(block_hash)
        
        self.blocks_processed += 1
        print(f"New block: {block.hash} (height: {block.height})")
        print(f"Block contains {len(block.tx)} transactions")
        
        # Analyze block data
        if len(block.tx) > 100:
            print(f"Large block detected: {len(block.tx)} transactions")
        
    async def handle_transaction(self, notification):
        txid = notification.hex
        
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
from evrmore_rpc.zmq import EvrmoreZMQError

try:
    zmq.start()
except EvrmoreZMQError as e:
    print(f"ZMQ error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Considerations

- Use `set_lingering(0)` for fast shutdown
- Set appropriate cleanup timeouts
- Consider using async mode for better performance
- Monitor memory usage with large transaction volumes

## See Also

- [Getting Started](getting-started.md) for basic usage
- [API Reference](api-reference.md) for detailed API docs
- [Examples](examples.md) for more code samples
- [Advanced Usage](advanced.md) for production patterns

---

## 📊 Stress Test Results

Real benchmark results from the `stress_test.py` utility:

| Mode            | Time    | RPS      | Avg (ms) | Median | Min  | Max  |
|-----------------|---------|----------|----------|--------|------|------|
| Local Async     | 0.01 s  | 10442.42 | 0.59     | 0.50   | 0.39 | 1.84 |
| Local Sync      | 0.06 s  | 1861.26  | 1.52     | 1.42   | 0.43 | 3.40 |
| Remote Async    | 1.75 s  | 57.31    | 167.77   | 155.93 | 111  | 324  |
| Remote Sync     | 1.86 s  | 53.83    | 160.39   | 163.26 | 112  | 310  |

Tested with `getblockcount`, 100 requests, 10 concurrent workers

---

## 🧬 Utilities & Examples

```bash
python3 -m evrmore_rpc.stress_test --sync --remote
```

Examples:
- `readme_test.py` — basic usage demo
- `stress_test.py` — concurrency performance test
- `connection_pooling.py` — show pooled reuse efficiency
- `flexible_config.py` — env var / conf / manual setup demo
- `rpc_coverage.py` — validates full RPC method mapping
- `zmq_notifications.py` — real-time block/tx decode stream

---

## 🧪 Requirements

- Python 3.8+
- Evrmore daemon running with RPC and optional ZMQ endpoints

---

## 🪪 License

MIT License — See [LICENSE](LICENSE)

---

## 🤝 Contributing

PRs welcome! Please lint, document, and include examples.

```bash
git clone https://github.com/manticoretechnologies/evrmore-rpc-dev
cd evrmore-rpc
python3 -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

Run tests with:

```bash
python3 -m evrmore_rpc.stress_test
```

---

## 🧭 Summary

`evrmore-rpc` is more than a wrapper — it's a full dev toolkit for Evrmore. Built for production-grade systems needing precision, flexibility, and real-time awareness. Perfect for explorers, exchanges, indexers, and power users.
