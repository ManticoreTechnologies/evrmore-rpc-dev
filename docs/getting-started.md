# Getting Started with evrmore-rpc

This guide will help you get started with the `evrmore-rpc` Python client for the Evrmore blockchain.

## 📦 Installation

Install the package using pip:

```bash
pip install evrmore-rpc
```

Optional extras:

```bash
pip install evrmore-rpc[websockets]     # For WebSocket support
pip install evrmore-rpc[full]           # All optional dependencies
```

## 🚀 Quick Start

### Basic Usage

```python
from evrmore_rpc import EvrmoreClient

# Create a client (auto-loads from evrmore.conf)
client = EvrmoreClient()

# Get blockchain info
info = client.getblockchaininfo()
print(f"Current block height: {info['blocks']}")
print(f"Chain: {info['chain']}")
print(f"Difficulty: {info['difficulty']}")

# Get a specific block
block_hash = client.getblockhash(1)
block = client.getblock(block_hash)
print(f"Block #1 hash: {block.hash}")
print(f"Block #1 time: {block.time}")
print(f"Block #1 transactions: {len(block.tx)}")
```

### Asynchronous Usage

```python
import asyncio
from evrmore_rpc import EvrmoreClient

async def main():
    # Create client
    client = EvrmoreClient()
    
    # Get blockchain info
    info = await client.getblockchaininfo()
    print(f"Current block height: {info['blocks']}")
    
    # Get a block
    block_hash = await client.getblockhash(1)
    block = await client.getblock(block_hash)
    print(f"Block #1 hash: {block.hash}")
    
    # Close the client
    await client.close()

# Run the async code
asyncio.run(main())
```

## ⚙️ Configuration

The client can be configured in several ways:

### 1. Using evrmore.conf

By default, the client will look for `evrmore.conf` in the default Evrmore data directory:

```python
client = EvrmoreClient()  # Auto-loads from evrmore.conf
```

### 2. Environment Variables

Set these environment variables to configure the client:

```bash
EVR_RPC_URL=http://localhost:8819
EVR_RPC_USER=user
EVR_RPC_PASSWORD=pass
EVR_RPC_PORT=8819
EVR_TESTNET=true
```

Then create the client:

```python
client = EvrmoreClient()  # Auto-loads from environment
```

### 3. Manual Configuration

```python
client = EvrmoreClient(
    url="http://localhost:8819",
    rpcuser="user",
    rpcpassword="pass",
    rpcport=8819,
    testnet=True,
    timeout=30,
    async_mode=None  # Auto-detect or force sync/async
)
```

### 4. Cookie Authentication

The client can automatically read from the `.cookie` file:

```python
client = EvrmoreClient(datadir="~/.evrmore")
```

## 💰 Asset Support

```python
# Get asset info
info = client.getassetdata("MYTOKEN")
print(f"Amount: {info['amount']}")
print(f"Reissuable: {info['reissuable']}")

# Transfer asset
txid = client.transfer("MYTOKEN", 100, "EVRAddress")
print(f"Transfer txid: {txid}")
```

## 📡 Real-Time Notifications

For real-time blockchain notifications, see the [ZMQ Guide](zmq.md) and [WebSocket Guide](websockets.md).

## 🔍 Next Steps

- Check out the [API Reference](api-reference.md) for detailed method documentation
- Explore [Examples](examples.md) for more usage patterns
- Read [Advanced Usage](advanced.md) for production best practices
- Learn about [Development](development.md) if you want to contribute 