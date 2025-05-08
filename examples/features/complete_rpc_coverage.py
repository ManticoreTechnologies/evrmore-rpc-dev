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

client.getaddressbalance()
client.getaddressdeltas()
client.getaddressmempool()
client.getaddresstxids()
client.getaddressutxos()

""" == Assets == """

client.getassetdata("asset_name")
client.getcacheinfo()
client.getsnapshot("asset_name", block_height)
client.issue("asset_name", qty, "to_address", "change_address", units, reissuable, has_ipfs, "ipfs_hash")
client.issueunique("root_name", asset_tags, ipfs_hashes, to_address, change_address)
client.listaddressesbyasset("asset_name", onlytotal, count, start)
client.listassetbalancesbyaddress("address", onlytotal, count, start)
client.listassets("asset", verbose, count, start)
client.listmyassets("asset", verbose, count, start, confs) 
client.purgesnapshot("asset_name", block_height)
client.reissue("asset_name", qty, "to_address", "change_address", reissuable, new_units, "new_ipfs") 
client.transfer("asset_name", qty, "to_address", "message", expire_time, "change_address", "asset_change_address")
client.transferfromaddress("asset_name", "from_address", qty, "to_address", "message", expire_time, "evr_change_address", "asset_change_address")
client.transferfromaddresses("asset_name", ["from_addresses"], qty, "to_address", "message", expire_time, "evr_change_address", "asset_change_address")

""" == Blockchain == """

client.clearmempool()
client.decodeblock("blockhex")
client.getbestblockhash()
client.getblock("blockhash", verbosity) 
client.getblockchaininfo()
client.getblockcount()

client.getblockhash(height)
client.getblockhashes(timestamp)
client.getblockheader("hash", verbose)
client.getchaintips()
client.getchaintxstats(nblocks, blockhash)
client.getdifficulty()
client.getmempoolancestors(txid, verbose)
client.getmempooldescendants(txid, verbose)
client.getmempoolentry(txid)
client.getmempoolinfo()
client.getrawmempool(verbose)
client.getspentinfo()
client.gettxout("txid", n, include_mempool)
client.gettxoutproof(["txid",...], blockhash)
client.gettxoutsetinfo()
client.preciousblock("blockhash")
client.pruneblockchain()
client.savemempool()
client.verifychain(checklevel, nblocks)
client.verifytxoutproof("proof")

""" == Control == """

client.getinfo()
client.getmemoryinfo("mode")
client.getrpcinfo()
client.help("command")
client.stop()
client.uptime()

""" == Generating == """

client.generate(nblocks, maxtries)
client.generatetoaddress(nblocks, address, maxtries)
client.getgenerate()
client.setgenerate(generate, genproclimit)

""" == Messages == """

client.clearmessages()
client.sendmessage("channel_name", "ipfs_hash", expire_time)
client.subscribetochannel()
client.unsubscribefromchannel()
client.viewallmessagechannels()
client.viewallmessages()

""" == Mining == """

client.getblocktemplate(TemplateRequest)
client.getevrprogpowhash("header_hash", "mix_hash", nonce, height, "target")
client.getmininginfo()
client.getnetworkhashps(nblocks, height)
client.pprpcsb("header_hash", "mix_hash", "nonce")
client.prioritisetransaction(txid, dummy_value, fee_delta)
client.submitblock("hexdata", "dummy")

""" == Network == """

client.addnode("node", "add|remove|onetry")
client.clearbanned()
client.disconnectnode("[address]", nodeid)
client.getaddednodeinfo("node")
client.getconnectioncount()
client.getnettotals()
client.getnetworkinfo()
client.getpeerinfo()
client.listbanned()
client.ping()
client.setban("subnet", "add|remove", bantime, absolute)
client.setnetworkactive(true|false)

""" == Rawtransactions == """

client.combinerawtransaction(["hexstring",...])
client.createrawtransaction([{"txid":"id","vout":n},...] {"address":(amount or object),"data":"hex",...})
client.decoderawtransaction("hexstring")
client.decodescript("hexstring")
client.fundrawtransaction("hexstring", options)
client.getrawtransaction("txid", verbose)
client.sendrawtransaction("hexstring", allowhighfees)
client.signrawtransaction("hexstring", [{"txid":"id","vout":n,"scriptPubKey":"hex","redeemScript":"hex"},...] ["privatekey1",...] sighashtype)
client.testmempoolaccept(["rawtxs"], allowhighfees)

""" == Restricted assets == """

