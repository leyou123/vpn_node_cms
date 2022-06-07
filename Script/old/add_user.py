import requests
import json
import redis
import time
import threading
REDIS_HOST = "3.101.139.105"
REDIS_PASSWORD = "leyou2020"
pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, password=REDIS_PASSWORD, db=15)
r = redis.Redis(connection_pool=pool)


class User(object):

    @classmethod
    def query(cls):
        url = "https://9527.click/api/v1/user/query"
        response = requests.post(url=url)
        if response.status_code == 200:
            datas = json.loads(response.text)
            user_datas = datas.get("data")
            for user in user_datas:
                uuid = user.get("uuid", "")
                r.lpush("users", uuid)

    @classmethod
    def create(cls,uuid):

        all_ip = ['108.160.130.104','149.248.51.249']

        for ip in all_ip:
            data = {"password": uuid,"ip":ip}
            url = "https://nodes.9527.click/user/create_single_user"
            response = requests.post(url=url, data=data)
            print(response.status_code,ip, uuid)

    @classmethod
    def processing_data(cls):
        while True:
            try:
                redis_data = r.lpop("users")
                if not redis_data:
                    break
                uuid = str(redis_data, "utf-8")
                cls.create(uuid)
            except Exception as e:
                print(e)
                break


def main():
    User.query()
    for i in range(10):
        t = threading.Thread(target=User.processing_data, name=f'LoopThread{i}')
        t.start()


if __name__ == '__main__':
    main()
