import re
import subprocess
import time
import redis
from json import load
from urllib.request import urlopen
import random
import string
import json
import requests
path = "/root"

pool = redis.ConnectionPool(host="18.144.125.117", port=6379, password="redis_!@node2021", db=0)
pool1 = redis.ConnectionPool(host="18.144.125.117", port=6379, password="redis_!@node2021", db=1)
pool2 = redis.ConnectionPool(host="18.144.125.117", port=6379, password="redis_!@node2021", db=2)

r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r2 = redis.Redis(connection_pool=pool2)

ipaddr = load(urlopen("http://httpbin.org/ip"))["origin"]


def add_user(name, port, password):
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
        print(out)
        s.stdout.close()
    except Exception as e:
        print(e)
        return False
    return True

def delete_user(port):

    s = subprocess.Popen(f"sudo {path}/ssrmu.sh",
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         shell=True)

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
    # print(out)
    s.stdout.close()
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")}删除了端口：{port}')


def set_user_speed(port, speed):
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    run_option = [
        "7",  # 选择用户配置
        "9",  # 选择速度限制
        str(port),  # 输入用户端口
        str(speed),  # 输入用户速度
    ]

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
    # print(out)
    s.stdout.close()
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")}限制了端口：{port} 速度为{speed}kb/s')
    return True


def query_user():
    """
        查询user 名字  端口 流量 和流量单位
    """
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    run_option = ["5", ]  # 查询用户信息

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub("",
                                        s.stdout.read().decode("UTF-8", "ignore"))
    s.stdout.close()

    vb = 0
    count = []
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
                    user = {
                        "name": i[1],
                        "port": i[3],
                        "flow": i[5],
                        "unit": i[6]
                    }
                    count.append(user)
    return count


def query_user_link():
    """
        查询user 名字  端口 流量 和流量单位
    """
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    run_option = ["6","1"]  # 查询用户信息

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub("",s.stdout.read().decode("UTF-8", "ignore"))
    s.stdout.close()

    ports = []
    redis_datas = r.lrange(ipaddr, 0, -1)

    for data in redis_datas:
        user_data = json.loads(str(data,"utf-8"))
        port = user_data.get("port",)
        ports.append(port)
    datas = out.split("\n")
    clear_ports = []

    for data in datas:
        if "用户名" in data or "用户总数" in data:
            split_data = data.split()
            length_data = len(split_data)

            if length_data > 4:
                ip_link_number = int(split_data[5])
                user_port = split_data[3]
                if ip_link_number:
                    continue

                if user_port in ports:
                    continue
                # 检测
                clear_ports.append(user_port)

            else:
                user_lick = int(split_data[3])

                if user_lick:
                    data = {
                        "host":ipaddr,
                        "connected":user_lick
                    }
                    url = "https://node.9527.click/upload_node_connected"

                    response = requests.post(url=url,data=data)
                    print(response.status_code)
                    print(response.text)

    return clear_ports


def convFlow(flow, unit):
    '''
    转换流量，
    flow float 流量
    unit string 流量单位
    '''
    setflow = 0
    if unit == "B":
        setflow = float(flow) * 1024
    elif unit == "KB":
        setflow = float(flow)
    elif unit == "MB":
        setflow = float(flow) / 1024
    elif unit == "GB":
        setflow = float(flow) / 1024 / 1024
    elif unit == "TB":
        setflow = float(flow) / 1024 / 1024 / 1024
    return setflow


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
                    print(port)
                    conv_flow = convFlow(flow,unit)
                    print(conv_flow)
                    redis_user_data = r1.get(name)
                    if not redis_user_data:
                        continue
                    conv_redis_data = json.loads(str(redis_user_data,"utf-8"))
                    print(conv_redis_data)
                    uuid = conv_redis_data.get("uuid","")
                    res = r2.incrbyfloat(uuid,conv_flow)
                    print(f"插入{uuid},流量{conv_flow}GB")
                    r1.delete(name)
                    delete_user(port)


def check_user_info():
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    run_option = ["5", ]  # 查询用户信息

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
    s.stdout.close()

    vb = 0
    names = []
    ports = []

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
                    names.append(name)
                    ports.append(port)

    user_data = {
        "name": names,
        "port": ports
    }
    return user_data


def add_temp_user(number, datas):
    """
        添加临时用户
    """

    node_number = 20
    count = 0
    if not number:
        count = node_number
    elif number >= node_number:
        print("大于等于=10 不需要创建")
        return
    elif number < node_number:
        count = node_number - number
    start_time = time.time()
    ports = datas.get("port", "")
    names = datas.get("name", "")

    for i in range(count):
        password = "".join(random.sample(string.ascii_letters + string.digits, 20))
        while True:
            port = str(random.randint(1024, 65535))
            if port not in ports:
                break
        while True:
            name = "TEMP" + "".join(random.sample(string.ascii_letters + string.digits, 20))
            if name not in names:
                break
        create_user_result = add_user(name, port, password)

        if create_user_result:
            data = {
                "name": name,
                "port": port,
                "password": password,
                "start_time": start_time
            }
            conv_data = json.dumps(data)
            r.lpush(ipaddr, conv_data)
            ports.append(port)
            names.append(name)


def main():
    redis_data = r.lrange(ipaddr, 0, -1)
    user_data = check_user_info()
    add_temp_user(len(redis_data), user_data)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
        print("等待10秒")
        time.sleep(30)


