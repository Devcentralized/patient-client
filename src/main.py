import json
import uuid

import requests

from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.blocks.block import generate_block
from src.data_generator import DataGenerator

"""
Steps:
1. Ask for user id (public key and bank IP)
2. Generate random patient data
3. Send data to bank
4. Check bank transaction to see that JSON data is present
"""

# Get user input
print("Enter signing key: ")
signing_key = SigningKey(input().encode(), encoder=HexEncoder)
account_number = signing_key.verify_key
print("Enter bank IP: ")
bank_ip = input()

# Generate patient data
patient_data = DataGenerator().generate_patient_data(5)

# Prepare data for bank
bank_config = requests.get(f'http://{bank_ip}/config?format=json').json()
validator_ip = bank_config["primary_validator"]["ip_address"]
balance_lock = requests.get(f"http://{validator_ip}/accounts/{account_number.encode(encoder=HexEncoder).decode('UTF-8')}/balance_lock?format=json").json()["balance_lock"]


transactions = [
    {
      'amount': 1,
      'recipient': 'dc3eb7a93238a4e691817d294c97fa372748807c473130901b71b819032a2faa'
    },
    {
        'amount': int(bank_config['default_transaction_fee']),
        # 'json_data': json.dumps(patient_data),
        'fee': 'BANK',
        'recipient': bank_config['account_number'],
    },
    {
        'amount': int(bank_config['primary_validator']['default_transaction_fee']),
        'fee': 'PRIMARY_VALIDATOR',
        'recipient': bank_config['primary_validator']['account_number'],
    }
]

# Create block containing the transactions
block = generate_block(
    account_number=account_number,
    balance_lock=balance_lock,
    signing_key=signing_key,
    transactions=transactions)

print(block)

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) TNBAccountManager/1.0.0-alpha.43 Chrome/83.0.4103.122 Electron/9.4.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept-Language': 'en-US'
}

send_transactions_result = requests.request("POST", f'http://{bank_ip}/blocks', headers=headers, json=block)
print(send_transactions_result.json())
