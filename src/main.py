from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.blocks.block import generate_block
from thenewboston.blocks.signatures import generate_signature
from thenewboston.accounts.manage import create_account
"""
Steps:
1. Ask for user id (public key)
2. Generate random patient data
3. Send data to bank
4. Check bank transaction to see that JSON data is present
"""

print("Enter signing key: ")
signing_key = SigningKey(input().encode(), encoder=HexEncoder)
account_number = signing_key.verify_key

# TODO: add reference to the data generation package
patient_data = {
    "patient": "Test"
}

balance_lock = "test"
transactions = []

block = generate_block(
    account_number=account_number,
    balance_lock=balance_lock,
    signing_key=signing_key,
    transactions=transactions)

print(block)
