"""
evrmore-rpc: A comprehensive Python wrapper for Evrmore blockchain RPC

Copyright (c) 2025 Manticore Technologies
MIT License - See LICENSE file for details

Features:
- Polymorphic client that works identically in both synchronous and asynchronous contexts
- Automatic detection of execution context (sync/async) with seamless adaptation
- Comprehensive type hints and Pydantic models for strong type safety
- High-performance connection handling with both HTTP and ZMQ interfaces
- Complete coverage of all Evrmore RPC commands with proper parameter typing
- Structured response models with automatic validation
- Flexible configuration via constructor parameters, environment variables, or evrmore.conf
- ZMQ support for real-time blockchain notifications
- Built-in stress testing and performance analysis capabilities

For documentation and examples, visit:
https://github.com/manticore-tech/evrmore-rpc

For issues and contributions:
https://github.com/manticore-tech/evrmore-rpc/issues
"""

__version__ = "4.0.0"

# Client imports
from evrmore_rpc.client import EvrmoreClient, EvrmoreConfig, EvrmoreRPCError

# If users need model classes, they can import them directly from the models module
from evrmore_rpc.models import (
    BlockchainInfo,
    NetworkInfo,
    Block, 
    BlockHeader,
    AssetInfo
)

# Simple export list
__all__ = [
    "EvrmoreClient",
    "EvrmoreConfig",
    "EvrmoreRPCError",
    "BlockchainInfo",
    "NetworkInfo",
    "Block",
    "BlockHeader",
    "AssetInfo"
] 