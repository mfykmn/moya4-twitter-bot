import requests

# External package
from requests_oauthlib import OAuth1

class TwitterClient:
    def __init__(self, config):
        self.bot_name = "@tip_moya4_bot"
        self.__oauth = OAuth1(config["apikey"], config["apisecret"], config["token"], config["tokensecret"])

        # Twitter全体のタイムラインからデータを取得するAPI
        self.__public_streams_url = "https://stream.twitter.com/1.1/statuses/filter.json"
        # リプライを送るAPI
        self.__public_reply_api_url = "https://api.twitter.com/1.1/statuses/update.json"

    def stream_bot_timeline(self):
        return requests.post(
            self.__public_streams_url,
            auth=self.__oauth,
            stream=True,
            data={"track": self.bot_name}
        )

    def reply(self, text, tweet_id_str):
        params = {
            "status": text,
            "in_reply_to_status_id": tweet_id_str,
            "auto_populate_reply_metadata": "true"
        }

        return requests.post(
            self.__public_reply_api_url,
            auth=self.__oauth,
            data=params,
        )
