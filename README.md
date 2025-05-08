# evrmore-rpc: Python Client for Evrmore Blockchain

[![PyPI version](https://badge.fury.io/py/evrmore-rpc.svg)](https://badge.fury.io/py/evrmore-rpc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/evrmore-rpc.svg)](https://pypi.org/project/evrmore-rpc/)

A comprehensive Python client for interacting with Evrmore blockchain nodes through JSON-RPC and ZMQ interfaces, with features optimized for efficient blockchain application development.

## Features

- **Seamless Execution Context**: Works identically in both synchronous and asynchronous contexts
- **Auto-Detection**: Automatically detects execution context (sync/async) and adapts accordingly
- **Type Safety**: Comprehensive type hints and structured data models
- **Performance**: Optimized connection handling with connection pooling
- **Complete Coverage**: Support for all Evrmore RPC commands
- **Asset Support**: Special handling for Evrmore asset operations
- **ZMQ Integration**: Real-time blockchain notifications via ZMQ
- **Auto-Decoding**: Enhanced ZMQ topics with automatic transaction and block decoding
- **Asset Detection**: Automatic detection and detailed information for asset transactions
- **Flexible Configuration**: Configure via parameters, environment variables, or evrmore.conf

## Installation

```bash
# Basic installation
pip install evrmore-rpc

# With ZMQ support
pip install evrmore-rpc[zmq]
```

## Quick Start

```python
from evrmore_rpc import EvrmoreClient

# Create a client (auto-configures from evrmore.conf)
client = EvrmoreClient()

# Get blockchain info
info = client.getblockchaininfo()
print(f"Current block height: {info['blocks']}")
print(f"Current difficulty: {info['difficulty']}")

# Get a specific block
block_hash = client.getblockhash(1)
block = client.getblock(block_hash)
print(f"Block #1 hash: {block['hash']}")
print(f"Block #1 time: {block['time']}")

# Get wallet balance
balance = client.getbalance()
print(f"Wallet balance: {balance} EVR")
```

## Asynchronous Usage

The same client works seamlessly in asynchronous contexts:

```python
import asyncio
from evrmore_rpc import EvrmoreClient

async def main():
    # Create a client
    client = EvrmoreClient()

    # Use with await
    info = await client.getblockchaininfo()
    print(f"Current block height: {info['blocks']}")
    
    # When done
    await client.close()

asyncio.run(main())
```

## Client Configuration

The client can be configured in several ways:

```python
# Explicit configuration
client = EvrmoreClient(
    url="http://localhost:8819",
    rpcuser="username",
    rpcpassword="password"
)

# From environment variables
# Set EVR_RPC_USER, EVR_RPC_PASSWORD, EVR_RPC_HOST, EVR_RPC_PORT
client = EvrmoreClient()

# From evrmore.conf
client = EvrmoreClient(datadir="/path/to/evrmore/data/dir")

# Testnet configuration
client = EvrmoreClient(testnet=True)
```

## Authentication Methods

The client supports multiple authentication methods:

### Configuration File

The most common method is to specify credentials in `evrmore.conf`:

```
rpcuser=username
rpcpassword=password
```

### Cookie Authentication

If RPC credentials are not set in `evrmore.conf`, the client will automatically look for the `.cookie` file in the Evrmore data directory. This is useful when running Evrmore with the `-server` flag but without explicit RPC credentials.

The `.cookie` file contains authentication information in the format `__cookie__:HASH`. The client will use this to authenticate with the RPC server.

```python
# This will work even without rpcuser/rpcpassword in evrmore.conf
# as long as the .cookie file exists in the data directory
client = EvrmoreClient()
```

### Direct Specification

You can also provide credentials directly when creating the client:

```python
client = EvrmoreClient(rpcuser="username", rpcpassword="password")
```

## Working with Assets

Evrmore's unique asset functionality is fully supported:

```python
# List all assets
assets = client.listassets()

# Get asset data
asset_info = client.getassetdata("ASSET_NAME")
print(f"Asset supply: {asset_info['amount']}")
print(f"Reissuable: {asset_info['reissuable']}")

# Transfer an asset
tx_id = client.transfer(
    asset_name="ASSET_NAME",
    qty=10.0,
    to_address="EVRAddress"
)
```

## ZMQ Notifications

Real-time blockchain monitoring with ZMQ:

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Create RPC client for decoding
rpc = EvrmoreClient()

# Create ZMQ client
zmq = EvrmoreZMQClient(
    zmq_host="127.0.0.1", 
    zmq_port=28332,
    rpc_client=rpc
)

# Register handlers with decorators
@zmq.on(ZMQTopic.HASH_BLOCK)
def on_block(notification):
    print(f"New block: {notification.hex}")
    
@zmq.on(ZMQTopic.HASH_TX)
def on_tx(notification):
    print(f"New transaction: {notification.hex}")

# Register for enhanced topics with auto-decoding
@zmq.on(ZMQTopic.BLOCK)
def on_decoded_block(notification):
    print(f"Block at height {notification.height} with {notification._tx_count} transactions")

@zmq.on(ZMQTopic.TX)
def on_decoded_tx(notification):
    print(f"Transaction with {notification._vin_count} inputs and {notification._vout_count} outputs")
    if notification.has_assets:
        print(f"Contains asset operations: {notification.asset_info}")

# Start the client
zmq.start()
```

## Asset Transaction Detection

Automatic detection of asset transactions:

```python
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

# Create clients
rpc = EvrmoreClient()
zmq = EvrmoreZMQClient(rpc_client=rpc, topics=[ZMQTopic.TX])

# Register for asset transactions
@zmq.on(ZMQTopic.TX)
def on_transaction(notification):
    if notification.has_assets:
        print(f"Asset transaction detected: {notification.hex}")
        
        for asset_info in notification.asset_info:
            print(f"Asset: {asset_info['asset_name']}")
            print(f"Type: {asset_info['type']}")
            print(f"Amount: {asset_info['amount']}")
            print(f"Address: {asset_info['address']}")
            
            # Access enhanced asset information
            if 'asset_details' in asset_info:
                details = asset_info['asset_details'] 
                print(f"Total supply: {details['amount']}")

# Start the client
zmq.start()
```

## Handling Connection Management

For efficient resource usage, you should close connections when done:

```python
# Synchronous cleanup
client.close_sync()

# Asynchronous cleanup
await client.close()
```

## Advanced Usage

For more advanced usage, please refer to the examples directory and API documentation.

## Requirements

- Python 3.8+
- Evrmore node (with RPC and optionally ZMQ enabled)

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request