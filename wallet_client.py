import requests
import json

class WalletClient:
    def __init__(self, config):
        self.url = "http://"+config["rpcuser"]+":"+config["rpcpassword"]+"@"+config["rpchost"]+":"+config["rpcport"]+"/"
        self.headers = {'content-type': 'application/json'}

    def getaddressesbyaccount(self, user_id):
        print("getaddressesbyaccount")

        request = {
            "jsonrpc": "2.0",
            "method": "getaddressesbyaccount",
            "params": [user_id],
            "id": 1
        }
        response = requests.post(self.url, data=json.dumps(request), headers=self.headers).json()
        print(response)
        if response["error"]:
            raise Exception(response["error"])

        return response["result"]

    def getnewaddress(self, user_id):
        print("getnewaddress")

        request = {
            "jsonrpc": "2.0",
            "method": "getnewaddress",
            "params": [user_id],
            "id": 1
        }
        response = requests.post(self.url, data=json.dumps(request), headers=self.headers).json()
        print(response)
        if response["error"]:
            raise Exception(response["error"])

        return response["result"]

    def getbalance(self, user_id):
        print("getbalance")
        request = {
            "jsonrpc": "2.0",
            "method": "getbalance",
            "params": [user_id],
            "id": 1
        }
        response = requests.post(self.url, data=json.dumps(request), headers=self.headers).json()
        print(response)
        if response["error"]:
            raise Exception(response["error"])

        return response["result"]

    def deposit(self, sender_user_id, amount):
        #todo amauntをユーザーから管理者のwalletに移す
        print("deposit")

    def withdraw(self, sender_user_id, sender_user_screen_name, amount):
        print("withdraw")

    def tip(self, sender_user_id, sender_user_screen_name, amount):
        print("tip")

    def rain(self, sender_user_id, sender_user_screen_name, amount):
        print("rain")

    def donate(self, sender_user_id, sender_user_screen_name, amount):
        print("donate")

