import requests
import json

from requests_oauthlib import OAuth1

class Twitter:
    ### Private class variable ###
    __bot_name = "@tip_moya4_bot"
    __bot_command_template = __bot_name + " [command] [twitterアカウントまたはアドレス] [amount]"
    __oauth = OAuth1(
        "",
        "",
        "",
        "",
    )
    # Twitter全体のタイムラインからデータを取得するAPI
    __public_streams_url = "https://stream.twitter.com/1.1/statuses/filter.json"

    def __init__(self):
        print("init")

    def run_worker(self):
        print("run_worker")
        r = requests.post(
            self.__public_streams_url,
            auth=self.__oauth,
            stream=True,
            data={"track": self.__bot_name}
        )

        for line in r.iter_lines():
            try:
                tweet = json.loads(line.decode("utf-8"))
                command = self.__split_command(tweet["text"])
                print(command)


                users = self.__get_users(tweet, command["send_destination"])
                print(users)

            except:
                pass

    def __split_command(self, tweet_text):
        res = tweet_text.split(" ")
        if res[0] != self.__bot_name:
            raise Exception("コマンド実行の形式を確認してね\n" + self.__bot_command_template)

        return {
            "command": res[1],
            "send_destination": res[2][1:],
            "amount": res[3]
        }

    def __get_users(self, tweet, receiver_screen_name):
        for mention in tweet["entities"]["user_mentions"]:
            if mention["screen_name"] == receiver_screen_name:
                return {
                    "sender_user_id": tweet["user"]["id"],
                    "sender_user_screen_name": tweet["user"]["screen_name"],
                    "receiver_id": mention["id"],
                    "receiver_screen_name": mention["screen_name"]
                }

        raise Exception("not match receiver_user")

if __name__ == '__main__':
    twitter = Twitter()
    twitter.run_worker()
