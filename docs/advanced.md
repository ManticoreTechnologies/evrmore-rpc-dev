# Advanced Usage Guide

This guide covers advanced features and production patterns for the `evrmore-rpc` package.

## Connection Management

### Connection Pooling

```python
from evrmore_rpc import EvrmoreClient, ConnectionPool

# Create connection pool
pool = ConnectionPool(
    host="127.0.0.1",
    port=8332,
    username="rpcuser",
    password="rpcpass",
    max_connections=10,
    timeout=30
)

# Get client from pool
client = pool.get_client()

try:
    # Use client
    result = client.getblockchaininfo()
finally:
    # Always return client to pool
    pool.return_client(client)
```

### Context Managers

```python
# Using context manager
with pool.get_client() as client:
    result = client.getblockchaininfo()

# Custom context manager
class EvrmoreContext:
    def __init__(self, host="127.0.0.1", port=8332):
        self.client = EvrmoreClient(host=host, port=port)
        
    def __enter__(self):
        return self.client
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

# Usage
with EvrmoreContext() as client:
    result = client.getblockchaininfo()
```

## Performance Optimization

### Batch Processing

```python
def process_blocks(start_height, end_height, batch_size=100):
    for i in range(start_height, end_height + 1, batch_size):
        batch_end = min(i + batch_size, end_height + 1)
        blocks = []
        
        for height in range(i, batch_end):
            block = client.getblock(height)
            blocks.append(block)
            
        # Process batch
        process_block_batch(blocks)

def process_block_batch(blocks):
    for block in blocks:
        # Process block data
        pass
```

### Caching

```python
from functools import lru_cache
import time

class CachedEvrmoreClient:
    def __init__(self, client):
        self.client = client
        self.block_cache = {}
        self.tx_cache = {}
        
    @lru_cache(maxsize=1000)
    def get_block(self, height):
        return self.client.getblock(height)
        
    @lru_cache(maxsize=10000)
    def get_transaction(self, txid):
        return self.client.getrawtransaction(txid, True)
        
    def clear_cache(self):
        self.get_block.cache_clear()
        self.get_transaction.cache_clear()
```

## Error Handling

### Custom Error Classes

```python
from evrmore_rpc import EvrmoreRPCError

class EvrmoreClientError(Exception):
    """Base class for Evrmore client errors"""
    pass

class BlockNotFoundError(EvrmoreClientError):
    """Raised when a block is not found"""
    pass

class TransactionNotFoundError(EvrmoreClientError):
    """Raised when a transaction is not found"""
    pass

def get_block_safe(height):
    try:
        return client.getblock(height)
    except EvrmoreRPCError as e:
        if "Block not found" in str(e):
            raise BlockNotFoundError(f"Block at height {height} not found")
        raise
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def get_block_with_retry(height):
    return client.getblock(height)
```

## Real-Time Processing

### ZMQ Integration

```python
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

class BlockchainProcessor:
    def __init__(self):
        self.zmq = EvrmoreZMQClient()
        self.rpc = EvrmoreClient()
        self.blocks_processed = 0
        self.transactions_processed = 0
        
    def start(self):
        # Register handlers
        self.zmq.on_block(self.handle_block)
        self.zmq.on_transaction(self.handle_transaction)
        
        # Start ZMQ client
        self.zmq.start()
        
    def handle_block(self, notification):
        block = self.rpc.getblock(notification.hex)
        self.blocks_processed += 1
        
        # Process block
        self.process_block(block)
        
    def handle_transaction(self, notification):
        tx = self.rpc.getrawtransaction(notification.hex, True)
        self.transactions_processed += 1
        
        # Process transaction
        self.process_transaction(tx)
```

### WebSocket Integration

```python
from evrmore_rpc.websocket import EvrmoreWebSocketClient, WebSocketTopic

class BlockchainMonitor:
    def __init__(self):
        self.ws = EvrmoreWebSocketClient()
        self.rpc = EvrmoreClient()
        self.blocks_processed = 0
        self.transactions_processed = 0
        
    async def start(self):
        # Register handlers
        self.ws.on_block(self.handle_block)
        self.ws.on_transaction(self.handle_transaction)
        
        # Start WebSocket client
        await self.ws.start()
        
    async def handle_block(self, notification):
        block = self.rpc.getblock(notification.hash)
        self.blocks_processed += 1
        
        # Process block
        await self.process_block(block)
        
    async def handle_transaction(self, notification):
        tx = self.rpc.getrawtransaction(notification.txid, True)
        self.transactions_processed += 1
        
        # Process transaction
        await self.process_transaction(tx)
```

