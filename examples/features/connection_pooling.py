# examples/features/connection_pooling.py

"""
📌 Feature: Connection Pooling
------------------------------
This example demonstrates how `EvrmoreClient` reuses its internal connection/session
to avoid the overhead of creating a new connection per request.

✅ One connection reused across multiple calls
✅ Works for both sync and async modes
✅ Improves performance and resource usage
"""

# ─── Imports ──────────────────────────────────────────────
import asyncio
from evrmore_rpc import EvrmoreClient

# ─── Sync Example ─────────────────────────────────────────
def run_sync_example():
    print("\n🔁 Sync Connection Pooling Test")

    # Create a sync client (uses requests.Session internally)
    client = EvrmoreClient()

    # Perform multiple RPC calls — should reuse one HTTP connection
    for i in range(3):
        block_count = client.getblockcount()
        print(f"  [Sync] Call {i+1}: Block height = {block_count}")

    # Close session explicitly
    client.close_sync()

# ─── Async Example ────────────────────────────────────────
async def run_async_example():
    print("\n⚡ Async Connection Pooling Test")

    # Create an async client (uses aiohttp.ClientSession internally)
    client = EvrmoreClient()

    async with client:
        for i in range(3):
            block_count = await client.getblockcount()
            print(f"  [Async] Call {i+1}: Block height = {block_count}")

# ─── Entry Point ──────────────────────────────────────────
if __name__ == "__main__":
    run_sync_example()
    asyncio.run(run_async_example())

"""
🎯 Output Preview:

🔁 Sync Connection Pooling Test
  [Sync] Call 1: Block height = 1316459
  [Sync] Call 2: Block height = 1316459
  [Sync] Call 3: Block height = 1316459

⚡ Async Connection Pooling Test
  [Async] Call 1: Block height = 1316459
  [Async] Call 2: Block height = 1316459
  [Async] Call 3: Block height = 1316459

All requests reuse the same underlying session/socket, reducing latency and overhead.
"""
