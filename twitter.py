import requests
import json

# Internal package
from commands import Command

# External package
from requests_oauthlib import OAuth1

class Twitter:
    ### Private class variable ###
    __bot_name = "@tip_moya4_bot"
    __oauth = OAuth1(
        "",
        "",
        "",
        "",
    )
    # Twitter全体のタイムラインからデータを取得するAPI
    __public_streams_url = "https://stream.twitter.com/1.1/statuses/filter.json"
    __public_reply_api_url = "https://api.twitter.com/1.1/statuses/update.json"

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

                tweet_id_str = tweet["id_str"]
                sender_user_id = tweet["user"]["id"]
                sender_user_screen_name = tweet["user"]["screen_name"]

                cmd_dict = self.__parse_command(tweet["text"])

                cmd = cmd_dict[1]

                # !もやたす
                if cmd == Command.DEPOSIT.value:
                    print('------------------------DEPOSITコマンド')
                    print(cmd)
                    print(sender_user_id)
                    print(sender_user_screen_name)
                    a = self.__reply("@" + sender_user_screen_name +"!もやたすコマンドが実行されましたaaavvaa", tweet_id_str)
                    print(a)

                # !出荷
                elif cmd == Command.TIP.value:
                    print('------------------------TIPコマンド')

                    receiver_users = self.__get_receiver_users(tweet, cmd_dict[2][1:])
                    ammount = cmd_dict[3]

                    print(cmd)
                    print(receiver_users)
                    print(ammount)
                    print(sender_user_id)
                    print(sender_user_screen_name)
                # !水やり
                elif cmd == Command.RAIN.value:
                    print('------------------------RAINコマンド')

                    ammount = cmd_dict[2]

                    print(cmd)
                    print(ammount)
                    print(sender_user_id)
                    print(sender_user_screen_name)
                else:
                    print("------------------------存在しないコマンドです")

            except:
                pass


    def __parse_command(self, tweet_text):
        tweet_text_dict = tweet_text.split(" ")
        if tweet_text_dict[0] != self.__bot_name:
            raise Exception("コマンド実行の形式を確認してね")

        return tweet_text_dict


    def __get_receiver_users(self, tweet, receiver_screen_name):
        for mention in tweet["entities"]["user_mentions"]:
            if mention["screen_name"] == receiver_screen_name:
                return {
                    "id": mention["id"],
                    "screen_name": mention["screen_name"]
                }

        raise Exception("not match receiver_user")

    def __reply(self, text, tweet_id_str):
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


if __name__ == '__main__':
    twitter = Twitter()
    twitter.run_worker()
