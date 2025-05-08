#!/usr/bin/env python3
"""
Tests for the EvrmoreConfig class.
"""

import os
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path

# Import directly from client.py since that's where it's defined in __init__.py
from evrmore_rpc.client import EvrmoreConfig

class TestEvrmoreConfig:
    """Tests for the EvrmoreConfig class."""
    
    def test_init_default(self):
        """Test default initialization."""
        with patch('evrmore_rpc.client.DEFAULT_DATADIR', Path('/home/user/.evrmore')):
            config = EvrmoreConfig()
            assert config.datadir == Path('/home/user/.evrmore')
            assert config.testnet is False
    
    def test_init_custom_datadir(self):
        """Test initialization with custom datadir."""
        config = EvrmoreConfig(datadir='/custom/path')
        assert config.datadir == Path('/custom/path')
        assert config.testnet is False
    
    def test_init_testnet(self):
        """Test initialization with testnet."""
        with patch('evrmore_rpc.client.DEFAULT_DATADIR', Path('/home/user/.evrmore')):
            config = EvrmoreConfig(testnet=True)
            assert config.datadir == Path('/home/user/.evrmore')
            assert config.testnet is True
    
    def test_load_config_file_not_found(self):
        """Test loading config when file not found."""
        with patch('pathlib.Path.exists', return_value=False):
            config = EvrmoreConfig()
            # Test get method with default
            assert config.get('rpcuser') is None
            assert config.get('rpcport', 8819) == 8819
    
    def test_load_config_file_found(self):
        """Test loading config when file is found."""
        mock_config_content = """
        rpcuser=testuser
        rpcpassword=testpass
        rpcport=9999
        """
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=mock_config_content)):
                config = EvrmoreConfig()
                assert config.get('rpcuser') == 'testuser'
                assert config.get('rpcpassword') == 'testpass'
                assert config.get('rpcport') == 9999
    
    def test_get_rpc_connection_info(self):
        """Test getting RPC connection info."""
        with patch('pathlib.Path.exists', return_value=False):
            # Test mainnet default
            config = EvrmoreConfig()
            host, port = config.get_rpc_connection_info()
            assert host == '127.0.0.1'
            assert port == 8819
            
            # Test testnet default
            config = EvrmoreConfig(testnet=True)
            host, port = config.get_rpc_connection_info()
            assert host == '127.0.0.1'
            assert port == 18819
    
    def test_get_rpc_credentials_from_config(self):
        """Test getting RPC credentials from config file."""
        mock_config_content = """
        rpcuser=testuser
        rpcpassword=testpass
        """
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=mock_config_content)):
                config = EvrmoreConfig()
                username, password = config.get_rpc_credentials()
                assert username == 'testuser'
                assert password == 'testpass'
    
    def test_get_rpc_credentials_from_cookie(self):
        mock_config_content = "rpcport=8819"
        mock_cookie_content = "__cookie__:13f964606c1dcd54240b5ef9fcdf92a43c6a7abe02320a5129181978dc2624ad"

        def path_exists_side_effect(*args, **kwargs):
            path = str(args[0]) if args else ""
            return path.endswith("evrmore.conf") or path.endswith(".cookie")

        file_mocks = {
            'evrmore.conf': mock_open(read_data=mock_config_content),
            '.cookie': mock_open(read_data=mock_cookie_content)
        }

        def open_side_effect(*args, **kwargs):
            path = str(args[0]) if args else ""
            for key, mock in file_mocks.items():
                if path.endswith(key):
                    return mock()
            return mock_open()()

        with patch('pathlib.Path.exists', side_effect=path_exists_side_effect):
            with patch('pathlib.Path.open', side_effect=open_side_effect):
                config = EvrmoreConfig()
                username, password = config.get_rpc_credentials()
                assert username == '__cookie__'
                assert password == '13f964606c1dcd54240b5ef9fcdf92a43c6a7abe02320a5129181978dc2624ad'

    def test_cookie_file_not_found(self):
        mock_config_content = "rpcport=9999"

        def path_exists_side_effect(self):
            path = str(self)
            if path.endswith("evrmore.conf"):
                return True
            if path.endswith(".cookie"):
                return True  # or False in the other test
            return False

        with patch('pathlib.Path.exists', side_effect=path_exists_side_effect):
            with patch('pathlib.Path.open', mock_open(read_data=mock_config_content)):
                config = EvrmoreConfig()
                username, password = config.get_rpc_credentials()
                assert username is None
                assert password is None

        """Test fallback when neither config nor cookie file has credentials."""
        # Config exists but has no credentials
        mock_config_content = """
        rpcport=9999
        """
        
        # Mock the path.exists method to control what files exist
        def path_exists_side_effect(path):
            if str(path).endswith('evrmore.conf'):
                return True
            elif str(path).endswith('.cookie'):
                return False  # Cookie file doesn't exist
            return False
        
        with patch('pathlib.Path.exists', side_effect=path_exists_side_effect):
            with patch('builtins.open', mock_open(read_data=mock_config_content)):
                config = EvrmoreConfig()
                username, password = config.get_rpc_credentials()
                assert username is None
                assert password is None 