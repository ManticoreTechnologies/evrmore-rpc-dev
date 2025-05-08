# API Reference

This document provides a comprehensive reference for the `evrmore-rpc` Python package.

## Core Classes

### EvrmoreClient

The main client class for interacting with the Evrmore blockchain.

```python
from evrmore_rpc import EvrmoreClient

client = EvrmoreClient()
```

#### Configuration

```python
client = EvrmoreClient(
    url="http://localhost:8819",      # RPC URL
    rpcuser="user",                   # RPC username
    rpcpassword="pass",               # RPC password
    rpcport=8819,                     # RPC port
    testnet=True,                     # Use testnet
    timeout=30,                       # Request timeout
    async_mode=None                   # Auto-detect or force sync/async
)
```

#### Key Methods

##### Blockchain

```python
# Get blockchain info
info = client.getblockchaininfo()

# Get block by height
block_hash = client.getblockhash(height)
block = client.getblock(block_hash)

# Get mempool info
mempool = client.getmempoolinfo()
```

##### Assets

```python
# Get asset data
info = client.getassetdata("ASSET_NAME")

# Transfer asset
txid = client.transfer("ASSET_NAME", amount, "ADDRESS")

# Issue asset
txid = client.issue(
    "ASSET_NAME",
    qty=1000,
    to_address="ADDRESS",
    units=0,
    reissuable=True
)
```

##### Transactions

```python
# Get transaction
tx = client.getrawtransaction("TXID", True)

# Send transaction
txid = client.sendrawtransaction("HEX")

# Create transaction
raw_tx = client.createrawtransaction(
    [{"txid": "TXID", "vout": 0}],
    {"ADDRESS": 0.1}
)
```

##### Wallet

```python
# Get balance
balance = client.getbalance()

# Send to address
txid = client.sendtoaddress("ADDRESS", 0.1)

# Get new address
address = client.getnewaddress()
```

### EvrmoreZMQClient

Client for receiving real-time blockchain notifications via ZMQ.

```python
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

zmq = EvrmoreZMQClient(
    zmq_host="127.0.0.1",
    zmq_port=28332,
    topics=[ZMQTopic.BLOCK, ZMQTopic.TX],
    rpc_client=client,
    auto_decode=True
)
```

#### Event Handlers

```python
@zmq.on(ZMQTopic.BLOCK)
def handle_block(notification):
    print(f"Block #{notification.height}")

@zmq.on(ZMQTopic.TX)
def handle_tx(notification):
    print(f"TX {notification.tx['txid']}")
```

### EvrmoreWebSocketClient

Client for WebSocket-based blockchain notifications.

```python
from evrmore_rpc.websockets import EvrmoreWebSocketClient

ws = EvrmoreWebSocketClient(uri="ws://localhost:8765")
```

#### Usage

```python
async def main():
    await ws.connect()
    await ws.subscribe("blocks")
    
    async for message in ws:
        print(f"{message.type}: {message.data}")

asyncio.run(main())
```

## Data Models

All RPC responses are automatically parsed into Pydantic models for type safety and validation.

### Block Model

```python
class Block(BaseModel):
    hash: str
    height: int
    time: int
    size: int
    tx: List[str]
    # ... other fields
```

### Transaction Model

```python
class Transaction(BaseModel):
    txid: str
    size: int
    vsize: int
    version: int
    locktime: int
    vin: List[Vin]
    vout: List[Vout]
    # ... other fields
```

### Asset Model

```python
class Asset(BaseModel):
    name: str
    amount: int
    units: int
    reissuable: bool
    has_ipfs: bool
    ipfs_hash: Optional[str]
    # ... other fields
```

## Error Handling

The client raises specific exceptions for different error types:

```python
from evrmore_rpc import EvrmoreRPCError

try:
    client.getblockchaininfo()
except EvrmoreRPCError as e:
    print(f"RPC error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Optimization

### Connection Pooling

The client automatically uses connection pooling for better performance:

```python
# Create a client with custom pool size
client = EvrmoreClient(pool_size=10)

# The pool is automatically managed
info = client.getblockchaininfo()
```

### Batch Processing

For processing multiple blocks or transactions:

```python
async def process_blocks(start_height, end_height):
    async with EvrmoreClient() as client:
        for height in range(start_height, end_height):
            block_hash = await client.getblockhash(height)
            block = await client.getblock(block_hash)
            # Process block
```

## See Also

- [Getting Started](getting-started.md) for installation and basic usage
- [Examples](examples.md) for more code samples
- [Advanced Usage](advanced.md) for production patterns
- [Development](development.md) for contributing 