client.addtagtoaddress("tag_name", "to_address", "change_address", "asset_data")
client.checkaddressrestriction("address", "restricted_name")
client.checkaddresstag("address", "tag_name")
client.checkglobalrestriction("restricted_name")
client.freezeaddress("asset_name", "address", "change_address", "asset_data")
client.freezerestrictedasset("asset_name", "change_address", "asset_data")
client.getverifierstring("restricted_name")
client.issuequalifierasset("asset_name", qty, "to_address", "change_address", has_ipfs, "ipfs_hash")
client.issuerestrictedasset("asset_name", qty, "verifier", "to_address", "change_address", units, reissuable, has_ipfs, "ipfs_hash")
client.isvalidverifierstring("verifier_string")
client.listaddressesfortag("tag_name")
client.listaddressrestrictions("address")
client.listglobalrestrictions()
client.listtagsforaddress("address")
client.reissuerestrictedasset("asset_name", qty, "to_address", "change_verifier", "new_verifier", "change_address", new_units, reissuable, "new_ipfs")
client.removetagfromaddress("tag_name", "to_address", "change_address", "asset_data")
client.transferqualifier("qualifier_name", qty, "to_address", "change_address", "message", expire_time)
client.unfreezeaddress("asset_name", "address", "change_address", "asset_data")
client.unfreezerestrictedasset("asset_name", "change_address", "asset_data")

""" == Restricted == """

client.viewmyrestrictedaddresses()
client.viewmytaggedaddresses()

""" == Rewards == """

client.cancelsnapshotrequest("asset_name", block_height)
client.distributereward("asset_name", snapshot_height, "distribution_asset_name", gross_distribution_amount, "exception_addresses", "change_address", "dry_run")
client.getdistributestatus("asset_name", snapshot_height, "distribution_asset_name", gross_distribution_amount, "exception_addresses")
client.getsnapshotrequest("asset_name", block_height)
client.listsnapshotrequests("asset_name", block_height)
client.requestsnapshot("asset_name", block_height)

""" == Util == """

client.createmultisig(nrequired, ["key",...])
client.estimatefee(nblocks)
client.estimatesmartfee(conf_target, estimate_mode)
client.signmessagewithprivkey("privkey", "message")
client.validateaddress("address")
client.verifymessage("address", "signature", "message")

""" == Wallet == """

client.abandontransaction("txid")
client.abortrescan()
client.addmultisigaddress(nrequired, ["key",...], "account")
client.addwitnessaddress("address")
client.backupwallet("destination")
client.bumpfee(has been deprecated on the EVR Wallet.)
client.dumpprivkey("address")
client.dumpwallet("filename")
client.encryptwallet("passphrase")
client.getaccount("address")
client.getaccountaddress("account")
client.getaddressesbyaccount("account")
client.getbalance("account", minconf, include_watchonly)
client.getmasterkeyinfo()
client.getmywords("account")
client.getnewaddress("account")
client.getrawchangeaddress()
client.getreceivedbyaccount("account", minconf)
client.getreceivedbyaddress("address", minconf)
client.gettransaction("txid", include_watchonly)
client.getunconfirmedbalance()
client.getwalletinfo()
client.importaddress("address", "label", rescan, p2sh)
client.importmulti("requests", "options")
client.importprivkey("privkey", "label", rescan)
client.importprunedfunds()
client.importpubkey("pubkey", "label", rescan)
client.importwallet("filename")
client.keypoolrefill(newsize)
client.listaccounts(minconf, include_watchonly)
client.listaddressgroupings()
client.listlockunspent()
client.listreceivedbyaccount(minconf, include_empty, include_watchonly)
client.listreceivedbyaddress(minconf, include_empty, include_watchonly)
client.listsinceblock("blockhash", target_confirmations, include_watchonly, include_removed)
client.listtransactions("account", count, skip, include_watchonly)
client.listunspent(minconf, maxconf, ["addresses",...], include_unsafe, query_options)
client.listwallets()
client.lockunspent(unlock, [{"txid":"txid","vout":n},...])
client.move("fromaccount", "toaccount", amount, minconf, "comment")
client.removeprunedfunds("txid")
client.rescanblockchain("start_height", "stop_height")
client.sendfrom("fromaccount", "toaddress", amount, minconf, "comment", "comment_to")
client.sendfromaddress("from_address", "to_address", amount, "comment", "comment_to", subtractfeefromamount, replaceable, conf_target, "estimate_mode")
client.sendmany("fromaccount", {"address":amount,...}, minconf, "comment", ["address",...], replaceable, conf_target, "estimate_mode")
client.sendtoaddress("address", amount, "comment", "comment_to", subtractfeefromamount, replaceable, conf_target, "estimate_mode")
client.setaccount("address", "account")
client.settxfee(amount)
client.signmessage("address", "message")
