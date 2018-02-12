import json

# Internal package
from twitter_client import TwitterClient
from commands import Command

def get_receiver_users(tweet, receiver_screen_name):
    for mention in tweet["entities"]["user_mentions"]:
        if mention["screen_name"] == receiver_screen_name:
            return {
                "id": mention["id"],
                "screen_name": mention["screen_name"]
            }

    raise Exception("not match receiver_user")


if __name__ == '__main__':
    t_client = TwitterClient()

    timeline = t_client.stream_bot_timeline()
    for line in timeline.iter_lines():
        try:
            tweet = json.loads(line.decode("utf-8"))

            tweet_id_str = tweet["id_str"]
            sender_user_id = tweet["user"]["id"]
            sender_user_screen_name = tweet["user"]["screen_name"]
            tweet_dict = tweet["text"].split(" ")

            # Botへのメンションチェック
            if tweet_dict[0] != t_client.bot_name:
                raise Exception("コマンド実行の形式を確認してね")

            # コマンド:@tip_moya4_bot !もやたす
            if tweet_dict[1] == Command.DEPOSIT.value:
                print(sender_user_id)
                print(sender_user_screen_name)
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !もやたす コマンドの結果", tweet_id_str)
                print(res)
            # コマンド:@tip_moya4_bot !出荷 [量] [アドレス or @Twitterアカウント]
            elif tweet_dict[1] == Command.TIP.value:
                receiver_users = get_receiver_users(tweet, tweet_dict[2][1:])
                amount = tweet_dict[3]

                print(receiver_users)
                print(amount)
                print(sender_user_id)
                print(sender_user_screen_name)

                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !出荷 コマンドの結果", tweet_id_str)
                print(res)
            # コマンド:@tip_moya4_bot !水やり [量]
            elif tweet_dict[1] == Command.RAIN.value:
                amount = tweet_dict[2]

                print(amount)
                print(sender_user_id)
                print(sender_user_screen_name)
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !水やり コマンドの結果", tweet_id_str)
                print(res)
            else:
                res = t_client.reply(
                    "@" + sender_user_screen_name + " 存在しないコマンドです", tweet_id_str)
                print(res)

        except:
            pass
