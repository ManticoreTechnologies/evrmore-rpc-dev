"""
📚 Evrmore RPC Coverage Map
---------------------------

This file mirrors the structure of `evrmore-cli help` to provide a human-readable,
clickable checklist of every RPC command expected to be implemented in `EvrmoreClient`.

🧩 Purpose:
- Ensure all known RPC methods from the Evrmore daemon are implemented
- Group methods logically to match the official CLI categories
- Allow Ctrl+Click navigation in your editor for easy inspection
- Serve as a living reference for maintenance and expansion

⚠️ This is NOT meant to be executed:
- Many methods mutate wallet or chain state (e.g. `sendtoaddress`, `generate`)
- Parameters are placeholders or partial
- There are no actual return value checks or network assertions

✅ Ideal Usage:
- Use as a manual verification sheet while writing or auditing the client
- Quickly search or diff against new CLI output from `evrmore-cli help`
- Identify missing or deprecated methods and tag them inline

📦 Categories are aligned with:
    - Addressindex
    - Assets
    - Blockchain
    - Control
    - Generating
    - Messages
    - Mining
    - Network
    - Rawtransactions
    - Restricted Assets
    - Rewards
    - Util
    - Wallet

© 2025 Manticore Technologies, LLC
Maintained by: Cymos (EfletL7gMLYkuu9CfHcRevVk3KdnG5JgruSE)
"""

from evrmore_rpc import EvrmoreClient
client = EvrmoreClient()

""" == Addressindex == """

# Get address balance
client.getaddressbalance("address")

# Get address deltas
client.getaddressdeltas({
    "addresses": ["address"],
    "start": 0,
    "end": 100,
    "chainInfo": True
})

# Get address mempool
client.getaddressmempool({
    "addresses": ["address"]
})

# Get address transaction IDs
client.getaddresstxids({
    "addresses": ["address"],
    "start": 0,
    "end": 100
})

# Get address UTXOs
client.getaddressutxos({
    "addresses": ["address"],
    "chainInfo": True
})

""" == Assets == """

# Get asset data
client.getassetdata("asset_name")

# Get cache info
client.getcacheinfo()

# Get snapshot
client.getsnapshot("asset_name", block_height)

# Issue asset
client.issue(
    "asset_name",
    qty=1000,
    to_address="address",
    change_address="address",
    units=0,
    reissuable=True,
    has_ipfs=False,
    ipfs_hash=""
)

# Issue unique asset
client.issueunique(
    "root_name",
    asset_tags=["tag1", "tag2"],
    ipfs_hashes=["hash1", "hash2"],
    to_address="address",
    change_address="address"
)

# List addresses by asset
client.listaddressesbyasset(
    "asset_name",
    onlytotal=False,
    count=10,
    start=0
)

# List asset balances by address
client.listassetbalancesbyaddress(
    "address",
    onlytotal=False,
    count=10,
    start=0
)

# List assets
client.listassets(
    "asset_name",
    verbose=True,
    count=10,
    start=0
)

# List my assets
client.listmyassets(
    "asset_name",
    verbose=True,
    count=10,
    start=0
)

# Purge snapshot
client.purgesnapshot("asset_name", block_height)

# Reissue asset
client.reissue(
    "asset_name",
    qty=1000,
    to_address="address",
    change_address="address",
    reissuable=True,
    new_units=-1,
    new_ipfs=""
)

# Transfer asset
client.transfer(
    "asset_name",
    qty=100,
    to_address="address",
    message="",
    expire_time=0,
    change_address="address"
)

# Transfer from
client.transferfrom(
    "asset_name",
    "from_address",
    qty=100,
    to_address="address",
    message="",
    expire_time=0,
    change_address="address"
)

""" == Blockchain == """

# Get best block hash
client.getbestblockhash()

# Get block
client.getblock("blockhash", verbosity=1)

# Get block chain info
client.getblockchaininfo()

# Get block count
client.getblockcount()

# Get block hash
client.getblockhash(height)

# Get block header
client.getblockheader("blockhash", verbose=True)

# Get chain tips
client.getchaintips()

# Get difficulty
client.getdifficulty()

# Get mempool ancestor fees
client.getmempoolancestorfees("txid")

# Get mempool entry
client.getmempoolentry("txid")

# Get mempool info
client.getmempoolinfo()

# Get raw mempool
client.getrawmempool(verbose=False)

# Get spent info
client.getspentinfo({
    "txid": "txid",
    "index": 0
})

# Get tx out
client.gettxout("txid", 0, include_mempool=True)

# Get tx out proof
client.gettxoutproof(["txid"], "blockhash")

# Get tx out set info
client.gettxoutsetinfo()

# Precious block
client.preciousblock("blockhash")

# Prune blockchain
client.pruneblockchain(height)

# Save mempool
client.savemempool()

# Verify chain
client.verifychain(checklevel=3, nblocks=6)

# Verify tx out proof
client.verifytxoutproof("proof")

""" == Control == """

# Get info
client.getinfo()

# Get memory info
client.getmemoryinfo(mode="stats")

# Get RPC info
client.getrpcinfo()

# Help
client.help("command")

