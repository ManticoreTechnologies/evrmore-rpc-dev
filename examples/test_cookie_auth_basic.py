#!/usr/bin/env python3
"""
Simple test script to verify the cookie authentication feature in the EvrmoreConfig class.
"""

from pathlib import Path
import tempfile
import os
from evrmore_rpc.config import EvrmoreConfig

def main():
    """Test the cookie authentication feature."""
    # Create a temporary directory for our test
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        print(f"Using temporary directory: {temp_path}")
        
        # Create a minimal config file without RPC credentials
        conf_path = temp_path / "evrmore.conf"
        with open(conf_path, "w") as f:
            f.write("rpcport=9999\n")
            f.write("server=1\n")
        
        print(f"Created config file at: {conf_path}")
        
        # Create a cookie file
        cookie_path = temp_path / ".cookie"
        with open(cookie_path, "w") as f:
            f.write("__cookie__:13f964606c1dcd54240b5ef9fcdf92a43c6a7abe02320a5129181978dc2624ad")
        
        print(f"Created cookie file at: {cookie_path}")
        
        # Create an EvrmoreConfig instance
        config = EvrmoreConfig(datadir=temp_path)
        
        # Test getting RPC credentials
        username, password = config.get_rpc_credentials()
        
        print("\n--- RPC Credentials ---")
        print(f"Username: {username}")
        if password:
            # Mask part of the password for security
            masked_pass = password[:8] + "..." + password[-8:]
            print(f"Password: {masked_pass}")
        else:
            print("Password: None")
            
        # Verify the results
        if username == "__cookie__" and password == "13f964606c1dcd54240b5ef9fcdf92a43c6a7abe02320a5129181978dc2624ad":
            print("\n✅ SUCCESS: Cookie authentication is working correctly!")
        else:
            print("\n❌ FAILURE: Cookie authentication is not working correctly.")
            
        # Now test with no cookie file
        os.remove(cookie_path)
        print(f"\nRemoved cookie file at: {cookie_path}")
        
        # Create a new config object
        config = EvrmoreConfig(datadir=temp_path)
        
        # Test getting RPC credentials with no cookie file
        username, password = config.get_rpc_credentials()
        
        print("\n--- RPC Credentials (No Cookie) ---")
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        # Verify the results
        if username is None and password is None:
            print("\n✅ SUCCESS: Correctly returned None when no credentials are available!")
        else:
            print("\n❌ FAILURE: Should return None when no credentials are available.")

if __name__ == "__main__":
    main() 