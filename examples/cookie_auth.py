#!/usr/bin/env python3
"""
Example script demonstrating cookie-based authentication with EvrmoreClient.

When running evrmored with -server but without specifying rpcuser and rpcpassword,
the daemon creates a .cookie file in the data directory that can be used for
authentication. This script demonstrates how to connect to an evrmored instance
using cookie-based authentication.

Prerequisites:
  - Evrmore daemon (evrmored) must be running with -server option
  - No rpcuser/rpcpassword set in evrmore.conf
"""

import logging
import sys
from pathlib import Path
from evrmore_rpc import EvrmoreClient, EvrmoreConfig, EvrmoreRPCError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

def print_separator():
    """Print a separator line for better readability."""
    print("-" * 60)

def main():
    """
    Main function demonstrating cookie-based authentication.
    """
    try:
        # First, examine the configuration to show the authentication method
        config = EvrmoreConfig()
        
        # Check if we're using cookie authentication
        rpcuser, rpcpassword = config.get_rpc_credentials()
        
        print_separator()
        print("Authentication information:")
        
        if config.get("rpcuser") and config.get("rpcpassword"):
            print(f"Using credentials from evrmore.conf")
            print(f"RPC User: {config.get('rpcuser')}")
            print(f"RPC Password: {'*' * len(config.get('rpcpassword'))}")
        else:
            print("No RPC credentials found in evrmore.conf")
            
            cookie_path = config._get_cookie_path()
            if cookie_path.exists():
                print(f"Using cookie authentication from {cookie_path}")
                print(f"Cookie User: {rpcuser}")
                print(f"Cookie Password: {'*' * 8}...{'*' * 8}")  # Mask the actual password
            else:
                print(f"Cookie file not found at {cookie_path}")
                print("No authentication method available")
                return
        
        print_separator()
        
        # Create a client and execute some commands
        client = EvrmoreClient()
        
        # Get blockchain info
        blockchain_info = client.getblockchaininfo()
        print("Blockchain Info:")
        print(f"Chain: {blockchain_info['chain']}")
        print(f"Blocks: {blockchain_info['blocks']}")
        print(f"Verification progress: {blockchain_info['verificationprogress']:.2%}")
        
        print_separator()
        
        # Get wallet info
        wallet_info = client.getwalletinfo()
        print("Wallet Info:")
        print(f"Wallet version: {wallet_info['walletversion']}")
        print(f"Balance: {wallet_info['balance']} EVR")
        print(f"Unconfirmed balance: {wallet_info['unconfirmed_balance']} EVR")
        
        print_separator()
        
        # Get network info
        network_info = client.getnetworkinfo()
        print("Network Info:")
        print(f"Version: {network_info['version']}")
        print(f"Subversion: {network_info['subversion']}")
        print(f"Protocol version: {network_info['protocolversion']}")
        
        print_separator()
        
    except EvrmoreRPCError as e:
        logger.error(f"RPC Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main() 