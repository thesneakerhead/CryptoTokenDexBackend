import os
import json
from web3 import Web3
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'contracts/SimpleStorage.sol')

from solcx import compile_standard, install_solc

with open(filename, "r") as f:
    simple_storage_file = f.read()
install_solc("0.8.0")
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)

# need bytecode and abi to deploy
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to local node

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337

# set default account private keys are for virtual environment no implications
default_address = "0x9b9ec926D922232154868Eb769e3CB10F756A3DD"
private_key = "0xbdd4ee770970fb0ad0ab13812a1bcb9412dbc151159131931ba6b48b2f0e897c"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(default_address)

# create a transaction that deploys the contract

transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice":w3.eth.gas_price,
    "chainId": chain_id,
    "from": default_address,
    "nonce": nonce,
})

# sign a transaction

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send the transaction to the network

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# get the transaction hash from the network
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


# Can call or transact with the contract 
# call equivalent to getter function
# transact equivalent to setter function
print(simple_storage.functions.retrieve().call())
store_transaction = simple_storage.functions.store(15).build_transaction({
    "gasPrice":w3.eth.gas_price,
    "chainId": chain_id,
    "from": default_address,
    "nonce": nonce + 1,
})
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

store_tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

