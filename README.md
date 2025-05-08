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
- **📡 ZMQ Notifications**: Subscribe to real-time blockchain events with auto-decoding
- **🧰 Fully Tested Utilities**: Stress test, coverage verification, pooling demo, and more

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

# Environment Variables
# EVR_RPC_URL=http://localhost:8819
# EVR_RPC_USER=user
# EVR_RPC_PASSWORD=pass
# EVR_RPC_PORT=8819
# EVR_TESTNET=true
client = EvrmoreClient()

# Manual Configuration
client = EvrmoreClient(
    url="http://localhost:8819",
    rpcuser="user",
    rpcpassword="pass",
    rpcport=8819,
    testnet=True,
    timeout=30,
    async_mode=None  # Auto-detect or force sync/async
)

# Cookie Authentication
# Automatically reads from ~/.evrmore/.cookie
client = EvrmoreClient(datadir="~/.evrmore")
```

---

## 💰 Asset Support

```python
# Get asset info
info = client.getassetdata("MYTOKEN")
print(info['amount'], info['reissuable'])

# Transfer asset
txid = client.transfer("MYTOKEN", 100, "EVRAddress")

# Enhanced asset metadata in ZMQ notifications
@zmq.on(ZMQTopic.TX)
def tx_handler(note):
    if note.has_assets:
        print(f"Asset info: {note.asset_info}")
```

---

## 📡 ZMQ Notifications (Real-Time)

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Create RPC client for auto-decoding
rpc = EvrmoreClient()

# Create ZMQ client with auto-decoding enabled
zmq = EvrmoreZMQClient(
    zmq_host="127.0.0.1",
    zmq_port=28332,
    topics=[ZMQTopic.BLOCK, ZMQTopic.TX],
    rpc_client=rpc,
    auto_decode=True
)

# Subscribe to decoded blocks
@zmq.on(ZMQTopic.BLOCK)
def block_handler(note):
    print(f"Block #{note.height}")
    print(f"Hash: {note.hex}")
    print(f"Transactions: {len(note.block['tx'])}")

# Subscribe to decoded transactions
@zmq.on(ZMQTopic.TX)
def tx_handler(note):
    print(f"TX {note.tx['txid']}")
    if note.has_assets:
        print(f"Asset info: {note.asset_info}")

# Start in current context (sync/async)
zmq.start()
```

Available Topics:
- `HASH_BLOCK`: Block hash notifications
- `HASH_TX`: Transaction hash notifications
- `RAW_BLOCK`: Raw serialized block data
- `RAW_TX`: Raw serialized transaction data
- `BLOCK`: Auto-decoded block data (requires RPC)
- `TX`: Auto-decoded transaction data (requires RPC)

Features:
- Automatic context detection (sync/async)
- Enhanced asset metadata in decoded transactions
- Automatic reconnection on connection loss
- Clean shutdown and resource management
- Typed notification data with structured fields

Required evrmore.conf settings:
```
zmqpubhashblock=tcp://127.0.0.1:28332
zmqpubhashtx=tcp://127.0.0.1:28332
zmqpubrawblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28332
```

---

## 📊 Stress Test Results

Tested on local node and remote RPC endpoint:

| Mode            | Time    | RPS      | Avg (ms) | Median | Min  | Max  |
|-----------------|---------|----------|----------|--------|------|------|
| Local Async     | 0.01 s  | 10442.42 | 0.59     | 0.50   | 0.39 | 1.84 |
| Local Sync      | 0.06 s  | 1861.26  | 1.52     | 1.42   | 0.43 | 3.40 |
| Remote Async    | 1.75 s  | 57.31    | 167.77   | 155.93 | 111  | 324  |
| Remote Sync     | 1.86 s  | 53.83    | 160.39   | 163.26 | 112  | 310  |

---

## 🔬 Examples & Utilities

- `basic_queries.py` — basic client usage
- `async_example.py` — async client usage
- `asset_operations.py` — asset management
- `zmq_auto_decode_example.py` — ZMQ with auto-decoding
- `cookie_auth.py` — cookie authentication
- `stress_test.py` — performance benchmarking
- `connection_pooling.py` — pooled connections
- `flexible_config.py` — configuration options
- `complete_rpc_coverage.py` — method coverage checker

Run with:
```bash
python3 -m evrmore_rpc.stress_test --sync --remote
```

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
git clone https://github.com/youruser/evrmore-rpc
cd evrmore-rpc
python3 -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

Test locally with:
```bash
python3 -m evrmore_rpc.stress_test
```

---

## 🧭 Summary

`evrmore-rpc` is not just a wrapper — it's a full developer toolkit for Evrmore blockchain apps. With context-aware clients, full RPC coverage, rich ZMQ integration, and intelligent asset decoding, it's built to power production-grade wallets, explorers, indexers, and game engines alike.

Enjoy building with it.
