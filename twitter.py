import requests
import json

from requests_oauthlib import OAuth1

OAUTH = OAuth1(
    "",
    "",
    "",
    "",
)

BOT_NAME = "mafuyuk_m"

def receive_tweet():
    url = "https://stream.twitter.com/1.1/statuses/filter.json"

    r = requests.post(url, auth=OAUTH, stream=True, data={"track": "@" + BOT_NAME})
    for line in r.iter_lines():
        try:
            if line.decode("utf-8") == '':
                print("JSONじゃないのでスキップ")
                pass

            tweet = json.loads(line.decode("utf-8"))
            print(tweet)
            print(tweet['text'])
        except:
            pass

if __name__ == '__main__':
    receive_tweet()