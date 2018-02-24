# twitter client
Require Python 3.6.4

```bash
# Botの起動
pipenv run python bot.py
```

# Walletについて
## 設定ファイル
```bash
vi ~/.sprouts/sprouts.conf

rpcuser=*****
rpcpassword=*****
rpcport=*****
rpcallowip=***** # RPC接続を許可するIP
```

## コマンド
```bash
cd ~/sprouts/src

# デーモンの起動
./sproutsd -daemon

# デーモンの停止
./sproutsd stop
```

## Curl例
```bash
$ ~/sprouts/src
$ curl -s -X POST --data '{"jsonrpc":"2.0","id":1,"method":"getbalance","params":[""]}' -H '{"content-type": "application/json"}' http://moya4:moya4pass@127.0.0.1:8332/
{"result":0.00000000,"error":null,"id":1}
```

# 参考リンク
* [Bitcoin ClockUpMemo](http://bitcoin.clock-up.jp/)
* [SPRTS(Sprouts)コインのWalletをUbuntu 16.04でビルドする(daemon編)](http://kozilla.hatenablog.com/entry/2018/01/24/173546)
* [Bitcoin WalletのWiki](https://en.bitcoin.it/wiki/Running_Bitcoin)