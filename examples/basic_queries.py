#!/usr/bin/env python3
"""
Basic Blockchain Queries Example

This example demonstrates how to use the evrmore-rpc library
to perform basic blockchain queries.
"""

from evrmore_rpc import EvrmoreClient

def main():
    # Create a client (auto-configures from evrmore.conf)
    print("Creating Evrmore RPC client...")
    client = EvrmoreClient()
    
    try:
        # Get basic blockchain information
        print("\n--- Blockchain Information ---")
        info = client.getblockchaininfo()
        print(f"Chain: {info['chain']}")
        print(f"Blocks: {info['blocks']}")
        print(f"Headers: {info['headers']}")
        print(f"Best Block Hash: {info['bestblockhash']}")
        print(f"Difficulty: {info['difficulty']}")
        print(f"Median Time: {info['mediantime']}")
        
        # Get network information
        print("\n--- Network Information ---")
        net_info = client.getnetworkinfo()
        print(f"Version: {net_info['version']}")
        print(f"Subversion: {net_info['subversion']}")
        print(f"Protocol Version: {net_info['protocolversion']}")
        print(f"Connections: {net_info['connections']}")
        
        # Get mining information
        print("\n--- Mining Information ---")
        mining_info = client.getmininginfo()
        print(f"Blocks: {mining_info['blocks']}")
        print(f"Current Block Size: {mining_info.get('currentblocksize', 'N/A')}")
        print(f"Current Block Weight: {mining_info.get('currentblockweight', 'N/A')}")
        print(f"Difficulty: {mining_info['difficulty']}")
        print(f"Network Hashps: {mining_info['networkhashps']}")
        print(f"Chain Hashps: {mining_info.get('chainhashps', 'N/A')}")
        
        # Get latest block details
        print("\n--- Latest Block Details ---")
        block_count = client.getblockcount()
        block_hash = client.getblockhash(block_count)
        block = client.getblock(block_hash)
        
        print(f"Block Height: {block_count}")
        print(f"Block Hash: {block['hash']}")
        print(f"Block Time: {block['time']}")
        print(f"Block Size: {block['size']} bytes")
        print(f"Block Weight: {block['weight']}")
        print(f"Transaction Count: {len(block['tx'])}")
        
        # Get mempool information
        print("\n--- Mempool Information ---")
        mempool_info = client.getmempoolinfo()
        print(f"Mempool Size: {mempool_info['size']} transactions")
        print(f"Mempool Bytes: {mempool_info['bytes']} bytes")
        print(f"Mempool Usage: {mempool_info['usage']} bytes")
        
        # Get wallet information (if available)
        print("\n--- Wallet Information ---")
        try:
            balance = client.getbalance()
            print(f"Wallet Balance: {balance} EVR")
            
            unconfirmed = client.getunconfirmedbalance()
            print(f"Unconfirmed Balance: {unconfirmed} EVR")
            
            # List transactions
            txs = client.listtransactions("*", 5)  # Last 5 transactions
            if txs:
                print("\nRecent Transactions:")
                for tx in txs:
                    print(f"  {tx['txid'][:8]}... : {tx['amount']} EVR ({tx['confirmations']} confirmations)")
        except Exception as e:
            print(f"Wallet information not available: {e}")
        
        # List available assets (Evrmore specific)
        print("\n--- Asset Information ---")
        try:
            assets = client.listassets()
            print(f"Total Assets: {len(assets)}")
            
            if len(assets) > 0:
                print("\nSample Assets:")
                # Handle both dictionary and list return types from listassets()
                if isinstance(assets, dict):
                    # Original code for dictionary response
                    sample_assets = list(assets.items())[:5]
                    for i, (asset_name, asset_data) in enumerate(sample_assets):
                        print(f"  {asset_name}: {asset_data['amount']} units")
                        
                        # Get detailed asset data
                        if i == 0:  # Just show details for the first asset
                            detail = client.getassetdata(asset_name)
                            print(f"    Owner: {detail.get('owner_address', 'N/A')}")
                            print(f"    Reissuable: {detail.get('reissuable', 'N/A')}")
                            print(f"    IPFS Hash: {detail.get('ipfs_hash', 'N/A')}")
                elif isinstance(assets, list):
                    # New code for list response
                    sample_assets = assets[:5]
                    for i, asset in enumerate(sample_assets):
                        # Extract asset name - either it's directly an asset name string
                        # or it has a 'name' field in a dictionary
                        if isinstance(asset, dict) and 'name' in asset:
                            asset_name = asset['name']
                            asset_data = asset
                        else:
                            asset_name = asset
                            # Get detailed asset data for display
                            try:
                                asset_data = client.getassetdata(asset_name)
                            except Exception:
                                asset_data = {'amount': 'Unknown'}
                        
                        # Display asset information
                        amount = asset_data.get('amount', 'Unknown')
                        print(f"  {asset_name}: {amount} units")
                        
                        # Get more detailed asset data for the first asset
                        if i == 0:
                            if isinstance(asset, dict) and 'name' in asset:
                                detail = client.getassetdata(asset_name)
                            else:
                                detail = asset_data
                                
                            print(f"    Owner: {detail.get('owner_address', 'N/A')}")
                            print(f"    Reissuable: {detail.get('reissuable', 'N/A')}")
                            print(f"    IPFS Hash: {detail.get('ipfs_hash', 'N/A')}")
                else:
                    print(f"  Unexpected assets format: {type(assets)}")
        except Exception as e:
            print(f"Asset information not available: {e}")
        
    finally:
        # Close the client
        print("\nClosing client...")
        client.close_sync()
        print("Done!")

if __name__ == "__main__":
    main() 