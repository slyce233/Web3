import json
from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


#  compile solidity program

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# output compiled solidity code in json
with open("compilerd_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/1e4f9967ed4746c6bfeca99b110424f9")
)
chain_id = 4
address = "0x499c73344f19F4319494Ec8206B1eC65245559e1"
private_key = os.getenv("PRIVATE_KEY")

# create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(address)

# 1. build transaction
# 2. sign transaction
# 3. send transaxction

transaction_data = {
    "chainId": chain_id,
    "from": address,
    "nonce": nonce,
    "gasPrice": w3.eth.gas_price,
}

# build
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

# sign
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)


print("Deploying Contract...")

# send
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract Deployed!")

# Working with contract you need:
# 1. Contract ABI
# 2. Contract Address

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#  Call -> Simulate making the call and getting a return value
#  Transact -> Actually make state change

print(simple_storage.functions.retrieve().call())
print("Updating Contract...")

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("Contract Updated!")
print(simple_storage.functions.retrieve().call())
