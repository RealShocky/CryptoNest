import requests
import json
import stellar_sdk as s_sdk

class PiNetwork:
    api_key = ""
    server = ""
    keypair = ""
    fee = ""

    def initialize(self, api_key, wallet_private_key, network):
        try:
            if not self.validate_private_seed_format(wallet_private_key):
                raise ValueError("Invalid private seed format")
            self.api_key = api_key
            self.load_account(wallet_private_key, network)
            self.fee = self.server.fetch_base_fee()
            return True
        except Exception as e:
            raise Exception("Error initializing PiNetwork: " + str(e))

    def get_balance(self):
        try:
            balances = self.server.accounts().account_id(self.keypair.public_key).call()["balances"]
            for balance in balances:
                if balance["asset_type"] == "native":
                    return float(balance["balance"])
            return 0
        except Exception as e:
            raise Exception("Error fetching balance: " + str(e))

    def create_payment(self, amount, memo=''):
        try:
            transaction = self.build_transaction(amount, memo)
            response = self.submit_transaction(transaction)
            payment_id = response["id"]
            return payment_id
        except Exception as e:
            raise Exception("Error creating payment: " + str(e))

    def load_account(self, private_seed, network):
        try:
            self.keypair = s_sdk.Keypair.from_secret(private_seed)
            if network == "Pi Network":
                horizon = "https://api.mainnet.minepi.com"
            else:
                horizon = "https://api.testnet.minepi.com"
            self.server = s_sdk.Server(horizon)
            self.account = self.server.load_account(self.keypair.public_key)
        except Exception as e:
            raise Exception("Error loading account: " + str(e))

    def fetch_base_fee(self):
        try:
            base_fee = self.server.fetch_base_fee()
            return base_fee
        except Exception as e:
            raise Exception("Error fetching base fee: " + str(e))

    def build_transaction(self, amount, memo=''):
        try:
            fee = self.fee
            transaction = (
                s_sdk.TransactionBuilder(
                    source_account=self.account,
                    network_passphrase=self.server.network_passphrase,
                    base_fee=fee,
                )
                .add_text_memo(memo)
                .append_payment_op(self.keypair.public_key, s_sdk.Asset.native(), str(amount))
                .set_timeout(180)
                .build()
            )
            return transaction
        except Exception as e:
            raise Exception("Error building transaction: " + str(e))

    def submit_transaction(self, transaction):
        try:
            transaction.sign(self.keypair)
            response = self.server.submit_transaction(transaction)
            return response
        except Exception as e:
            raise Exception("Error submitting transaction: " + str(e))

    def validate_private_seed_format(self, seed):
        try:
            if not seed.upper().startswith("S"):
                return False
            elif len(seed) != 56:
                return False
            return True
        except Exception as e:
            raise Exception("Error validating private seed format: " + str(e))