## Asset Management

### Asset Tracking

```python
class AssetTracker:
    def __init__(self):
        self.client = EvrmoreClient()
        self.assets = {}
        
    def track_asset(self, asset_name):
        # Get asset info
        asset = self.client.getassetinfo(asset_name)
        self.assets[asset_name] = {
            "name": asset.name,
            "amount": asset.amount,
            "units": asset.units,
            "reissuable": asset.reissuable,
            "transfers": []
        }
        
    def get_asset_transfers(self, asset_name, start_block=0):
        if asset_name not in self.assets:
            self.track_asset(asset_name)
            
        current_height = self.client.getblockcount()
        
        for height in range(start_block, current_height + 1):
            block = self.client.getblock(height)
            
            for txid in block.tx:
                tx = self.client.getrawtransaction(txid, True)
                
                for vout in tx.vout:
                    if "asset" in vout.get("scriptPubKey", {}).get("asset", {}):
                        asset = vout["scriptPubKey"]["asset"]
                        if asset["name"] == asset_name:
                            self.assets[asset_name]["transfers"].append({
                                "txid": txid,
                                "amount": asset["amount"],
                                "block": height,
                                "time": block.time
                            })
```

### Asset Issuance

```python
class AssetIssuer:
    def __init__(self):
        self.client = EvrmoreClient()
        
    def issue_asset(self, name, amount, units=0, reissuable=True, ipfs_hash=None):
        # Issue new asset
        txid = self.client.issueasset(
            name=name,
            amount=amount,
            units=units,
            reissuable=reissuable,
            ipfs_hash=ipfs_hash
        )
        
        # Wait for confirmation
        self.wait_for_confirmation(txid)
        
        return txid
        
    def reissue_asset(self, name, amount, ipfs_hash=None):
        # Reissue existing asset
        txid = self.client.reissueasset(
            name=name,
            amount=amount,
            ipfs_hash=ipfs_hash
        )
        
        # Wait for confirmation
        self.wait_for_confirmation(txid)
        
        return txid
        
    def wait_for_confirmation(self, txid, confirmations=1):
        while True:
            tx = self.client.getrawtransaction(txid, True)
            if tx.confirmations >= confirmations:
                break
            time.sleep(1)
```

## Production Patterns

### Logging

```python
import logging

class EvrmoreLogger:
    def __init__(self):
        self.logger = logging.getLogger("evrmore")
        self.logger.setLevel(logging.INFO)
        
        # Add handlers
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_block(self, block):
        self.logger.info(f"Processing block {block.height}")
        
    def log_transaction(self, tx):
        self.logger.info(f"Processing transaction {tx.txid}")
        
    def log_error(self, error):
        self.logger.error(f"Error: {error}")
```

### Metrics Collection

```python
from prometheus_client import Counter, Gauge, start_http_server

class EvrmoreMetrics:
    def __init__(self):
        # Counters
        self.blocks_processed = Counter(
            'evrmore_blocks_processed_total',
            'Total number of blocks processed'
        )
        self.transactions_processed = Counter(
            'evrmore_transactions_processed_total',
            'Total number of transactions processed'
        )
        
        # Gauges
        self.current_height = Gauge(
            'evrmore_current_height',
            'Current blockchain height'
        )
        self.connection_status = Gauge(
            'evrmore_connection_status',
            'Connection status (1=connected, 0=disconnected)'
        )
        
    def start_server(self, port=8000):
        start_http_server(port)
        
    def update_metrics(self, client):
        info = client.getblockchaininfo()
        self.current_height.set(info.blocks)
        self.connection_status.set(1)
```

### Health Checks

```python
class EvrmoreHealth:
    def __init__(self):
        self.client = EvrmoreClient()
        self.last_check = 0
        self.check_interval = 60  # seconds
        
    def is_healthy(self):
        current_time = time.time()
        if current_time - self.last_check < self.check_interval:
            return True
            
        try:
            # Check connection
            self.client.getblockchaininfo()
            self.last_check = current_time
            return True
        except Exception as e:
            return False
            
    def get_status(self):
        try:
            info = self.client.getblockchaininfo()
            return {
                "status": "healthy",
                "blocks": info.blocks,
                "headers": info.headers,
                "verification_progress": info.verificationprogress
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
```

## See Also

- [Getting Started](getting-started.md) for basic usage
- [API Reference](api-reference.md) for detailed API docs
- [Examples](examples.md) for code samples
- [ZMQ Guide](zmq.md) for real-time notifications
- [WebSocket Guide](websockets.md) for WebSocket integration 