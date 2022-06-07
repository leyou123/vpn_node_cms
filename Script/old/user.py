import re
import subprocess
import time
import redis
from json import load
from urllib.request import urlopen
import random
import string
import json
import hashlib

path = "/root"
redis_host = "18.144.125.117"

pool = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=0)
pool1 = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=1)
pool3 = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=3)
pool4 = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=4)

r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r3 = redis.Redis(connection_pool=pool3)
r4 = redis.Redis(connection_pool=pool4)

ipaddr = load(urlopen("http://httpbin.org/ip"))["origin"]


def add_user(name, port, password):
    """
        通过脚本创建用户
    """
    try:
        s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        run_option = [
            "7",  # 选择用户配置
            "1",  # 选择增加用户
            str(name),  # 输入用户名
            str(port),  # 输入用户端口
            str(password),  # 输入用户密码
            "10",  # 选择协议
            "2",  # 协议插件
            "y",  # 是否兼容
            "1",  # 选择混淆
            " ",  # 连接数量
            " ",  # 单线程流量
            " ",  # 多线程流量
            " ",  # 流量上限
            " ",  # 禁止端口
            "n"  # 是否继续
        ]

        for i in run_option:
            s.stdin.write(bytes(i + "\n", encoding="utf-8"))
        s.stdin.close()

        out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
        # print(out)
        s.stdout.close()
    except Exception as e:
        print(e)
        return False
    return True


def getStrAsMD5(parmStr):
    """
        str 转Md5
    """
    if isinstance(parmStr, str):
        # 如果是unicode先转utf-8
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()


def generate_user_data():
    """
        生成用户数据
    """

    for i in range(10):
        password = "".join(random.sample(string.ascii_letters + string.digits, 20))
        name = "TEMP" + "".join(random.sample(string.ascii_letters + string.digits, 20))
        port = str(random.randint(1024, 65535))
        md5_value = f"{name}{port}{ipaddr}"
        md5_conv_value = getStrAsMD5(md5_value)
        redis_data = r3.get(md5_conv_value)
        if not redis_data:
            data = {"ipaddr": ipaddr, "password": password, "name": name, "port": port,"time":int(time.time())}
            r3.set(md5_conv_value, json.dumps(data))
            return data


def add_temp_user(number):
    """
        添加临时用户
    """

    node_number = 20
    median = node_number / 2

    count = 0
    if not number:
        count = node_number
    elif number >= median:
        # print("大于等于=10 不需要创建")
        return
    elif number < node_number:
        count = node_number - number
    start_time = time.time()

    for i in range(count):
        user_data = generate_user_data()

        name = user_data.get("name")
        port = user_data.get("port")
        password = user_data.get("password")
        create_user_result = add_user(name, port, password)

        if create_user_result:
            data = {
                "name": name,
                "port": port,
                "password": password,
                "start_time": start_time
            }
            conv_data = json.dumps(data)
            res = r.lpush(ipaddr, conv_data)
            if res:
                r4.incr(ipaddr)


def main():
    redis_data = r.lrange(ipaddr, 0, -1)
    add_temp_user(len(redis_data))


if __name__ == '__main__':

    while True:
        try:
            main()
        except Exception as e:
            print(e)
        # print("等待30秒")
        time.sleep(15)
