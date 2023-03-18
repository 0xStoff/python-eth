import asyncio
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from websockets.legacy.client import connect
from env_config import INFURA_WS_URL, TEST_ADDRESS, TEST_PRIVATE_KEY, MM_ADDRESS


# Setup Web3 instance
def setup_web3(infura_url):
    w3 = Web3(Web3.HTTPProvider(infura_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


# Main event loop to monitor and process transactions
async def get_event(w3, test_address, test_private_key, mm_address, gas_price, gas_limit):
    async with connect(w3.provider.endpoint_uri) as ws:
        # Subscribe to new pending transactions
        await ws.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
        last_block_number = None

        while True:
            try:
                # Print current block number if changed
                current_block_number = w3.eth.block_number
                if current_block_number != last_block_number:
                    print(f"Current block number: {current_block_number}")
                    last_block_number = current_block_number

                # Get incoming tx details
                message = await ws.recv()
                response = json.loads(message)
                tx_hash = response['params']['result']
                tx = w3.eth.get_transaction(tx_hash)

                # Process incoming transaction
                if tx is not None and tx['to'] == test_address:
                    print(f"Incoming transaction detected: {tx.hash.hex()}")
                    print(f"Waiting for the incoming transaction ({tx.hash.hex()}) to be mined...")
                    w3.eth.wait_for_transaction_receipt(tx.hash)
                    print("Incoming transaction mined. Proceeding with sending the new transaction...")
                    tx_hash_hex = send_out_ether(w3, test_address, test_private_key, mm_address, gas_price, gas_limit)
                    print(f"Sent Ether to {mm_address}: {tx_hash_hex}")
            except:
                pass


# Send Ether to specified address
def send_out_ether(w3, from_address, private_key, to_address, gas_price, gas_limit):
    nonce = w3.eth.get_transaction_count(from_address)
    account_balance = w3.eth.get_balance(from_address)
    total_gas_cost = gas_price * gas_limit
    max_send_value = account_balance - total_gas_cost

    if max_send_value <= 0:
        print(f"Max: {max_send_value}")
        print(f"Total Gas: {total_gas_cost}")
        print(f"Balance: {account_balance}")
        print("Error: Total gas cost is greater than or equal to the transaction value.")
        return None

    tx_params = {
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas_limit,
        'to': to_address,
        'value': max_send_value,
        'chainId': w3.eth.chain_id,
    }

    signed_tx = Account.sign_transaction(tx_params, private_key)

    try:
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash_hex = "0x" + tx_hash.hex()[2:]
        return tx_hash_hex
    except Exception as e:
        print(f"Error sending raw transaction: {str(e)}")
        return None


# Main function
def main():
    w3 = Web3(Web3.WebsocketProvider(INFURA_WS_URL))
    gas_price = w3.to_wei('1', 'gwei')
    gas_limit = 21_000

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(get_event(w3, TEST_ADDRESS, TEST_PRIVATE_KEY, MM_ADDRESS, gas_price, gas_limit))
    except KeyboardInterrupt:
        print("\nStopped monitoring transactions.")
    finally:
        loop.close()


# Entry point
if __name__ == "__main__":
    main()
