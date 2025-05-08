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
- **📡 ZMQ Notifications**: Subscribe to real-time `BLOCK`, `TX`, `RAW_*`, `HASH_*` events
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

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

rpc = EvrmoreClient()
zmq = EvrmoreZMQClient(rpc_client=rpc)

@zmq.on(ZMQTopic.BLOCK)
def block_handler(note):
    print(f"Block #{note.height} with {len(note.block['tx'])} txs")

@zmq.on(ZMQTopic.TX)
def tx_handler(note):
    print(f"TX {note.tx['txid']} has {note._vin_count} inputs")

zmq.start()
```

Supports:
- `HASH_BLOCK`, `HASH_TX`, `RAW_BLOCK`, `RAW_TX`
- `BLOCK`, `TX` (auto-decoded)
- Asset metadata and event info on decoded transactions

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

- `readme_test.py` — basic client usage
- `stress_test.py` — performance benchmarking, concurrency tests
- `connection_pooling.py` — pooled connections for sync/async
- `flexible_config.py` — shows all configuration options
- `rpc_coverage.py` — full method coverage checker
- `zmq_notifications.py` — live decoded transaction/block stream

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
