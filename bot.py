import json
import toml

# Internal package
from twitter_client import TwitterClient
from wallet_client import WalletClient
from db_client import DBClient
from commands import Command

config_path = './_config/development.toml'
fee = 0.01 # 手数料

def get_receiver_user_id_str(tweet, receiver_screen_name):
    for mention in tweet["entities"]["user_mentions"]:
        if mention["screen_name"] == receiver_screen_name:
            return mention["id"]

    raise Exception("not match receiver_user")


if __name__ == '__main__':
    config = toml.load(open(config_path))

    t_client = TwitterClient(config["twitter"])
    w_client = WalletClient(config["wallet"])
    d_client = DBClient(config["database"])

    print("Worker Run")

    timeline = t_client.stream_bot_timeline()
    for line in timeline.iter_lines():
        try:
            tweet = json.loads(line.decode("utf-8"))

            tweet_id_str = tweet["id_str"] # リプライ時に利用する
            sender_user_id_str = tweet["user"]["id_str"]
            sender_user_screen_name = tweet["user"]["screen_name"]
            tweet_dict = tweet["text"].split(" ")

            # Botへのメンションチェック
            if tweet_dict[0] != t_client.bot_name:
                t_client.reply(
                    "@" + sender_user_screen_name + " コマンド実行の形式を確認してね", tweet_id_str)
                break

            print(tweet_dict[1])
# --- コマンド:@tip_moya4_bot !開園
            if tweet_dict[1] == Command.REGSTER.value:
                try:
                    user = d_client.getUser(sender_user_id_str)
                    if user is None:
                        # アドレス生成
                        addr = w_client.getnewaddress(sender_user_id_str)
                        # DB登録
                        d_client.createUser(sender_user_id_str, addr)

                        msg = "@{screen_name}さん もやしファームが開園されましたよ！\n" \
                              + "🏦 アドレス：{address}\n"
                        formatted_msg = msg.format(
                            screen_name=sender_user_screen_name,
                            address=addr,
                        )

                        # 結果をリプライ
                        t_client.reply(formatted_msg, tweet_id_str)
                    else:
                        t_client.reply(
                            "@" + sender_user_screen_name + " もう開園済みだよ", tweet_id_str)
                except:
                    t_client.reply(
                        "@" + sender_user_screen_name + " エラー発生", tweet_id_str)
# --- コマンド:@tip_moya4_bot !もやたす
            elif tweet_dict[1] == Command.BALANCE.value:
                try:
                    user = d_client.getUser(sender_user_id_str)
                    print(user)
                    if user is not None:
                        # 保持コインの確認
                        balance = w_client.getbalance(sender_user_id_str)

                        msg = "@{screen_name}さんの育成状況だよ。栽培がんばろー！\n" \
                            + "🏦 アドレス：{address}\n" \
                            + "🛒 出荷待ち：{balance}もやし\n" \
                            + "🌱 栽培中　： {cultivation_coins}もやし\n" \
                            + "💧 総水やり量：{total_rain}\n" \
                            + "👑 水やりランク：TODO位"
                        formatted_msg = msg.format(
                            screen_name=sender_user_screen_name,
                            address=user[1],
                            balance=str(balance),
                            cultivation_coins=str(user[2]),
                            total_rain=str(user[3]),
                        )

                        # 結果をリプライ
                        t_client.reply(formatted_msg, tweet_id_str)
                    else:
                        t_client.reply(
                            "@" + sender_user_screen_name + " アドレスが存在しません。開園を行ってください", tweet_id_str)
                except:
                    t_client.reply(
                        "@" + sender_user_screen_name + " エラー発生", tweet_id_str)
# --- コマンド:@tip_moya4_bot !種まき [数量]
            elif tweet_dict[1] == Command.DEPOSIT.value:
                amount = float(tweet_dict[2])

                try:
                    user = d_client.getUser(sender_user_id_str)
                    # ユーザー存在チェック
                    if user is None:
                        t_client.reply(
                            "@" + sender_user_screen_name + " アドレスが存在しません。開園を行ってください", tweet_id_str)
                        break

                    # 保持コインの確認
                    balance = w_client.getbalance(sender_user_id_str)
                    if amount + fee < balance:
                        t_client.reply(
                            "@" + sender_user_screen_name + " 出荷待ちのもやしが不足しています。", tweet_id_str)
                        break

                    # 個人のwalletから共有walletにコインを移す
                    w_client.deposit(sender_user_id_str, amount)
                    # 移した分だけDBの栽培中のコインを増やす
                    before_cultivation_coins = user[2]
                    update_cultivation_coins = before_cultivation_coins + amount
                    d_client.updateUserCultivationCoins(sender_user_id_str, update_cultivation_coins)

                    msg = "@{screen_name} {amount}もやし種まきしました！\n" \
                          + "🛒 出荷待ち：{balance}もやし\n" \
                          + "🌱 栽培中　： {cultivation_coins}もやし\n"

                    formatted_msg = msg.format(
                        screen_name=sender_user_screen_name,
                        amount=amount,
                        balance=str(balance - amount),
                        cultivation_coins=str(update_cultivation_coins),
                    )

                    # 結果をリプライ
                    t_client.reply(formatted_msg, tweet_id_str)
                except:
                    t_client.reply("@" + sender_user_screen_name + " エラー発生", tweet_id_str)

