import requests
import json

from requests_oauthlib import OAuth1

OAUTH = OAuth1(
    "",
    "",
    "",
    "",
)

BOT_NAME = "tip_moya4_bot"

def receive_tweet():
    url = "https://stream.twitter.com/1.1/statuses/filter.json"

    r = requests.post(url, auth=OAUTH, stream=True, data={"track": "@" + BOT_NAME})
    for line in r.iter_lines():
        try:
            if line == '':
                # is not JSON. Skip
                pass

            tweet = json.loads(line.decode("utf-8"))
            command = split_command(tweet["text"])
            print(command)


            users = get_users(tweet, command["send_destination"])
            print(users)

        except:
            pass

def split_command(tweet_text):
    res = tweet_text.split(" ")
    if res[0] != "@" + BOT_NAME:
        raise Exception("fail split")

    return {
        "command": res[1],
        "send_destination": res[2][1:],
        "amount": res[3]
    }

def get_users(tweet, receiver_screen_name):
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
    receive_tweet()