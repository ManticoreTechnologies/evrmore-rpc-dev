"""
Models for ZMQ notifications from the Evrmore blockchain.

This module provides data structures for the ZMQ notifications sent by Evrmore nodes.
These models ensure properly typed and structured data when working with ZMQ notifications.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List, Union


@dataclass
class ZMQNotification:
    """
    Represents a ZMQ notification from an Evrmore node.
    
    ZMQ notifications contain the following information:
    - topic: The type of notification (e.g., 'hashblock', 'hashtx')
    - body: The binary data of the notification (e.g., block or transaction hash)
    - sequence: A sequence number for the notification
    - hex: The hexadecimal representation of the binary data
    
    The exact format of the body depends on the notification type:
    - HASH_BLOCK: 32-byte block hash
    - HASH_TX: 32-byte transaction hash
    - RAW_BLOCK: Full serialized block
    - RAW_TX: Full serialized transaction
    
    Attributes:
        topic (str): The notification topic (e.g., 'hashblock', 'hashtx')
        body (bytes): The binary data of the notification
        sequence (int): A sequence number for the notification
        hex (str): Hexadecimal representation of the binary data
    """
    topic: str
    body: bytes
    sequence: int
    hex: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def __repr__(self) -> str:
        """String representation of the notification."""
        return f"ZMQNotification(topic='{self.topic}', hex='{self.hex[:16]}{'...' if len(self.hex) > 16 else ''}', sequence={self.sequence})"


@dataclass
class ZMQDecodedBlockNotification(ZMQNotification):
    """
    Represents a ZMQ notification with an automatically decoded block.
    
    This notification type extends the standard ZMQNotification with decoded block data.
    It is used with the enhanced ZMQTopic.BLOCK subscription.
    
    Attributes:
        block (Dict[str, Any]): The decoded block data
        height (int): The block height
        is_valid (bool): Whether the block data was successfully decoded
        error (Optional[str]): Error message if decoding failed
    """
    block: Union[Dict[str, Any], Any] = None
    height: Optional[int] = None
    is_valid: bool = True
    error: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        # If block is a dict, get tx count for __repr__
        self._tx_count = 0
        if self.is_valid and self.block is not None:
            try:
                if isinstance(self.block, dict):
                    self._tx_count = len(self.block.get('tx', []))
                else:
                    # Try to access tx attribute or method
                    tx = getattr(self.block, 'tx', None)
                    if tx is not None:
                        if callable(tx):
                            tx = tx()
                        self._tx_count = len(tx)
            except Exception:
                self._tx_count = 0
    
    def __repr__(self) -> str:
        """String representation of the decoded block notification."""
        if self.is_valid and self.block:
            # Get additional block information when available
            block_info = self.block
            size = block_info.get('size', 0) if isinstance(block_info, dict) else getattr(block_info, 'size', 0)
            time_str = ""
            if isinstance(block_info, dict) and 'time' in block_info:
                try:
                    time_obj = datetime.fromtimestamp(block_info['time'])
                    time_str = f", time={time_obj.strftime('%Y-%m-%d %H:%M:%S')}"
                except:
                    pass
            
            # Create a more informative representation
            return f"Block [Height: {self.height}] {self.hex}\n" \
                   f"  • Transactions: {self._tx_count}\n" \
                   f"  • Size: {size} bytes{time_str}"
        return f"Invalid Block {self.hex[:16]}... (Error: {self.error})"


@dataclass
class ZMQDecodedTxNotification(ZMQNotification):
    """
    Represents a ZMQ notification with an automatically decoded transaction.
    
    This notification type extends the standard ZMQNotification with decoded transaction data.
    It is used with the enhanced ZMQTopic.TX subscription.
    
    Attributes:
        tx (Dict[str, Any]): The decoded transaction data
        is_valid (bool): Whether the transaction data was successfully decoded
        error (Optional[str]): Error message if decoding failed
        has_assets (bool): Whether the transaction contains asset operations
        asset_info (List[Dict[str, Any]]): Information about assets in the transaction
    """
    tx: Union[Dict[str, Any], Any] = None
    is_valid: bool = True
    error: Optional[str] = None
    has_assets: bool = False
    asset_info: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        super().__post_init__()
        # Initialize asset_info if None
        if self.asset_info is None:
            self.asset_info = []
            
        # Calculate vin and vout counts for __repr__
        self._vin_count = 0
        self._vout_count = 0
        if self.is_valid and self.tx is not None:
            try:
                if isinstance(self.tx, dict):
                    self._vin_count = len(self.tx.get('vin', []))
                    self._vout_count = len(self.tx.get('vout', []))
                    
                    # Check for asset operations in the transaction outputs
                    self._extract_asset_info_from_dict()
                else:
                    # Try to access vin and vout attributes or methods
                    vin = getattr(self.tx, 'vin', None)
                    vout = getattr(self.tx, 'vout', None)
                    
                    if vin is not None:
                        if callable(vin):
                            vin = vin()
                        self._vin_count = len(vin)
                        
                    if vout is not None:
                        if callable(vout):
                            vout = vout()
                        self._vout_count = len(vout)
                        
                    # Extract asset info from object attributes
                    self._extract_asset_info_from_object()
            except Exception:
                self._vin_count = 0
                self._vout_count = 0
    
    def _extract_asset_info_from_dict(self):
        """Extract asset information from dictionary transaction data"""
        if not isinstance(self.tx, dict):
            return
            
        # Check vouts for asset operations
        for vout in self.tx.get('vout', []):
            script_pub_key = vout.get('scriptPubKey', {})
            
            # Check if this output is asset-related
            if 'asset' in script_pub_key or script_pub_key.get('type', '') in ('new_asset', 'transfer_asset', 'reissue_asset'):
                self.has_assets = True
                
                asset_data = script_pub_key.get('asset', {})
                if asset_data:
                    self.asset_info.append({
                        'type': script_pub_key.get('type', 'unknown'),
                        'vout_n': vout.get('n'),
                        'asset_name': asset_data.get('name'),
                        'amount': asset_data.get('amount'),
                        'address': script_pub_key.get('addresses', [None])[0],
                        'data': asset_data
                    })
    
    def _extract_asset_info_from_object(self):
        """Extract asset information from object transaction data"""
        if isinstance(self.tx, dict):
            return
            
        # Try to access vout attribute or method
        try:
            vout = getattr(self.tx, 'vout', None)
            if vout is not None:
                if callable(vout):
                    vout = vout()
                    
                # Process each vout
                for v in vout:
                    # Try to get scriptPubKey
                    script_pub_key = getattr(v, 'scriptPubKey', None)
                    if script_pub_key is None:
                        continue
                        
                    # Check if asset type or has asset attribute
                    output_type = getattr(script_pub_key, 'type', '')
                    if 'asset' in output_type or hasattr(script_pub_key, 'asset'):
                        self.has_assets = True
                        
                        # Try to get asset data
                        asset_data = getattr(script_pub_key, 'asset', None)
                        if asset_data:
                            self.asset_info.append({
                                'type': output_type,
                                'vout_n': getattr(v, 'n', None),
                                'asset_name': getattr(asset_data, 'name', None),
                                'amount': getattr(asset_data, 'amount', None),
                                'address': getattr(script_pub_key, 'addresses', [None])[0] if hasattr(script_pub_key, 'addresses') else None,
                                'data': asset_data
                            })
        except Exception:
            pass
    
    def __repr__(self) -> str:
        """String representation of the decoded transaction notification."""
        if self.is_valid and self.tx:
            # Extract additional information if available
            tx_info = self.tx
            size = tx_info.get('size', 0) if isinstance(tx_info, dict) else getattr(tx_info, 'size', 0)
            version = tx_info.get('version', '') if isinstance(tx_info, dict) else getattr(tx_info, 'version', '')
            
            # Format value sums if available
            total_in = 0
            total_out = 0
            
            if isinstance(tx_info, dict):
                # Try to calculate input sum
                try:
                    for vin in tx_info.get('vin', []):
                        if 'value' in vin:
                            total_in += float(vin['value'])
                except:
                    pass
                
                # Try to calculate output sum
                try:
                    for vout in tx_info.get('vout', []):
                        if 'value' in vout:
                            total_out += float(vout['value'])
                except:
                    pass
            
            # Format the asset information
            asset_str = ""
            if self.has_assets:
                asset_names = [a.get('asset_name', 'Unknown') for a in self.asset_info]
                unique_assets = set(asset_names)
                asset_str = f"\n  • Assets: {', '.join(unique_assets)} ({len(self.asset_info)} operations)"
            
            # Build the representation
            return f"Transaction {self.hex}\n" \
                   f"  • Inputs: {self._vin_count}, Outputs: {self._vout_count}\n" \
                   f"  • Size: {size} bytes, Version: {version}" + \
                   (f"\n  • Value: {total_in} EVR → {total_out} EVR" if total_in > 0 or total_out > 0 else "") + \
                   asset_str
                   
        return f"Invalid Transaction {self.hex[:16]}... (Error: {self.error})" 
    
@dataclass
class ZMQMessageNotification(ZMQNotification):
    """
    Represents a ZMQ notification with a message.
    """
    message: str = None
    asset_name: str = None
    address: str = None
    
    def __repr__(self) -> str:
        """String representation of the message notification."""
        return f"Message {self.hex}\n" \
               f"  • Asset: {self.asset_name}\n" \
               f"  • Address: {self.address}\n" \
               f"  • Message: {self.message}"