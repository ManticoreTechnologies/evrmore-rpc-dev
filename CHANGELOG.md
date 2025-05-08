# Changelog
## 3.2.4 (2025-03-26)

### Added
- Added support for cookie-based authentication when RPC credentials are not specified in evrmore.conf
- Added examples for cookie authentication usage



## 3.2.3 (2024-03-10)

### Fixed
- Fixed compatibility issues with `listassets()` method to handle both dictionary and list return types
- Improved examples to work with different Evrmore node versions
- Enhanced wallet address handling in async examples to support multiple RPC methods
- Fixed ZMQ auto-decode example to handle transaction notification attributes properly

### Changed
- Updated all example scripts to be more robust and handle different response formats
- Improved error handling in asset operation examples
- Enhanced documentation with clearer installation instructions

## Unreleased

### Added
- Comprehensive ZMQ notification examples
- Detailed documentation for ZMQ usage patterns
- Best practices for using RPC client with ZMQ
- Support for cookie-based authentication when RPC credentials are not specified in evrmore.conf
- Example script demonstrating cookie authentication usage

### Fixed
- Critical bug in ZMQ examples where RPC client wasn't correctly used in async context
- ZMQ handlers now properly use `force_async()` to ensure correct async operation

### Changed
- Improved ZMQ client documentation with focus on correct async usage
- Enhanced error handling in ZMQ notification handlers
- Updated ZMQ examples to demonstrate proper resource management
- Enhanced EvrmoreConfig class to automatically detect and use .cookie file for authentication

## 3.2.1 (2024-05-15)

### Added
- Seamless API that works in both synchronous and asynchronous contexts without context managers
- `reset()` method to reset client state when switching between sync and async contexts
- `force_sync()` and `force_async()` methods to explicitly set the mode
- Improved resource management with `__del__` method and explicit `close()` methods
- New examples demonstrating the seamless API
- Comprehensive test suite for all components
- Fixed test suite for EvrmoreClient and EvrmoreConfig classes
- Improved async test mocking
- Enhanced publication check script

### Changed
- Simplified codebase by consolidating functionality into a single client class
- Improved auto-detection of execution context
- Updated documentation to focus on the seamless API
- Streamlined examples to demonstrate best practices
- Improved resource management in client implementations
- Better error handling in configuration parsing

### Removed
- Deprecated client implementations
- Unnecessary command modules
- Redundant examples

## 3.1.0 (2024-02-15)

### Added
- Auto-detection of execution context
- Support for both synchronous and asynchronous usage
- Comprehensive type annotations
- Pydantic models for common RPC responses
- Integrated stress testing tools
- Seamless API for both sync and async usage without context managers
- Improved connection pooling
- Stress testing tools

### Changed
- Improved error handling
- Enhanced documentation
- Optimized performance
- Simplified client usage pattern
- Better error handling

## 3.0.0 (2024-01-01)

### Added
- Initial release of the rewritten evrmore-rpc library
- Support for all Evrmore RPC commands
- Asynchronous API
- Automatic configuration from evrmore.conf
- Connection pooling
- Type hints

## [2.0.0] - 2025-01-01

### Major Changes

- **Async-Only Architecture**: Completely redesigned the library to be async-only for maximum performance
- **Simplified Codebase**: Removed all synchronous code for a smaller, more focused library
- **Enhanced Concurrency**: Improved concurrency handling for better performance
- **Reduced Dependencies**: Removed requests dependency, now only requires aiohttp

### Added

- Improved error handling for async operations
- Better connection pooling for persistent connections
- Enhanced concurrency control in stress testing

### Removed

- All synchronous code and clients
- Requests dependency

## [1.4.0] - 2024-12-15

### Added

- Modular architecture with base client class
- Command factory for generating command wrappers
- Unified response handling
- Improved type hints

### Changed

- Refactored direct and async clients to inherit from base client
- Updated blockchain commands to use command factory
- Enhanced documentation with architecture details

## [1.3.0] - 2024-11-30

### Added

- WebSockets support for real-time blockchain notifications
- WebSocket server for proxying blockchain events
- Additional examples for WebSockets usage

### Changed

- Improved ZMQ client with better error handling
- Enhanced documentation with WebSockets examples

## [1.2.0] - 2024-10-15

### Added

- ZMQ support for subscribing to blockchain events
- Examples for ZMQ usage
- Performance comparison examples

### Changed

- Improved error handling in direct clients
- Enhanced documentation with ZMQ examples

## [1.1.0] - 2024-09-01

### Added

- Direct RPC clients for better performance
- Asynchronous support for concurrent operations
- Configuration management with automatic parsing of evrmore.conf
- Comprehensive examples directory

### Changed

- Improved error handling
- Enhanced documentation

## [1.0.0] - 2024-08-01

### Added

- Initial release with CLI-based client
- Support for all Evrmore RPC commands
- Basic documentation 