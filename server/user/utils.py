from django.conf import settings
import requests

def get_eth_balance(wallet_address):
    api_key = settings.ETHERSCAN_API_KEY
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "1":
        balance_wei = int(data["result"])
        balance_eth = balance_wei / 10**18
        return balance_eth
    else:
        raise Exception(f"Error fetching balance: {data['message']}")

