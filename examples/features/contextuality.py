# examples/features/contextuality.py

"""
📌 Feature: Contextuality
-------------------------
This example demonstrates how the EvrmoreClient adapts seamlessly to both
synchronous and asynchronous execution contexts.

You can use the same client interface in regular (sync) scripts or async
coroutines — no need to instantiate different classes or switch APIs.

This is ideal for:
- building apps that use both sync and async logic (e.g., CLI + event loop)
- transitioning from sync to async without refactoring
- libraries that want to be agnostic of the caller's context

✅ No wrappers
✅ No separate client classes
✅ One consistent API surface

© 2025 Manticore Technologies, LLC
Maintained by: Cymos (EfletL7gMLYkuu9CfHcRevVk3KdnG5JgruSE)
"""

# ─── Imports ──────────────────────────────────────────────
from evrmore_rpc import EvrmoreClient
import asyncio

# ─── Synchronous Usage ────────────────────────────────────
# Create a standard EvrmoreClient (defaults to loading from evrmore.conf)
sync_client = EvrmoreClient()

# Use the client in a blocking (synchronous) way
print("🧠 Synchronous context:")
block_height = sync_client.getblockcount()
print(f"  🔹 Current block height: {block_height}")

# ─── Asynchronous Usage ───────────────────────────────────
# The exact same EvrmoreClient works in an async coroutine
async def async_method():
    async_client = EvrmoreClient()

    print("⚡ Asynchronous context:")
    async_block_height = await async_client.getblockcount()
    print(f"  🔹 Current block height: {async_block_height}")

# Run the async example
asyncio.run(async_method())

"""
🎯 Output:
🧠 Synchronous context:
  🔹 Current block height: 1316428
⚡ Asynchronous context:
  🔹 Current block height: 1316428

The sync and async calls use the same internal RPC adapter,
but the client detects your context at call-time and adapts accordingly.
"""
