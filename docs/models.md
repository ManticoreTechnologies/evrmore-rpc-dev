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

`evrmore-rpc` is a production-grade toolkit for Evrmore developers. Whether you're building block explorers, trading platforms, indexers, or decentralized tools, it's engineered to deliver speed, type-safety, real-time insight, and robust integration with the Evrmore chain.