# --- コマンド:@tip_moya4_bot !収穫 [数量]
            elif tweet_dict[1] == Command.WITHDRAW.value:
                amount = tweet_dict[2]

                # コインを残高から出金する
                w_client.withdraw(sender_user_id_str, sender_user_screen_name, amount)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !収穫 コマンドの結果", tweet_id_str)
                print(res)
# --- コマンド:@tip_moya4_bot !出荷 [メンション／アドレス] [数量]
            elif tweet_dict[1] == Command.TIP.value:
                amount = float(tweet_dict[3])

                try:
                    # 送信先アドレスの取得
                    to_address = ""
                    if "@" == tweet_dict[2][:1]:
                        # メンション指定だった場合
                        receiver_users_id_str = get_receiver_user_id_str(tweet, tweet_dict[2][1:])
                        user = d_client.getUser(receiver_users_id_str)
                        # ユーザー存在チェック
                        if user is None:
                            t_client.reply(
                                "@" + sender_user_screen_name + " 送信先メンションのアドレスが存在しません", tweet_id_str)
                            break

                        to_address = user[1]
                    else:
                        # アドレス指定だった場合
                        to_address = tweet_dict[2]


                    user = d_client.getUser(sender_user_id_str)
                    # ユーザー存在チェック
                    if user is None:
                        t_client.reply(
                            "@" + sender_user_screen_name + " アドレスが存在しません。開園を行ってください", tweet_id_str)
                        break

                    # 保持コインの確認
                    balance = w_client.getbalance(sender_user_id_str)
                    if amount + fee < balance:
                        t_client.reply(
                            "@" + sender_user_screen_name + " 出荷待ちのもやしが不足しています。", tweet_id_str)
                        break

                    # コインをメンション or アドレスに送金する
                    w_client.sendfrom(sender_user_id_str, to_address, amount)

                    msg = "@{screen_name} {amount}もやし出荷しました！\n" \
                          + "🛒 出荷待ち：{balance}もやし\n" \

                    formatted_msg = msg.format(
                        screen_name=sender_user_screen_name,
                        amount=amount,
                        balance=str(balance - amount),
                    )

                    # 結果をリプライ
                    t_client.reply(formatted_msg, tweet_id_str)


                except:
                    t_client.reply("@" + sender_user_screen_name + " エラー発生", tweet_id_str)

# --- コマンド:@tip_moya4_bot !水やり [数量]
            elif tweet_dict[1] == Command.RAIN.value:
                amount = tweet_dict[2]

                # 全twitterアドレスに対してコインを配布する
                w_client.rain(sender_user_id_str, sender_user_screen_name, amount)

                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " TODO: !水やり コマンドの結果", tweet_id_str)
                print(res)
# --- コマンド:@tip_moya4_bot !ヘルプ
            elif tweet_dict[1] == Command.HELP.value:
                msg1 = "@" + sender_user_screen_name + " もやしファームの使い方を説明するよ🌱 その1\n\n" \
                      + "!開園\nもやしファームの開園ができるよ。最初に実施してね。\n\n" \
                      + "!もやたす\nファームの状況をお知らせするよ。\n\n" \
                      + "!種まき [数量]\n出荷待ちのもやしを使って、栽培ができるよ"

                msg2 = "@" + sender_user_screen_name + " もやしファームの使い方を説明するよ🌱 その２\n\n" \
                       + "!収穫 [数量]\n栽培中のもやしを、出荷待ちにするよ。\n\n" \
                       + "!出荷 [メンション／アドレス] [数量]\n出荷待ちのもやしを、宛先に出荷するよ。\n\n" \
                       + "!水やり [数量]\n栽培中のもやしで、他のファームに水やりができるよ。"

                # 結果をリプライ
                t_client.reply(msg1, tweet_id_str)
                t_client.reply(msg2, tweet_id_str)
# --- コマンド:存在しない
            else:
                # 結果をリプライ
                res = t_client.reply(
                    "@" + sender_user_screen_name + " 存在しないコマンドです", tweet_id_str)
                print(res)

        except:
            pass
