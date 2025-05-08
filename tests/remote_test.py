from evrmore_rpc import EvrmoreClient
EVRMORE_RPC_HOST = "evrmail.com"
EVRMORE_RPC_PORT = 8819
RPC_USER = "evruser"
RPC_PASSWORD = "changeThisToAStrongPassword123"
client = EvrmoreClient(url=EVRMORE_RPC_HOST, rpcuser=RPC_USER, rpcpassword=RPC_PASSWORD, rpcport=EVRMORE_RPC_PORT)
print(client.getblockcount())