# Stop
client.stop()

# Uptime
client.uptime()

""" == Generating == """

# Generate
client.generate(nblocks=1)

# Generate to address
client.generatetoaddress(nblocks=1, address="address")

""" == Messages == """

# Get message
client.getmessage("message_id")

# Get message status
client.getmessagestatus("message_id")

# List messages
client.listmessages(
    message_type="all",
    count=10,
    start=0,
    verbose=True
)

# Send message
client.sendmessage(
    "message",
    "to_address",
    "from_address",
    subject="",
    message_type="text",
    expire_time=0
)

""" == Mining == """

# Get block template
client.getblocktemplate(
    mode="template",
    capabilities=["support"],
    rules=["support"]
)

# Get mining info
client.getmininginfo()

# Get network hash ps
client.getnetworkhashps(nblocks=120, height=-1)

# Prioritise transaction
client.prioritisetransaction(
    "txid",
    fee_delta=0,
    dummy=False
)

# Submit block
client.submitblock("hexdata", "dummy")

""" == Network == """

# Add node
client.addnode("node", "command")

# Clear banned
client.clearbanned()

# Disconnect node
client.disconnectnode("address", nodeid=0)

# Get added node info
client.getaddednodeinfo("node")

# Get connection count
client.getconnectioncount()

# Get net totals
client.getnettotals()

# Get network info
client.getnetworkinfo()

# Get peer info
client.getpeerinfo()

# List banned
client.listbanned()

# Ping
client.ping()

# Set ban
client.setban(
    "subnet",
    "command",
    bantime=0,
    absolute=False
)

""" == Rawtransactions == """

# Combine raw transaction
client.combinerawtransaction(["hexstring"])

# Create raw transaction
client.createrawtransaction(
    [{"txid": "txid", "vout": 0}],
    {"address": 0.1}
)

# Decode raw transaction
client.decoderawtransaction("hexstring")

# Decode script
client.decodescript("hexstring")

# Fund raw transaction
client.fundrawtransaction(
    "hexstring",
    {
        "changeAddress": "address",
        "changePosition": 1,
        "includeWatching": True,
        "lockUnspents": True,
        "feeRate": 0.1,
        "subtractFeeFromOutputs": [0],
        "replaceable": False,
        "conf_target": 1,
        "estimate_mode": "UNSET"
    }
)

# Get raw transaction
client.getrawtransaction("txid", verbose=True)

# Send raw transaction
client.sendrawtransaction(
    "hexstring",
    allowhighfees=False,
    dummy=False
)

# Sign raw transaction
client.signrawtransaction(
    "hexstring",
    [{"txid": "txid", "vout": 0, "scriptPubKey": "hex", "redeemScript": "hex"}],
    ["privatekey"],
    "sighashtype"
)

""" == Restricted Assets == """

# Get restricted asset data
client.getrestrictedassetdata("asset_name")

# Get restricted asset snapshot
client.getrestrictedassetsnapshot("asset_name", block_height)

# Issue restricted asset
client.issuerestrictedasset(
    "asset_name",
    qty=1000,
    to_address="address",
    change_address="address",
    units=0,
    reissuable=True,
    has_ipfs=False,
    ipfs_hash="",
    verifier="",
    tags=["tag1", "tag2"]
)

# List restricted assets
client.listrestrictedassets(
    "asset_name",
    verbose=True,
    count=10,
    start=0
)

# Purge restricted asset snapshot
client.purgerestrictedassetsnapshot("asset_name", block_height)

# Reissue restricted asset
client.reissuerestrictedasset(
    "asset_name",
    qty=1000,
    to_address="address",
    change_address="address",
    reissuable=True,
    new_units=-1,
    new_ipfs="",
    new_verifier="",
    new_tags=["tag1", "tag2"]
)

# Transfer restricted asset
client.transferrestrictedasset(
    "asset_name",
    qty=100,
    to_address="address",
    message="",
    expire_time=0,
    change_address="address"
)

""" == Rewards == """

# Get reward info
client.getrewardinfo()

# Get reward snapshot
client.getrewardsnapshot(block_height)

# List rewards
client.listrewards(
    "reward_name",
    verbose=True,
    count=10,
    start=0
)

# Purge reward snapshot
client.purgerewardsnapshot(block_height)

""" == Util == """

# Create multisig
client.createmultisig(
    nrequired=2,
    keys=["key1", "key2"]
)

# Estimate fee
client.estimatefee(nblocks=6)

# Estimate priority
client.estimatepriority(nblocks=6)

# Estimate smart fee
client.estimatesmartfee(
    conf_target=6,
    estimate_mode="CONSERVATIVE"
)

# Estimate smart priority
client.estimatesmartpriority(nblocks=6)

# Sign message with address
client.signmessagewithprivkey("privkey", "message")

# Validate address
client.validateaddress("address")

# Verify message
client.verifymessage("address", "signature", "message")

""" == Wallet == """

# Abandon transaction
client.abandontransaction("txid")

# Abort rescan
client.abortrescan()

# Add multisig address
client.addmultisigaddress(
    nrequired=2,
    keys=["key1", "key2"],
    account=""
)

