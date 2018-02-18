import requests
import json

class WalletClient:
    def __init__(self, config):
        self.url = "http://"+config["rpcuser"]+":"+config["rpcpassword"]+"@"+config["rpchost"]+":"+config["rpcport"]+"/"
        self.headers = {'content-type': 'application/json'}

    def getnewaddress(self, sender_user_id, sender_user_screen_name):
        print("getnewaddress")

        request = {
            "jsonrpc": "2.0",
            "method": "getnewaddress",
            "params": [sender_user_id],
            "id": 1
        }
        response = requests.post(
            self.url, data=json.dumps(request), headers=self.headers).json()
        print(response)

    def balance(self, sender_user_id, sender_user_screen_name):
        print("balance")
        request = {
            "jsonrpc": "2.0",
            "method": "getbalance",
            "params": [sender_user_id],
            "id": 1
        }
        response = requests.post(
            self.url, data=json.dumps(request), headers=self.headers).json()

        print(response)

    def deposit(self, sender_user_id, sender_user_screen_name, amount):
        print("deposit")

    def withdraw(self, sender_user_id, sender_user_screen_name, amount):
        print("withdraw")

    def tip(self, sender_user_id, sender_user_screen_name, amount):
        print("tip")

    def rain(self, sender_user_id, sender_user_screen_name, amount):
        print("rain")

    def donate(self, sender_user_id, sender_user_screen_name, amount):
        print("donate")

