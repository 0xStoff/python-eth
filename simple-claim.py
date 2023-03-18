from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from dotenv import load_dotenv
import os
from abi import contract_abi

# Load environment variables from .env file
load_dotenv()

infura_url = os.getenv("INFURA_URL")
contract_address = os.getenv("CONTRACT_ADDRESS")
address = os.getenv("TEST_ADDRESS")
private_key = os.getenv("TEST_ADDRESS_PRIVATE_KEY")

# Set up Web3 connection
w3 = Web3(Web3.HTTPProvider(infura_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load your account
account = w3.eth.account.from_key(private_key)

# Load the contract ABI
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Construct the transaction
nonce = w3.eth.get_transaction_count(address)
gas_price = w3.to_wei('50', 'gwei')
gas_limit = 100000
tx_params = {
    'nonce': nonce,
    'gasPrice': gas_price,
    'gas': gas_limit,
    'to': contract_address,
    'value': 0,
    'data': contract.encodeABI(fn_name='claim'),
    'chainId': w3.eth.chain_id,
}
signed_tx = Account.sign_transaction(tx_params, private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for the transaction to be mined
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Tokens claimed!")
