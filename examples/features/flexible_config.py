# examples/features/flexible_config.py

"""
📌 Feature: Flexible Configuration
---------------------------------
This example demonstrates the various ways you can configure the EvrmoreClient:

1. Configuration from `evrmore.conf`
2. Environment variables (`EVR_RPC_*`)
3. Manual parameters (explicit URL/user/pass)
4. Testnet auto-setup

Each method creates a working EvrmoreClient and queries the current block count.

✅ Useful for:
- Environments with `.cookie` or local node setup
- Docker/container workflows using env vars
- Hardcoded configs in CLI tools or apps
"""

import os
from evrmore_rpc import EvrmoreClient

# ─── Using evrmore.conf (default) ───────────────────────────
print("🔧 Config: Default (evrmore.conf or ~/.evrmore)")
client = EvrmoreClient()
print("  → Block height:", client.getblockcount())
client.close_sync()

# ─── Using environment variables ────────────────────────────
print("\n🔧 Config: Environment Variables")
os.environ["EVR_RPC_USER"] = "evruser"
os.environ["EVR_RPC_PASSWORD"] = "changeThisToAStrongPassword123"
os.environ["EVR_RPC_HOST"] = "tcp://77.90.40.55"
os.environ["EVR_RPC_PORT"] = "8819"

client = EvrmoreClient()
print("  → Block height:", client.getblockcount())
client.close_sync()

# ─── Using manual parameters ────────────────────────────────
print("\n🔧 Config: Manual Parameters")
client = EvrmoreClient(
    rpcuser="evruser",
    rpcpassword="changeThisToAStrongPassword123",
    url="http://77.90.40.55:8819"
)
print("  → Block height:", client.getblockcount())
client.close_sync()

# ─── Testnet mode ───────────────────────────────────────────
print("\n🔧 Config: Testnet Mode")
client = EvrmoreClient(testnet=True)
print("  → Block height (testnet):", client.getblockcount())
client.close_sync()

"""
📦 Summary:
This demonstrates all supported config options:
- 🔁 Auto-loaded conf file
- 🌍 Environment-driven
- ✍️ Manual overrides
- 🧪 Testnet toggle

This makes EvrmoreClient usable in dev, test, prod, and containerized environments without changing code.
"""
