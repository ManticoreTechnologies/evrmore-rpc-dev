# Installation Guide for evrmore-rpc

This guide provides detailed instructions for installing the evrmore-rpc Python library for interacting with Evrmore blockchain nodes.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Evrmore node (if you plan to interact with the blockchain locally)

## Basic Installation

You can install the evrmore-rpc library using pip:

```bash
pip install evrmore-rpc
```

This will install the core functionality without ZMQ support.

## Installation with ZMQ Support

If you want to use ZMQ for real-time blockchain notifications, install with the `zmq` extra:

```bash
pip install evrmore-rpc[zmq]
```

## Development Installation

For development purposes, you can install all dependencies including testing tools:

```bash
pip install evrmore-rpc[all]
```

Or clone the repository and install in development mode:

```bash
git clone https://github.com/manticore-tech/evrmore-rpc.git
cd evrmore-rpc
pip install -e .[all]
```

## Evrmore Node Setup

To use this library, you'll need access to an Evrmore node. You can:

1. Run your own node (recommended for production)
2. Use a public node (for testing only)

### Running Your Own Evrmore Node

1. Download the Evrmore Core client from the [official repository](https://github.com/EvrmoreOrg/Evrmore/releases)
2. Install and set up the client according to the instructions
3. Configure the `evrmore.conf` file with RPC credentials:

```
# Basic RPC configuration
rpcuser=your_username
rpcpassword=your_secure_password
rpcallowip=127.0.0.1
server=1

# For ZMQ support (optional)
zmqpubhashtx=tcp://127.0.0.1:28332
zmqpubhashblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28332
zmqpubrawblock=tcp://127.0.0.1:28332
```

4. Start the Evrmore node:

```bash
# Start the daemon
evrmored

# Or with specific options
evrmored -rpcuser=your_username -rpcpassword=your_secure_password -server
```

## Verifying Installation

You can verify that the library is installed correctly by running a simple script:

```python
from evrmore_rpc import EvrmoreClient

# Create a client
client = EvrmoreClient()

# Get blockchain info
try:
    info = client.getblockchaininfo()
    print(f"Connected to Evrmore node. Chain: {info['chain']}, Blocks: {info['blocks']}")
    client.close_sync()
except Exception as e:
    print(f"Error connecting to Evrmore node: {e}")
```

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. **Check RPC Credentials**: Ensure your username and password match those in `evrmore.conf`
2. **Check Node Status**: Verify that your Evrmore node is running
3. **Check Firewall Settings**: Make sure appropriate ports are open
4. **Check Network Settings**: For remote nodes, ensure your IP is allowed in `rpcallowip`

### ZMQ Issues

For ZMQ-related issues:

1. **Verify ZMQ Configuration**: Check that ZMQ is properly configured in `evrmore.conf`
2. **Check ZMQ Dependencies**: Ensure pyzmq is installed with `pip install pyzmq`
3. **Check Port Availability**: Make sure the ZMQ ports (default: 28332) are available

## Advanced Configuration

### Environment Variables

The library supports configuration via environment variables:

```bash
export EVR_RPC_USER=your_username
export EVR_RPC_PASSWORD=your_secure_password
export EVR_RPC_HOST=localhost
export EVR_RPC_PORT=8819  # Default Evrmore RPC port
export EVR_TESTNET=0      # Set to 1 for testnet
```

### Custom Data Directory

You can specify a custom data directory when creating the client:

```python
from evrmore_rpc import EvrmoreClient

client = EvrmoreClient(datadir="/path/to/custom/directory")
```

## Next Steps

After installation, check out the [examples directory](./examples/) for sample code demonstrating various features of the library. 