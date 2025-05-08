# evrmore-rpc: Python Client for Evrmore Blockchain

[![PyPI version](https://badge.fury.io/py/evrmore-rpc.svg)](https://badge.fury.io/py/evrmore-rpc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/evrmore-rpc.svg)](https://pypi.org/project/evrmore-rpc/)

A high-performance, production-grade Python client for the [Evrmore](https://evrmore.com) blockchain. Built for developers who need reliability, performance, and comprehensive blockchain integration.

## 🚀 Key Features

- **🔄 Context-Aware**: Seamlessly switches between sync and async modes
- **⚙️ Flexible Configuration**: Load from `evrmore.conf`, env vars, or manual args
- **💡 Complete RPC Coverage**: Full method support with type hints
- **⚡ High Performance**: Connection pooling and optimized requests
- **🧠 Asset Intelligence**: Smart asset transaction parsing
- **📡 Real-Time Events**: ZMQ notifications and WebSocket support
- **🧰 Developer Tools**: Stress testing, coverage verification, and more

## 📚 Documentation

- [Getting Started](getting-started.md) - Installation and basic usage
- [API Reference](api-reference.md) - Complete API documentation
- [ZMQ Guide](zmq.md) - Real-time blockchain notifications
- [WebSocket Guide](websockets.md) - WebSocket integration
- [Advanced Usage](advanced.md) - Advanced patterns and best practices
- [Examples](examples.md) - Code examples and tutorials
- [Development](development.md) - Contributing guide

## 🎯 Use Cases

- **Block Explorers**: Real-time block and transaction monitoring
- **Trading Platforms**: Asset management and transaction processing
- **Wallets**: Address management and transaction signing
- **Indexers**: Efficient blockchain data extraction
- **DEX Integration**: Asset trading and order management
- **Game Engines**: In-game asset and reward systems

## 🛠️ Requirements

- Python 3.8+
- Evrmore daemon with RPC enabled
- Optional: ZMQ for real-time notifications

## 🪪 License

MIT License — See [LICENSE](LICENSE)

## 🤝 Contributing

We welcome contributions! See our [Development Guide](development.md) for details.

```bash
git clone https://github.com/manticoretechnologies/evrmore-rpc-dev
cd evrmore-rpc
python3 -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```
