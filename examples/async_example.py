#!/usr/bin/env python3
"""
Asynchronous Evrmore RPC Example

This example demonstrates how to use the evrmore-rpc library in an
asynchronous context, showcasing the seamless API that works in both
synchronous and asynchronous environments.
"""

import asyncio
from evrmore_rpc import EvrmoreClient
import time

async def get_block_details(client, height):
    """Get details for a specific block height"""
    try:
        # Get the block hash for the specified height
        block_hash = await client.getblockhash(height)
        
        # Get detailed block information using the hash
        block = await client.getblock(block_hash, 2)  # Verbosity 2 for full transaction data
        
        return {
            'height': height,
            'hash': block.get('hash', 'N/A'),
            'time': block.get('time', 0),
            'tx_count': len(block.get('tx', [])),
            'size': block.get('size', 0),
            'difficulty': block.get('difficulty', 0)
        }
    except Exception as e:
        print(f"Error getting block {height}: {e}")
        return None

async def get_latest_blocks(client, count=5):
    """Retrieve the latest blocks from the blockchain"""
    try:
        # Get the current block count
        current_height = await client.getblockcount()
        print(f"Current blockchain height: {current_height}")
        
        # Create tasks to fetch multiple blocks in parallel
        tasks = []
        for height in range(current_height, current_height - count, -1):
            if height < 0:
                break
            tasks.append(get_block_details(client, height))
        
        # Wait for all tasks to complete
        blocks = await asyncio.gather(*tasks)
        return [b for b in blocks if b is not None]
    
    except Exception as e:
        print(f"Error fetching latest blocks: {e}")
        return []

async def get_mempool_transactions(client, limit=5):
    """Get transactions currently in the mempool"""
    try:
        # Get transaction IDs from mempool
        tx_ids = await client.getrawmempool()
        print(f"Mempool size: {len(tx_ids)} transactions")
        
        # Limit the number of transactions to process
        tx_ids = tx_ids[:limit]
        
        # Create tasks to fetch transaction details in parallel
        tasks = []
        for tx_id in tx_ids:
            tasks.append(client.getrawtransaction(tx_id, 1))  # Verbose mode
        
        # Wait for all tasks to complete
        if tasks:
            transactions = await asyncio.gather(*tasks)
            return transactions
        return []
    
    except Exception as e:
        print(f"Error fetching mempool transactions: {e}")
        return []

async def wallet_operations(client):
    """Perform wallet-related operations if a wallet is available"""
    try:
        # Get wallet information
        wallet_info = await client.getwalletinfo()
        balance = wallet_info.get('balance', 0)
        print(f"Wallet found with balance: {balance} EVR")
        
        # Get recent transactions
        tx_list = await client.listtransactions("*", 5)  # Last 5 transactions
        print(f"Recent transactions: {len(tx_list)}")
        
        # Try to get addresses - using a more compatible approach
        # First try getaddressesbylabel (Bitcoin Core standard)
        address_count = 0
        try:
            addresses = await client.getaddressesbylabel("")
            address_count = len(addresses) if addresses else 0
        except Exception:
            # If that fails, try listaddressgroupings (more widely supported)
            try:
                address_groups = await client.listaddressgroupings()
                # Extract unique addresses from groups
                unique_addresses = set()
                for group in address_groups:
                    for addr_data in group:
                        if addr_data and len(addr_data) > 0:
                            unique_addresses.add(addr_data[0])  # First element is the address
                address_count = len(unique_addresses)
            except Exception:
                # If that also fails, try a simpler approach with listunspent
                try:
                    unspent = await client.listunspent()
                    unique_addresses = set(entry.get('address') for entry in unspent if 'address' in entry)
                    address_count = len(unique_addresses)
                except Exception:
                    address_count = 0
        
        print(f"Wallet has {address_count} addresses")
        
        # Return wallet summary
        return {
            'balance': balance,
            'transaction_count': len(tx_list),
            'address_count': address_count
        }
    
    except Exception as e:
        print(f"Wallet operations error or no wallet available: {e}")
        return None

async def main():
    """Main async function"""
    print("Asynchronous Evrmore RPC Example")
    print("--------------------------------")
    
    # Create a client - it will automatically work in async mode
    # when called with 'await'
    print("Creating Evrmore RPC client...")
    client = EvrmoreClient()
    
    try:
        # Get blockchain information
        print("\n--- Blockchain Information ---")
        start_time = time.time()
        info = await client.getblockchaininfo()
        print(f"Chain: {info.get('chain', 'unknown')}")
        print(f"Blocks: {info.get('blocks', 0)}")
        print(f"Headers: {info.get('headers', 0)}")
        print(f"Difficulty: {info.get('difficulty', 0)}")
        
        # Get the latest blocks in parallel
        print("\n--- Latest Blocks (Parallel Requests) ---")
        blocks = await get_latest_blocks(client, 5)
        for block in blocks:
            print(f"Block #{block['height']}: {block['hash'][:10]}... | " 
                  f"Tx Count: {block['tx_count']} | Size: {block['size']} bytes")
        
        # Get mempool transactions in parallel
        print("\n--- Mempool Transactions (Parallel Requests) ---")
        transactions = await get_mempool_transactions(client)
        for tx in transactions:
            print(f"Tx {tx.get('txid', 'unknown')[:10]}... | "
                  f"Size: {tx.get('size', 0)} bytes | "
                  f"Inputs: {len(tx.get('vin', []))}, Outputs: {len(tx.get('vout', []))}")
        
        # Perform wallet operations if available
        print("\n--- Wallet Operations ---")
        wallet_info = await wallet_operations(client)
        
        # Check total execution time
        execution_time = time.time() - start_time
        print(f"\nTotal execution time: {execution_time:.2f} seconds")
    
    except Exception as e:
        print(f"Error in main process: {e}")
    
    finally:
        # Close client connections
        print("\nClosing connections...")
        await client.close()
        print("Done!")

if __name__ == "__main__":
    # Run the async main function using asyncio
    asyncio.run(main()) 