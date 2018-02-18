#twitter client
Require Python 3.6.4

```bash
# Botの起動
pipenv run python bot.py
```


#Walletについて
##コマンド
```bash
cd ~/sprouts/src

# デーモンの起動
./sproutsd -daemon

# デーモンの停止
./sproutsd stop
```

##設定ファイル
```bash
vi ~/.sprouts/sprouts.conf

rpcuser=*****
rpcpassword=*****
rpcport=*****
```

# 参考リンク
* http://kozilla.hatenablog.com/entry/2018/01/24/173546