class EvrmoreClient:
    def getblockchaininfo(self) -> dict:
        pass

    def getblock(self, block_hash: str) -> dict:
        pass
    
    # ===== ADDRESSINDEX METHODS =====
    
    def getaddressbalance(self, addresses: list[str]) -> dict:
        """Get the balance for an address."""
        pass
    
    def getaddressdeltas(self, addresses: list[str], start: int = None, end: int = None) -> list[dict]:
        """Get all changes for an address."""
        pass
    
    def getaddressmempool(self, addresses: list[str]) -> list[dict]:
        """Get address-related mempool deltas."""
        pass
    
    def getaddresstxids(self, addresses: list[str], start: int = None, end: int = None) -> list[str]:
        """Get txids for an address."""
        pass
    
    def getaddressutxos(self, addresses: list[str], chainInfo: bool = False) -> list[dict]:
        """Get unspent outputs for an address."""
        pass
    
    # ===== ASSET METHODS =====
    
    def getassetdata(self, asset_name: str) -> dict:
        """Get data for a specific asset."""
        pass
    
    def getcacheinfo(self) -> dict:
        """Get asset cache information."""
        pass
    
    def getsnapshot(self, asset_name: str, block_height: int) -> dict:
        """Get asset ownership snapshot."""
        pass
    
    def issue(self, asset_name: str, qty: float, to_address: str = None, 
              change_address: str = None, units: int = 0, reissuable: bool = True, 
              has_ipfs: bool = False, ipfs_hash: str = None) -> str:
        """Issue a new asset."""
        pass
    
    def issueunique(self, root_name: str, asset_tags: list[str], ipfs_hashes: list[str] = None,
                   to_address: str = None, change_address: str = None) -> str:
        """Issue unique assets."""
        pass
    
    def listaddressesbyasset(self, asset_name: str, onlytotal: bool = False, count: int = 100, start: int = 0) -> dict:
        """List addresses owning an asset."""
        pass
    
    def listassetbalancesbyaddress(self, address: str, onlytotal: bool = False, count: int = 100, start: int = 0) -> dict:
        """List asset balances for an address."""
        pass
    
    def listassets(self, asset: str = "*", verbose: bool = False, count: int = 100, start: int = 0) -> list[dict]:
        """List all assets."""
        pass
    
    def listmyassets(self, asset: str = "*", verbose: bool = False, count: int = 100, start: int = 0, confs: int = 0) -> dict:
        """List assets owned by the wallet."""
        pass
    
    def purgesnapshot(self, asset_name: str, block_height: int) -> None:
        """Purge an asset snapshot."""
        pass
    
    def reissue(self, asset_name: str, qty: float, to_address: str, 
               change_address: str = None, reissuable: bool = True, 
               new_units: int = -1, new_ipfs: str = None) -> str:
        """Reissue an existing asset."""
        pass
    
    def transfer(self, asset_name: str, qty: float, to_address: str, 
                message: str = None, expire_time: int = None,
                change_address: str = None, asset_change_address: str = None) -> str:
        """Transfer an asset."""
        pass
    
    def transferfromaddress(self, asset_name: str, from_address: str, qty: float, 
                           to_address: str, message: str = None, expire_time: int = None,
                           evr_change_address: str = None, asset_change_address: str = None) -> str:
        """Transfer asset from a specific address."""
        pass
    
    def transferfromaddresses(self, asset_name: str, from_addresses: list[str], qty: float,
                             to_address: str, message: str = None, expire_time: int = None,
                             evr_change_address: str = None, asset_change_address: str = None) -> str:
        """Transfer asset from multiple addresses."""
        pass
    
    # ===== BLOCKCHAIN METHODS =====
    
    def clearmempool(self) -> None:
        """Clear the memory pool."""
        pass
    
    def decodeblock(self, blockhex: str) -> dict:
        """Decode a block hex string."""
        pass
    
    def getbestblockhash(self) -> str: 
        """Get the best block hash."""
        pass
    
    def getblock(self, blockhash: str, verbosity: int = 1) -> dict:
        """Get block data."""
        pass
    
    def getblockcount(self) -> int: 
        """Get the current block count."""
        pass
    
    def getblockhash(self, height: int) -> str: 
        """Get a block hash by height."""
        pass
    
    def getblockhashes(self, timestamp: int, blockhash: str = None) -> list[str]:
        """Get block hashes by timestamp."""
        pass
    
    def getblockheader(self, blockhash: str, verbose: bool = True) -> dict:
        """Get a block header."""
        pass
    
    def getchaintips(self) -> list[dict]:
        """Get information about chain tips."""
        pass
    
    def getchaintxstats(self, nblocks: int = None, blockhash: str = None) -> dict:
        """Get chain transaction statistics."""
        pass
    
    def getdifficulty(self) -> float: 
        """Get the current difficulty."""
        pass
    
    def getmempoolancestors(self, txid: str, verbose: bool = False) -> dict:
        """Get mempool transaction ancestors."""
        pass
    
    def getmempooldescendants(self, txid: str, verbose: bool = False) -> dict:
        """Get mempool transaction descendants."""
        pass
    
    def getmempoolentry(self, txid: str) -> dict:
        """Get mempool entry data."""
        pass
    
    def getmempoolinfo(self) -> dict:
        """Get mempool information."""
        pass
    
    def getrawmempool(self, verbose: bool = False) -> dict:
        """Get raw mempool data."""
        pass
    
    def getspentinfo(self, txid: str, index: int) -> dict:
        """Get information about spent outputs."""
        pass
    
    def gettxout(self, txid: str, n: int, include_mempool: bool = True) -> dict:
        """Get an unspent transaction output."""
        pass
    
    def gettxoutproof(self, txids: list[str], blockhash: str = None) -> str:
        """Get a transaction proof."""
        pass
    
    def gettxoutsetinfo(self) -> dict:
        """Get UTXO set information."""
        pass
    
    def preciousblock(self, blockhash: str) -> None:
        """Mark a block as precious."""
        pass
    
    def pruneblockchain(self, height: int) -> int:
        """Prune the blockchain."""
        pass
    
    def savemempool(self) -> None:
        """Save the mempool to disk."""
        pass
    
    def verifychain(self, checklevel: int = 3, nblocks: int = 6) -> bool: 
        """Verify the blockchain."""
        pass
    
    def verifytxoutproof(self, proof: str) -> list[str]:
        """Verify a transaction proof."""
        pass
    
    # ===== CONTROL METHODS =====
    
    def getinfo(self) -> dict:
        """Get general information."""
        pass
    
    def getmemoryinfo(self, mode: str = "stats") -> dict:
        """Get memory usage information."""
        pass
    
    def getrpcinfo(self) -> dict:
        """Get RPC server information."""
        pass
    
    def help(self, command: str = None) -> str:
        """Show help information."""
        pass
    
    def stop(self) -> str:
        """Stop the Evrmore server."""
        pass
    
    def uptime(self) -> int:
        """Get server uptime."""
        pass
    
    # ===== GENERATING METHODS =====
    
    def generate(self, nblocks: int, maxtries: int = 1000000) -> list[str]:
        """Generate blocks."""
        pass
    
    def generatetoaddress(self, nblocks: int, address: str, maxtries: int = 1000000) -> list[str]:
        """Generate blocks to an address."""
        pass
    
    def getgenerate(self) -> bool:
        """Get generation status."""
        pass
    
    def setgenerate(self, generate: bool, genproclimit: int = None) -> None:
        """Set generation status."""
        pass
    
    # ===== MESSAGES METHODS =====
    
    def clearmessages(self) -> None:
        """Clear locally stored messages."""
        pass
    
    def sendmessage(self, channel_name: str, ipfs_hash: str, expire_time: int = None) -> str:
        """Send a message."""
        pass
    
    def subscribetochannel(self, channel_name: str) -> None:
        """Subscribe to a message channel."""
        pass
    
    def unsubscribefromchannel(self, channel_name: str) -> None:
        """Unsubscribe from a channel."""
        pass
    
    def viewallmessagechannels(self) -> list[str]:
        """View all message channels."""
        pass
    
    def viewallmessages(self) -> list[dict]:
        """View all messages."""
        pass
    
    # ===== MINING METHODS =====
    
    def getblocktemplate(self, template_request: dict = None) -> dict:
        """Get a block template for mining."""
        pass
    
    def getevrprogpowhash(self, header_hash: str, mix_hash: str, nonce: int, height: int, target: str) -> str:
        """Get EvrmorePoW hash."""
        pass
    
    def getmininginfo(self) -> dict:
        """Get mining information."""
        pass
    
    def getnetworkhashps(self, nblocks: int = 120, height: int = -1) -> float:
        """Get network hash rate."""
        pass
    
    def pprpcsb(self, header_hash: str, mix_hash: str, nonce: str) -> dict:
        """Verify block parameters."""
        pass
    
    def prioritisetransaction(self, txid: str, dummy_value: int, fee_delta: int) -> bool:
        """Prioritize a transaction."""
        pass
    
    def submitblock(self, hexdata: str, dummy: str = None) -> str:
        """Submit a mined block."""
        pass
    
    # ===== NETWORK METHODS =====
    
    def addnode(self, node: str, command: str) -> None:
        """Add or remove a node."""
        pass
    
    def clearbanned(self) -> None:
        """Clear banned IPs."""
        pass
    
    def disconnectnode(self, address: str = None, nodeid: int = None) -> None:
        """Disconnect a node."""
        pass
    
    def getaddednodeinfo(self, node: str = None) -> list[dict]:
        """Get added node information."""
        pass
    
    def getconnectioncount(self) -> int:
        """Get connection count."""
        pass
    
    def getnettotals(self) -> dict:
        """Get network traffic information."""
        pass
    
    def getnetworkinfo(self) -> dict:
        """Get network information."""
        pass
    
    def getpeerinfo(self) -> list[dict]:
        """Get peer information."""
        pass
    
    def listbanned(self) -> list[dict]:
        """List banned IPs."""
        pass
    
    def ping(self) -> None:
        """Ping network nodes."""
        pass
    
    def setban(self, subnet: str, command: str, bantime: int = 0, absolute: bool = False) -> None:
        """Ban/unban IPs."""
        pass
    
    def setnetworkactive(self, state: bool) -> bool:
        """Set network activity."""
        pass
    
    # ===== RAWTRANSACTIONS METHODS =====
    
    def combinerawtransaction(self, txs: list[str]) -> str:
        """Combine raw transactions."""
        pass
    
    def createrawtransaction(self, inputs: list[dict], outputs: dict, locktime: int = 0, replaceable: bool = False) -> str:
        """Create a raw transaction."""
        pass
    
    def decoderawtransaction(self, hexstring: str) -> dict:
        """Decode a raw transaction."""
        pass
    
    def decodescript(self, hexstring: str) -> dict:
        """Decode a script."""
        pass
    
    def fundrawtransaction(self, hexstring: str, options: dict = None) -> dict:
        """Fund a raw transaction."""
        pass
    
    def getrawtransaction(self, txid: str, verbose: bool = False) -> dict:
        """Get a raw transaction."""
        pass
    
    def sendrawtransaction(self, hexstring: str, allowhighfees: bool = False) -> str:
        """Send a raw transaction."""
        pass
    
    def signrawtransaction(self, hexstring: str, prevtxs: list[dict] = None, 
                          privkeys: list[str] = None, sighashtype: str = "ALL") -> dict:
        """Sign a raw transaction."""
        pass
    
    def testmempoolaccept(self, rawtxs: list[str], allowhighfees: bool = False) -> list[dict]:
        """Test mempool acceptance."""
        pass
    
    # ===== RESTRICTED ASSETS METHODS =====
    
    def addtagtoaddress(self, tag_name: str, to_address: str, 
                       change_address: str = None, 
                       asset_data: str = None) -> str:
        """Add a tag to an address."""
        pass
    
    def checkaddressrestriction(self, address: str, restricted_name: str) -> bool:
        """Check address restrictions."""
        pass
    
    def checkaddresstag(self, address: str, tag_name: str) -> bool:
        """Check address tags."""
        pass
    
    def checkglobalrestriction(self, restricted_name: str) -> bool:
        """Check global restrictions."""
        pass
    
    def freezeaddress(self, asset_name: str, address: str, 
                     change_address: str = None, 
                     asset_data: str = None) -> str:
        """Freeze an address for an asset."""
        pass
    
    def freezerestrictedasset(self, asset_name: str, 
                             change_address: str = None, 
                             asset_data: str = None) -> str:
        """Freeze a restricted asset."""
        pass
    
    def getverifierstring(self, restricted_name: str) -> str:
        """Get verifier string."""
        pass
    
    def issuequalifierasset(self, asset_name: str, qty: float, to_address: str = None,
                           change_address: str = None, has_ipfs: bool = False, 
                           ipfs_hash: str = None) -> str:
        """Issue a qualifier asset."""
        pass
    
    def issuerestrictedasset(self, asset_name: str, qty: float, verifier: str, 
                             to_address: str, change_address: str = None, units: int = 0, 
                             reissuable: bool = True, has_ipfs: bool = False, 
                             ipfs_hash: str = None) -> str:
        """Issue a restricted asset."""
        pass
    
    def isvalidverifierstring(self, verifier_string: str) -> bool:
        """Validate verifier string."""
        pass
    
    def listaddressesfortag(self, tag_name: str) -> list[str]:
        """List addresses for a tag."""
        pass
    
    def listaddressrestrictions(self, address: str) -> dict:
        """List address restrictions."""
        pass
    
    def listglobalrestrictions(self) -> dict:
        """List global restrictions."""
        pass
    
    def listtagsforaddress(self, address: str) -> list[str]:
        """List tags for an address."""
        pass
    
    def reissuerestrictedasset(self, asset_name: str, qty: float, to_address: str,
                              change_verifier: bool = False, new_verifier: str = None,
                              change_address: str = None, new_units: int = -1,
                              reissuable: bool = True, new_ipfs: str = None) -> str:
        """Reissue a restricted asset."""
        pass
    
    def removetagfromaddress(self, tag_name: str, to_address: str, 
                            change_address: str = None, 
                            asset_data: str = None) -> str:
        """Remove tag from address."""
        pass
    
    def transferqualifier(self, qualifier_name: str, qty: float, to_address: str,
                         change_address: str = None, message: str = None,
                         expire_time: int = None) -> str:
        """Transfer a qualifier."""
        pass
    
    def unfreezeaddress(self, asset_name: str, address: str, 
                       change_address: str = None, 
                       asset_data: str = None) -> str:
        """Unfreeze an address."""
        pass
    
    def unfreezerestrictedasset(self, asset_name: str, 
                               change_address: str = None, 
                               asset_data: str = None) -> str:
        """Unfreeze a restricted asset."""
        pass
    
    # ===== RESTRICTED COMMANDS =====
    
    def viewmyrestrictedaddresses(self) -> dict:
        """View my restricted addresses."""
        pass
    
    def viewmytaggedaddresses(self) -> dict:
        """View my tagged addresses."""
        pass
    
    # ===== REWARDS METHODS =====
    
    def cancelsnapshotrequest(self, asset_name: str, block_height: int) -> None:
        """Cancel a snapshot request."""
        pass
    
    def distributereward(self, asset_name: str, snapshot_height: int, distribution_asset_name: str, 
                        gross_distribution_amount: float, 
                        exception_addresses: list[str] = None, 
                        change_address: str = None, 
                        dry_run: bool = False) -> dict:
        """Distribute rewards."""
        pass
    
    def getdistributestatus(self, asset_name: str, snapshot_height: int, distribution_asset_name: str, 
                           gross_distribution_amount: float, 
                           exception_addresses: list[str] = None) -> dict:
        """Get distribution status."""
        pass
    
    def getsnapshotrequest(self, asset_name: str, block_height: int) -> dict:
        """Get snapshot request."""
        pass
    
    def listsnapshotrequests(self, asset_names: list[str] = None, 
                            block_heights: list[int] = None) -> list[dict]:
        """List snapshot requests."""
        pass
    
    def requestsnapshot(self, asset_name: str, block_height: int) -> None:
        """Request a snapshot."""
        pass
    
    # ===== UTIL METHODS =====
    
    def createmultisig(self, nrequired: int, keys: list[str]) -> dict:
        """Create multisig address."""
        pass
    
    def estimatefee(self, nblocks: int) -> float:
        """Estimate fee."""
        pass
    
    def estimatesmartfee(self, conf_target: int, estimate_mode: str = "CONSERVATIVE") -> dict:
        """Estimate smart fee."""
        pass
    
    def signmessagewithprivkey(self, privkey: str, message: str) -> str:
        """Sign message with private key."""
        pass
    
    def validateaddress(self, address: str) -> dict:
        """Validate an address."""
        pass
    
    def verifymessage(self, address: str, signature: str, message: str) -> bool:
        """Verify a message."""
        pass
    
    # ===== WALLET METHODS =====
    
    def abandontransaction(self, txid: str) -> None: 
        """Abandon a transaction."""
        pass
    
    def abortrescan(self) -> bool:
        """Abort blockchain rescan."""
        pass
    
    def addmultisigaddress(self, nrequired: int, keys: list[str], account: str = "") -> str:
        """Add a multisig address."""
        pass
    
    def addwitnessaddress(self, address: str) -> str:
        """Add a witness address."""
        pass
    
    def backupwallet(self, destination: str) -> None:
        """Backup wallet."""
        pass
    
    def dumpprivkey(self, address: str) -> str:
        """Dump private key."""
        pass
    
    def dumpwallet(self, filename: str) -> str:
        """Dump wallet."""
        pass
    
    def encryptwallet(self, passphrase: str) -> str:
        """Encrypt wallet."""
        pass
    
    def getaccount(self, address: str) -> str:
        """Get account."""
        pass
    
    def getaccountaddress(self, account: str) -> str:
        """Get account address."""
        pass
    
    def getaddressesbyaccount(self, account: str) -> list[str]:
        """Get addresses by account."""
        pass
    
    def getbalance(self, account: str = "*", minconf: int = 1, include_watchonly: bool = False) -> float: 
        """Get balance."""
        pass
    
    def getmasterkeyinfo(self) -> dict:
        """Get master key info."""
        pass
    
    def getmywords(self, account: str = None) -> str:
        """Get mnemonic words."""
        pass
    
    def getnewaddress(self, account: str = "") -> str: 
        """Get new address."""
        pass
    
    def getrawchangeaddress(self) -> str: 
        """Get raw change address."""
        pass
    
    def getreceivedbyaccount(self, account: str, minconf: int = 1) -> float:
        """Get received by account."""
        pass
    
    def getreceivedbyaddress(self, address: str, minconf: int = 1) -> float: 
        """Get received by address."""
        pass
    
    def gettransaction(self, txid: str, include_watchonly: bool = False) -> dict:
        """Get transaction."""
        pass
    
    def getunconfirmedbalance(self) -> float: 
        """Get unconfirmed balance."""
        pass
    
    def getwalletinfo(self) -> dict:
        """Get wallet info."""
        pass
    
    def importaddress(self, address: str, label: str = "", rescan: bool = True, p2sh: bool = False) -> None:
        """Import address."""
        pass
    
    def importmulti(self, requests: list[dict], options: dict = None) -> list[dict]:
        """Import multiple addresses."""
        pass
    
    def importprivkey(self, privkey: str, label: str = "", rescan: bool = True) -> None:
        """Import private key."""
        pass
    
    def importprunedfunds(self, rawtransaction: str, txoutproof: str) -> None:
        """Import pruned funds."""
        pass
    
    def importpubkey(self, pubkey: str, label: str = "", rescan: bool = True) -> None:
        """Import public key."""
        pass
    
    def importwallet(self, filename: str) -> None:
        """Import wallet."""
        pass
    
    def keypoolrefill(self, newsize: int = 100) -> None:
        """Refill keypool."""
        pass
    
    def listaccounts(self, minconf: int = 1, include_watchonly: bool = False) -> dict:
        """List accounts."""
        pass
    
    def listaddressgroupings(self) -> list:
        """List address groupings."""
        pass
    
    def listlockunspent(self) -> list[dict]:
        """List locked outputs."""
        pass
    
    def listreceivedbyaccount(self, minconf: int = 1, include_empty: bool = False, include_watchonly: bool = False) -> list[dict]:
        """List received by account."""
        pass
    
    def listreceivedbyaddress(self, minconf: int = 1, include_empty: bool = False, include_watchonly: bool = False) -> list[dict]:
        """List received by address."""
        pass
    
    def listsinceblock(self, blockhash: str = None, target_confirmations: int = 1, include_watchonly: bool = False, include_removed: bool = True) -> dict:
        """List transactions since block."""
        pass
    
    def listtransactions(self, account: str = "*", count: int = 10, skip: int = 0, include_watchonly: bool = False) -> list[dict]:
        """List transactions."""
        pass
    
    def listunspent(self, minconf: int = 1, maxconf: int = 9999999, 
                   addresses: list[str] = None, 
                   include_unsafe: bool = True, 
                   query_options: dict = None) -> list[dict]:
        """List unspent outputs."""
        pass
    
    def listwallets(self) -> list[str]:
        """List wallets."""
        pass
    
    def lockunspent(self, unlock: bool, transactions: list[dict] = None) -> bool:
        """Lock/unlock unspent outputs."""
        pass
    
    def move(self, fromaccount: str, toaccount: str, amount: float, minconf: int = 1, comment: str = "") -> bool:
        """Move funds between accounts."""
        pass
    
    def removeprunedfunds(self, txid: str) -> None:
        """Remove pruned funds."""
        pass
    
    def rescanblockchain(self, start_height: int = None, stop_height: int = None) -> dict:
        """Rescan blockchain."""
        pass
    
    def sendfrom(self, fromaccount: str, toaddress: str, amount: float, minconf: int = 1, comment: str = "", comment_to: str = "") -> str:
        """Send from account."""
        pass
    
    def sendfromaddress(self, from_address: str, to_address: str, amount: float, 
                       comment: str = "", comment_to: str = "", subtractfeefromamount: bool = False,
                       replaceable: bool = False, conf_target: int = 1, estimate_mode: str = "UNSET") -> str:
        """Send from address."""
        pass
    
    def sendmany(self, fromaccount: str, amounts: dict, minconf: int = 1, comment: str = "", subtractfeefrom: list[str] = None, replaceable: bool = False, conf_target: int = 1, estimate_mode: str = "UNSET") -> str:
        """Send to multiple addresses."""
        pass
    
    def sendtoaddress(self, address: str, amount: float, 
                     comment: str = "", comment_to: str = "", 
                     subtractfeefromamount: bool = False, 
                     replaceable: bool = False, 
                     conf_target: int = 1, 
                     estimate_mode: str = "UNSET") -> str: 
        """Send to address."""
        pass
    
    def setaccount(self, address: str, account: str) -> None:
        """Set account."""
        pass
    
    def settxfee(self, amount: float) -> bool:
        """Set transaction fee."""
        pass
    
    def signmessage(self, address: str, message: str) -> str:
        """Sign message."""
        pass
    
    def walletlock(self) -> None:
        """Lock wallet."""
        pass
    
    def walletpassphrase(self, passphrase: str, timeout: int) -> None:
        """Unlock wallet with passphrase."""
        pass
    
    def walletpassphrasechange(self, oldpassphrase: str, newpassphrase: str) -> None:
        """Change wallet passphrase."""
        pass
    
    