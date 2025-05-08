#!/usr/bin/env python3
"""
Evrmore Asset Operations Example

This example demonstrates how to work with Evrmore assets using the evrmore-rpc library.
It shows how to query asset information, issue new assets, manage assets, and more.
"""

from evrmore_rpc import EvrmoreClient
import json
import sys

def print_asset_info(asset_data):
    """Helper function to print asset info in a formatted way"""
    print(f"  Name: {asset_data.get('name', 'N/A')}")
    print(f"  Amount: {asset_data.get('amount', 'N/A')}")
    print(f"  Units: {asset_data.get('units', 'N/A')}")
    print(f"  Reissuable: {asset_data.get('reissuable', 'N/A')}")
    print(f"  Has IPFS: {asset_data.get('has_ipfs', 'N/A')}")
    if asset_data.get('ipfs_hash'):
        print(f"  IPFS Hash: {asset_data.get('ipfs_hash')}")
    if asset_data.get('owner_address'):
        print(f"  Owner: {asset_data.get('owner_address')}")
    print()

def main():
    print("Evrmore Asset Operations Example")
    print("--------------------------------")
    
    # Create a client
    print("Creating Evrmore RPC client...")
    client = EvrmoreClient()
    
    try:
        # Check if the node supports assets
        print("\nChecking wallet and asset support...")
        
        # We need to verify the wallet is available and supports assets
        try:
            wallet_info = client.getwalletinfo()
            print(f"Wallet is available with balance: {wallet_info.get('balance', 0)} EVR")
        except Exception as e:
            print(f"Error accessing wallet: {e}")
            print("This example requires a wallet to be loaded.")
            sys.exit(1)
        
        # Query list of assets to confirm asset support
        try:
            assets = client.listassets()
            print(f"Asset support confirmed! Found {len(assets)} assets.")
        except Exception as e:
            print(f"Error querying assets: {e}")
            print("This example requires a node with asset support.")
            sys.exit(1)
        
        # Get information about assets
        print("\n--- Asset Information ---")
        
        # Get the first few assets for demonstration
        sample_assets = []
        asset_names = []
        
        # Handle both dictionary and list return types
        if isinstance(assets, dict):
            # Original code for dictionary response
            sample_assets = list(assets.items())[:5]
            asset_names = [name for name, _ in sample_assets]
        elif isinstance(assets, list):
            # New code for list response
            sample_assets = assets[:5]
            # Extract asset names from the list
            asset_names = []
            for asset in sample_assets:
                if isinstance(asset, dict) and 'name' in asset:
                    asset_names.append(asset['name'])
                else:
                    asset_names.append(asset)
        else:
            print(f"Unexpected assets format: {type(assets)}")
            
        if asset_names:
            print(f"Showing {len(asset_names)} sample assets:")
            for i, asset_name in enumerate(asset_names):
                print(f"\nAsset: {asset_name}")
                
                # Get detailed asset data
                asset_data = client.getassetdata(asset_name)
                print_asset_info(asset_data)
        else:
            print("No assets found in the blockchain.")
        
        # Get addresses with asset balances
        print("\n--- Addresses With Asset Balances ---")
        try:
            # Choose the first asset for demonstration
            if asset_names:
                test_asset = asset_names[0]
                print(f"Checking addresses holding {test_asset}:")
                
                try:
                    addresses = client.getaddressesbyasset(test_asset)
                    if addresses:
                        print(f"Found {len(addresses)} addresses holding {test_asset}:")
                        for addr, amount in list(addresses.items())[:3]:  # Show first 3
                            print(f"  {addr}: {amount}")
                        if len(addresses) > 3:
                            print(f"  ... and {len(addresses) - 3} more addresses")
                    else:
                        print(f"No addresses found holding {test_asset}")
                except Exception as e:
                    print(f"Note: This node doesn't support the getaddressesbyasset method: {e}")
                    print("This feature requires an Evrmore node with address index enabled.")
            else:
                print("No assets available to check addresses")
        except Exception as e:
            print(f"Error getting addresses by asset: {e}")
        
        # Show asset balance for current wallet
        print("\n--- Wallet Asset Balances ---")
        try:
            try:
                balances = client.listassetbalancesbyaddress("*")
                if balances:
                    print("Asset balances in current wallet:")
                    for address, assets_held in list(balances.items())[:3]:  # Show first 3 addresses
                        print(f"\nAddress: {address}")
                        for asset_name, amount in assets_held.items():
                            print(f"  {asset_name}: {amount}")
                    
                    if len(balances) > 3:
                        print(f"... and {len(balances) - 3} more addresses")
                else:
                    print("No asset balances found in current wallet")
            except Exception as e:
                print(f"Note: This node doesn't support the listassetbalancesbyaddress method: {e}")
                print("This feature requires an Evrmore node with additional asset indexing.")
                
                # Try alternative approach with listmyassets if available
                try:
                    my_assets = client.listmyassets()
                    if my_assets:
                        print("Asset balances in current wallet (using listmyassets):")
                        for asset_name, data in list(my_assets.items())[:5]:  # Show first 5
                            print(f"  {asset_name}: {data.get('balance', 'Unknown')}")
                        if len(my_assets) > 5:
                            print(f"  ... and {len(my_assets) - 5} more assets")
                    else:
                        print("No asset balances found in current wallet")
                except Exception:
                    print("Alternative method listmyassets is also not available.")
        except Exception as e:
            print(f"Error getting wallet asset balances: {e}")
        
        # Show how to create a new asset (commented out to avoid actually creating one)
        print("\n--- Asset Creation Example (simulation) ---")
        print("To create a new asset, you would use:")
        print("""
client.issue(
    asset_name="MYASSET",
    qty=1000,
    to_address="<destination_address>",
    change_address="<change_address>",
    units=0,
    reissuable=True,
    has_ipfs=False
)
        """)
        print("This example does not actually create an asset.")
        
        # Show how to transfer an asset (commented out to avoid actual transfer)
        print("\n--- Asset Transfer Example (simulation) ---")
        print("To transfer an asset, you would use:")
        print("""
client.transfer(
    asset_name="MYASSET",
    qty=100,
    to_address="<destination_address>"
)
        """)
        print("This example does not actually transfer any assets.")
        
        # Show how to reissue an asset (commented out to avoid actual reissuance)
        print("\n--- Asset Reissuance Example (simulation) ---")
        print("To reissue an asset (increase supply), you would use:")
        print("""
client.reissue(
    asset_name="MYASSET",
    qty=500,
    to_address="<destination_address>",
    reissuable=True
)
        """)
        print("This example does not actually reissue any assets.")
    
    finally:
        # Close the client
        print("\nClosing client...")
        client.close_sync()
        print("Done!")

if __name__ == "__main__":
    main() 