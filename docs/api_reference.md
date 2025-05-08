# API Reference

This page documents the main classes and methods of the `evrmore-rpc` Python package.

## Overview

The `evrmore-rpc` library provides a full-featured, production-grade API for interacting with the Evrmore blockchain. It supports:

- **Synchronous and Asynchronous Clients**: Choose between `EvrmoreClient` or `EvrmoreAsyncRPCClient`.
- **ZMQ Notifications**: Stream real-time block and transaction data.
- **WebSockets**: Push blockchain data to clients with subscription support.
- **Typed Models**: Built with Pydantic for strong typing and validation.
- **Flexible Configuration**: Works out-of-the-box with `evrmore.conf`, env vars, or direct credentials.

---

## 🚀 Main Classes

| Class | Description | Import Path |
|-------|-------------|-------------|
| `EvrmoreClient` | Main synchronous client | `from evrmore_rpc import EvrmoreClient` |
| `EvrmoreZMQClient` | ZMQ notifications client | `from evrmore_rpc.zmq import EvrmoreZMQClient` |
| `EvrmoreWebSocketClient` | WebSocket client | `from evrmore_rpc.websockets import EvrmoreWebSocketClient` |
| `EvrmoreWebSocketServer` | WebSocket server | `from evrmore_rpc.websockets import EvrmoreWebSocketServer` |

---

## 🧪 Quick Example

```python
from evrmore_rpc import EvrmoreClient

# Create a client
client = EvrmoreClient()

# Get blockchain info
info = client.getblockchaininfo()
print(f"Current block height: {info.blocks}")
print(f"Chain: {info.chain}")
print(f"Difficulty: {info.difficulty}")

# Get a specific block
block_hash = client.getblockhash(1)
block = client.getblock(block_hash)
print(f"Block #1 hash: {block.hash}")
print(f"Block #1 time: {block.time}")
print(f"Block #1 transactions: {len(block.tx)}")
```

---

## 🧠 Design Philosophy

- ✅ **Type Safety**: All methods return validated, documented models using Pydantic.
- 🔁 **Context Awareness**: Clients auto-adapt to sync/async environments.
- ⚡ **Performance First**: Fast connection pooling, minimal overhead.
- 🔐 **Secure Defaults**: Supports `.cookie` auth, encrypted RPC, and env-based credentials.
- 🧩 **Composable**: All classes and utilities are modular and extendable.

---

## 🔎 Explore More

- [Synchronous API](sync_api.md): Traditional blocking usage via `EvrmoreClient`
- [Asynchronous API](async_api.md): Async/await programming via `EvrmoreAsyncRPCClient`
- [ZMQ Support](zmq.md): Realtime blockchain streaming with `EvrmoreZMQClient`
- [WebSockets Support](websockets.md): Pub-sub architecture using `EvrmoreWebSocketServer`
- [Data Models](models.md): Full list of typed structures returned from RPC
- [Usage Examples](examples.md): Dashboards, stress tests, DEX logic, more

---

For additional CLI usage, performance benchmarks, and integrations, check the [README](index.md) and the `examples/` directory.