# Backup wallet
client.backupwallet("destination")

# Bump fee
client.bumpfee(
    "txid",
    {
        "confTarget": 6,
        "totalFee": 0.1,
        "replaceable": True,
        "estimate_mode": "UNSET"
    }
)

# Create wallet
client.createwallet(
    "wallet_name",
    disable_private_keys=False,
    blank=False,
    passphrase="",
    avoid_reuse=False
)

# Dump private key
client.dumpprivkey("address")

# Dump wallet
client.dumpwallet("filename")

# Encrypt wallet
client.encryptwallet("passphrase")

# Get account
client.getaccount("address")

# Get account address
client.getaccountaddress("account")

# Get addresses by account
client.getaddressesbyaccount("account")

# Get balance
client.getbalance(
    account="*",
    minconf=1,
    include_watchonly=True
)

# Get new address
client.getnewaddress(account="")

# Get raw change address
client.getrawchangeaddress()

# Get received by account
client.getreceivedbyaccount(
    "account",
    minconf=1
)

# Get received by address
client.getreceivedbyaddress(
    "address",
    minconf=1
)

# Get transaction
client.gettransaction(
    "txid",
    include_watchonly=True
)

# Get unconfirmed balance
client.getunconfirmedbalance()

# Get wallet info
client.getwalletinfo()

# Import address
client.importaddress(
    "address",
    label="",
    rescan=True,
    p2sh=False
)

# Import multi
client.importmulti(
    [{
        "scriptPubKey": {"address": "address"},
        "timestamp": 0,
        "redeemscript": "script",
        "pubkeys": ["key"],
        "keys": ["key"],
        "internal": False,
        "watchonly": False,
        "label": "label"
    }],
    {
        "rescan": True
    }
)

# Import private key
client.importprivkey(
    "privkey",
    label="",
    rescan=True
)

# Import public key
client.importpubkey(
    "pubkey",
    label="",
    rescan=True
)

# Import wallet
client.importwallet("filename")

# Key pool refill
client.keypoolrefill(newsize=100)

# List accounts
client.listaccounts(
    minconf=1,
    include_watchonly=True
)

# List address groupings
client.listaddressgroupings()

# List lock unspent
client.listlockunspent()

# List received by account
client.listreceivedbyaccount(
    minconf=1,
    include_empty=False,
    include_watchonly=True
)

# List received by address
client.listreceivedbyaddress(
    minconf=1,
    include_empty=False,
    include_watchonly=True
)

# List since block
client.listsinceblock(
    "blockhash",
    target_confirmations=1,
    include_watchonly=True,
    include_removed=False
)

# List transactions
client.listtransactions(
    account="*",
    count=10,
    skip=0,
    include_watchonly=True
)

# List unspent
client.listunspent(
    minconf=1,
    maxconf=9999999,
    addresses=["address"],
    include_unsafe=True,
    query_options={
        "minimumAmount": 0.1,
        "maximumAmount": 1.0,
        "maximumCount": 10,
        "minimumSumAmount": 1.0
    }
)

# List wallet dir
client.listwalletdir()

# List wallets
client.listwallets()

# Load wallet
client.loadwallet(
    "filename",
    load_on_startup=False
)

# Lock unspent
client.lockunspent(
    unlock=False,
    transactions=[{
        "txid": "txid",
        "vout": 0
    }]
)

# Move
client.move(
    "fromaccount",
    "toaccount",
    amount=0.1,
    minconf=1,
    comment=""
)

# Remove pruned funds
client.removeprunedfunds("txid")

# Rescan blockchain
client.rescanblockchain(
    start_height=0,
    stop_height=0
)

# Send from
client.sendfrom(
    "fromaccount",
    "toaddress",
    amount=0.1,
    minconf=1,
    comment="",
    comment_to=""
)

# Send many
client.sendmany(
    "fromaccount",
    {
        "address": 0.1
    },
    minconf=1,
    comment="",
    subtractfeefrom=["address"]
)

# Send to address
client.sendtoaddress(
    "address",
    amount=0.1,
    comment="",
    comment_to="",
    subtractfeefromamount=False,
    replaceable=False,
    conf_target=6,
    estimate_mode="UNSET"
)

# Set account
client.setaccount("address", "account")

# Set tx fee
client.settxfee(amount=0.0001)

# Sign raw transaction with key
client.signrawtransactionwithkey(
    "hexstring",
    ["privatekey"],
    [{
        "txid": "txid",
        "vout": 0,
        "scriptPubKey": "hex",
        "redeemScript": "hex",
        "amount": 0.1
    }],
    "sighashtype"
)

# Sign raw transaction with wallet
client.signrawtransactionwithwallet(
    "hexstring",
    [{
        "txid": "txid",
        "vout": 0,
        "scriptPubKey": "hex",
        "redeemScript": "hex",
        "amount": 0.1
    }],
    "sighashtype"
)

# Unload wallet
client.unloadwallet("wallet_name")

# Wallet lock
client.walletlock()

# Wallet passphrase
client.walletpassphrase("passphrase", timeout=60)

# Wallet passphrase change
client.walletpassphrasechange("oldpassphrase", "newpassphrase")
