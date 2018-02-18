# twitter client
Require Python 3.6.4

```bash
# Botの起動
pipenv run python bot.py
```


# Walletについて
## コマンド
```bash
cd ~/sprouts/src

# デーモンの起動
./sproutsd -daemon

# デーモンの停止
./sproutsd stop
```

## 設定ファイル
```bash
vi ~/.sprouts/sprouts.conf

rpcuser=*****
rpcpassword=*****
rpcport=*****
```

## Curl例
```bash
$ ~/sprouts/src$ curl -s -X POST --data '{"jsonrpc":"2.0","id":1,"method":"getbalance","params":[""]}' -H '{"content-type": "application/json"}' http://moya4:moya4pass@127.0.0.1:8332/
{"result":0.00000000,"error":null,"id":1}
```
# 参考リンク
* http://kozilla.hatenablog.com/entry/2018/01/24/173546