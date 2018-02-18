import json

# Internal package
from twitter_client import TwitterClient
from wallet_client import WalletClient
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
    m_client = WalletClient()

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

            print(tweet_dict[1])
            # コマンド:@tip_moya4_bot !開園
            if tweet_dict[1] == Command.REGSTER.value:
                # アドレス生成
                m_client.register(sender_user_id, sender_user_screen_name)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !開園 コマンドの結果", tweet_id_str)
                print(res)
            # コマンド:@tip_moya4_bot !もやたす
            elif tweet_dict[1] == Command.BALANCE.value:
                # 保持コインの確認
                m_client.balance(sender_user_id, sender_user_screen_name)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !もやたす コマンドの結果", tweet_id_str)
                print(res)
            # コマンド:@tip_moya4_bot !種まき [数量]
            elif tweet_dict[1] == Command.DEPOSIT.value:
                amount = tweet_dict[2]

                # コインを残高に入金する
                m_client.deposit(sender_user_id, sender_user_screen_name, amount)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !種まき コマンドの結果", tweet_id_str)
                print(res)
            # コマンド:@tip_moya4_bot !収穫 [数量]
            elif tweet_dict[1] == Command.WITHDRAW.value:
                amount = tweet_dict[2]

                # コインを残高から出金する
                m_client.withdraw(sender_user_id, sender_user_screen_name, amount)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !収穫 コマンドの結果", tweet_id_str)
                print(res)
            # コマンド:@tip_moya4_bot !出荷 [メンション／アドレス] [数量]
            elif tweet_dict[1] == Command.TIP.value:
                receiver_users = get_receiver_users(tweet, tweet_dict[2][1:])
                amount = tweet_dict[3]

                # コインをメンション or アドレスに送金する
                m_client.tip(sender_user_id, sender_user_screen_name, receiver_users, amount)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !出荷 コマンドの結果", tweet_id_str)
                print(res)
            # コマンド:@tip_moya4_bot !水やり [数量]
            elif tweet_dict[1] == Command.RAIN.value:
                amount = tweet_dict[2]

                # 全twitterアドレスに対してコインを配布する
                m_client.rain(sender_user_id, sender_user_screen_name, amount)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !水やり コマンドの結果", tweet_id_str)
                print(res)
            else:
                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " 存在しないコマンドです", tweet_id_str)
                print(res)

        except:
            pass