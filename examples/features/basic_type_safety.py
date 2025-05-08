"""
📌 Feature: Basic Type Safety
-----------------------------
This example highlights how `evrmore-rpc` uses type hints to guide development,
enable static checking, and improve editor support.

Although results are runtime `dict` objects, function signatures are explicitly typed.

🔎 Benefits:
- IDE autocomplete & tooltips
- Static analysis (mypy, pylance, etc.)
- Fewer runtime mistakes
"""

from evrmore_rpc import EvrmoreClient

client = EvrmoreClient()

# This is statically declared as a dict[str, any]
block_info: dict = client.getblockchaininfo()

# You get immediate editor help on what keys are available
print("⛓️ Blockchain Info:")
print(f"  🔹 Chain: {block_info['chain']}")
print(f"  🔹 Blocks: {block_info['blocks']}")
print(f"  🔹 Difficulty: {block_info['difficulty']}")

# If you try to access a non-existent field, your IDE or mypy will warn you
# Uncomment the line below to see the warning in a type checker:
# print(block_info['invalid_key'])  # ❌ Key error statically detectable!
