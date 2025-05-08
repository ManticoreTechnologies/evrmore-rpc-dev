#!/usr/bin/env python3
"""
ZMQ Auto-Decoding Example

This example demonstrates how to use the ZMQ client with auto-decoding features
to receive and process real-time blockchain notifications with fully decoded
block and transaction data.
"""

import time
import datetime
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic

def main():
    print("Starting ZMQ Auto-Decoding Example")
    print("----------------------------------")
    print("This example will listen for new blocks and transactions")
    print("and automatically decode them using the RPC client.")
    print()
    
    # Create an RPC client for decoding
    print("Creating RPC client...")
    rpc = EvrmoreClient()
    
    # Create a ZMQ client with auto-decoding enabled
    print("Creating ZMQ client with auto-decoding...")
    zmq = EvrmoreZMQClient(
        zmq_host="127.0.0.1",
        zmq_port=28332,
        rpc_client=rpc,
        auto_decode=True,
        topics=[ZMQTopic.BLOCK, ZMQTopic.TX]  # Enhanced topics for auto-decoding
    )
    
    # Track statistics
    stats = {
        "blocks_received": 0,
        "transactions_received": 0,
        "asset_transactions": 0,
        "start_time": datetime.datetime.now(),
        "last_block_time": None,
        "last_tx_time": None
    }
    
    # Register handler for decoded blocks
    @zmq.on(ZMQTopic.BLOCK)
    def on_block(notification):
        """Handle fully decoded block notifications"""
        stats["blocks_received"] += 1
        stats["last_block_time"] = datetime.datetime.now()
        
        # Print block details
        print("\n" + "="*50)
        print(f"📦 NEW BLOCK RECEIVED at {stats['last_block_time']}")
        print(notification)  # Use enhanced __repr__ format
        print("="*50)
        
        # Print summary statistics
        display_stats()
    
    # Register handler for decoded transactions
    @zmq.on(ZMQTopic.TX)
    def on_transaction(notification):
        print(notification)
        """Handle fully decoded transaction notifications"""
        stats["transactions_received"] += 1
        stats["last_tx_time"] = datetime.datetime.now()
        
        # Check if this is an asset transaction
        if notification.has_assets:
            stats["asset_transactions"] += 1
            
            # Print detailed asset transaction information
            print("\n" + "*"*50)
            print(f"🪙 ASSET TRANSACTION DETECTED at {stats['last_tx_time']}")
            print(notification)  # Use enhanced __repr__ format
            
            # Display detailed asset information
            print("\nDetailed Asset Information:")
            for asset_info in notification.asset_info:
                print(f"  Asset: {asset_info['asset_name']}")
                print(f"  Type: {asset_info['type']}")
                print(f"  Amount: {asset_info['amount']}")
                if 'address' in asset_info:
                    print(f"  Address: {asset_info['address']}")
                print()
            print("*"*50)
        else:
            # Print basic transaction information
            tx_id = notification.hex  # Use hex instead of txid for compatibility
            print(f"\n💰 New transaction: {tx_id}")
    
    def display_stats():
        """Display current statistics"""
        runtime = datetime.datetime.now() - stats["start_time"]
        minutes = runtime.total_seconds() / 60
        
        txs_per_min = 0
        blocks_per_min = 0
        
        if minutes > 0:
            txs_per_min = stats["transactions_received"] / minutes
            blocks_per_min = stats["blocks_received"] / minutes
        
        print("\nStatistics:")
        print(f"  Runtime: {runtime}")
        print(f"  Blocks received: {stats['blocks_received']} ({blocks_per_min:.2f}/min)")
        print(f"  Transactions received: {stats['transactions_received']} ({txs_per_min:.2f}/min)")
        print(f"  Asset transactions: {stats['asset_transactions']}")
    
    # Start the ZMQ client
    print("\nStarting ZMQ client...")
    zmq.start()
    print("ZMQ client started successfully!")
    print("Listening for new blocks and transactions...")
    print("Press Ctrl+C to stop.")
    
    try:
        # Keep the program running
        while True:
            time.sleep(10)  # Sleep to avoid CPU consumption
            display_stats()
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Clean up
        print("Shutting down ZMQ client...")
        zmq.stop_sync()
        print("Shutting down RPC client...")
        rpc.close_sync()
        print("Done!")

if __name__ == "__main__":
    main() 