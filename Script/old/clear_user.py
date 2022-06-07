import re
import subprocess
import time
import redis
from json import load
from urllib.request import urlopen

import json
import hashlib

path = "/root"
redis_host = "18.144.125.117"

pool = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=0)
pool1 = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=1)
pool2 = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=2)
pool3 = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=3)
pool4 = redis.ConnectionPool(host=redis_host, port=6379, password="redis_!@node2021", db=4)

r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r2 = redis.Redis(connection_pool=pool2)
r3 = redis.Redis(connection_pool=pool3)
r4 = redis.Redis(connection_pool=pool4)

ipaddr = load(urlopen("http://httpbin.org/ip"))["origin"]


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


def convert_flow(flow, unit):
    '''
    转换流量，
    flow float 流量
    unit string 流量单位
    return 返回流量单位 GB
    '''

    setflow = 0
    if unit == "B":
        setflow = round(float(flow) / 1024 / 1024 / 1024, 4)
    elif unit == "KB":
        setflow = round(float(flow) / 1024 / 1024, 4)
    elif unit == "MB":
        setflow = round(float(flow) / 1024, 4)
    elif unit == "GB":
        setflow = flow
    elif unit == "TB":
        setflow = float(flow) * 1024
    return setflow


def get_exp_time(user_name, port):
    md5_value = f"{user_name}{port}{ipaddr}"
    md5_str = getStrAsMD5(md5_value)
    redis_data = r3.get(md5_str)
    if redis_data:
        json_data = json.loads(str(redis_data, "utf-8"))
        return int(json_data.get("time", 0))
    else:
        return None


def query_user_link():
    """
        查询user 名字  端口 流量 和流量单位
    """
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    run_option = ["6", "1"]  # 查询用户信息

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
    s.stdout.close()

    ports = []
    redis_datas = r.lrange(ipaddr, 0, -1)

    for data in redis_datas:
        user_data = json.loads(str(data, "utf-8"))
        port = user_data.get("port", )
        ports.append(port)
    datas = out.split("\n")

    del_ports = []
    current_time = int(time.time())

    for data in datas:
        if "用户名" in data or "用户总数" in data:
            split_data = data.split()
            length_data = len(split_data)

            if length_data > 4:
                ip_link_number = int(split_data[5])
                user_name = split_data[1]
                user_port = split_data[3]

                exp_time = get_exp_time(user_name, user_port)

                if not exp_time:
                    continue

                if current_time - exp_time < 60 * 60 * 12:
                    print(f"还没到过期时间{current_time - exp_time},端口{user_port}")
                    continue

                if ip_link_number:
                    continue

                if user_port in ports:
                    continue
                # 检测
                del_ports.append(user_port)

    return del_ports


def redis_clear(name, port):
    md5_value = f"{name}{port}{ipaddr}"
    md5_conv_value = getStrAsMD5(md5_value)
    r3.delete(md5_conv_value)
    r4.decrby(ipaddr)


def check_flow(ports):
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    run_option = ["5", ]  # 查询用户信息

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
    s.stdout.close()

    vb = 0
    datas = out.split("\n")
    for data in datas:
        if not data.find("===") == -1:
            vb += 1
            if vb > 1:
                break
            continue

        if vb:
            if not data == "":
                i = data.split()
                if not len(i) == 0:
                    name = i[1]
                    port = i[3]
                    flow = i[5]
                    unit = i[6]

                    if port not in ports:
                        continue

                    conv_flow = convert_flow(flow, unit)
                    redis_user_data = r1.get(name)

                    if not conv_flow:
                        if redis_user_data:
                            r1.delete(name)
                        delete_user(port)
                        redis_clear(name, port)
                        print(f"没有流量:删除 {port},使用{conv_flow}GB")
                        continue

                    if not redis_user_data:
                        delete_user(port)
                        redis_clear(name, port)
                        print(f"没有redis:删除{port},使用{conv_flow}GB")
                        continue

                    conv_redis_data = json.loads(str(redis_user_data, "utf-8"))
                    uuid = conv_redis_data.get("uuid", "")
                    res = r2.incrbyfloat(uuid, conv_flow)
                    print(f"插入{uuid},流量{conv_flow}GB")
                    r1.delete(name)
                    delete_user(port)
                    redis_clear(name, port)


def delete_user(port):
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    run_option = [
        "7",  # 选择用户配置
        "2",  # 选择删除用户
        port,  # 输入用户端口
    ]

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub(
        "",
        s.stdout.read().decode("UTF-8", "ignore"))
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")}删除了端口：{port}')


def main():
    redis_data = r4.get(ipaddr)

    if not redis_data:
        return

    user_count = int(str(redis_data, "utf-8"))
    if user_count >= 80:
        ports = query_user_link()
        check_flow(ports)
    else:
        print("用户小于80个,不清理")


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
        print("等待60分钟")
        time.sleep(60 * 60)
