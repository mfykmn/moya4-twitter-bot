import psycopg2

class DBClient:
    def __init__(self, config):
        dsn = "postgresql://"+config["user"]+":"+config["password"]+"@"+config["host"]+":"+config["port"]+"/moya4"
        self.conn = psycopg2.connect(dsn)

    def getUser(self, twitter_user_id):
        cur = self.conn.cursor()
        cur.execute("select * from users where twitter_user_id=%s", (twitter_user_id,))
        print(cur.fetchone())
        cur.close()

