from flask import Flask, request
import re
import subprocess
import json
import time
import socket
import psutil as p
from urllib.request import urlopen
import requests
import datetime
from json import load

path = "/root"

ip_addr = load(urlopen("http://httpbin.org/ip"))["origin"]

VULTR_API_KEY = "TRRT2DMP5PD6WYYBM6PIQJPNBKPEW4OHEZIA"
headers = {'Authorization': f'Bearer {VULTR_API_KEY}'}

app = Flask(__name__)


@app.route("/check_flow", methods=["POST"])
def check_flow():
    # 默认返回内容
    return_dict = {'statusCode': '200', 'message': 'successful!', 'result': False}
    # 判断入参是否为空

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
    return_dict['result'] = count  # 对参数进行操作
    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/delete_user", methods=["POST"])
def delete_user():
    get_data = request.get_data()  # 获取传入的参数
    get_data = json.loads(get_data)  # 传入的参数为bytes类型，需要转化成json
    ports = get_data.get('port', "")

    if not ports:
        return json.dumps({'code': 404, 'message': 'error!'}, ensure_ascii=False)

    for port in ports:
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

    return json.dumps({'code': 200, 'message': 'successful!', 'result': True}, ensure_ascii=False)


@app.route("/delete_user", methods=["POST"])
def set_user_speed():
    get_data = request.get_data()  # 获取传入的参数
    get_data = json.loads(get_data)  # 传入的参数为bytes类型，需要转化成json
    port = get_data.get('port')
    speed = get_data.get('speed')
    s = subprocess.Popen(f"sudo {path}/ssrmu.sh",
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         shell=True)

    run_option = [
        "7",  # 选择用户配置
        "9",  # 选择速度限制
        str(port),  # 输入用户端口
        str(speed),  # 输入用户速度
    ]

    for i in run_option:
        s.stdin.write(bytes(i + "\n", encoding="utf-8"))
    s.stdin.close()

    out = re.compile(r"\x1b[^m]*m").sub(
        "",
        s.stdout.read().decode("UTF-8", "ignore"))
    print(out)
    s.stdout.close()
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")}限制了端口：{port} 速度为{speed}kb/s')
    return json.dumps({'code': 200, 'message': 'successful!', 'result': True}, ensure_ascii=False)


@app.route("/server_status", methods=["POST"])
def servet_status():
    instace_data = get_instance_list(ip_addr)
    instace_id = instace_data.get("instace_id", "")
    total_flow = instace_data.get("total_flow", "")

    already_flow = get_instance_bandwidth(instace_id)

    cpu = cpu_convert(single_core=False, multi_core_avg=True)
    memory = mem_convert()
    net_io = net_io_convert(show_simple=True)
    link_count = user_link()
    flow_send = net_io.get("sent")
    flow_recv = net_io.get("recv")

    ip = get_host_ip()
    data = {
        "ip": ip,
        "cpu": f"{cpu}%",
        "memory": f"{memory}%",
        "flow_send": flow_send,
        "flow_recv": flow_recv,
        "link_count": link_count,
        "instace_id": instace_id,
        "total_flow": total_flow,
        "already_flow": round(already_flow /1024 /1024 /1024,2)

    }
    return json.dumps({'code': 200, 'message': 'successful!', 'data': data}, ensure_ascii=False)


def cpu_convert(single_core=True, multi_core_avg=False) -> float:
    """处理器使用情况

    Args:
        single_core (bool, optional): 是否单核心. Defaults to True.
        multi_core_avg (bool, optional): 是否取平均值（仅多核）. Defaults to False.

    Returns:
        float: 处理器当前占用
    """
    if single_core:
        cpu = p.cpu_percent(interval=1)
    else:
        cpu = p.cpu_percent(interval=1, percpu=True)
        if multi_core_avg:
            cpu = sum(cpu) / len(cpu)
    return round(cpu, 2)


def mem_convert(include_swap=False) -> dict:
    """内存使用情况

    Returns:
        dict:
            vmem: 物理空间内存占用
            smem: 交换空间内存占用
            mem_avg: 平均内存占用
    """
    vmem = p.virtual_memory()
    vmem_total = vmem.total
    vmem_used = vmem.used
    vmem = round(vmem_total / vmem_used, 2)
    res = {"vmem": vmem}
    if include_swap:
        smem = p.swap_memory()
        smem_total = smem.total
        smem_used = smem.used
        smem = round(smem_total / smem_used, 2)
        mem_avg = (vmem + smem) / 2
        res["smem"] = smem
        res["mem_avg"] = mem_avg

    return vmem


def net_io_convert(show_simple: bool = False, decimal: int = 4, interval: int = 1) -> dict:
    """网络带宽使用情况

    Args:
        show_simple (bool, optional): 显示方式，是否为MB 即 值/1024/1024. Defaults to False.
        decimal (int, optional): 保留几位小数. Defaults to 4.
        interval (int, optional): 计算时间间隔. Defaults to 1.

    Returns:
        dict:
            sent: 发送流量带宽
            recv: 接受流量带宽
    """
    net_io1 = p.net_io_counters()
    sent1, recv1 = net_io1.bytes_sent, net_io1.bytes_recv

    if not isinstance(interval, int) or interval <= 0:
        interval = 1

    time.sleep(interval)

    net_io2 = p.net_io_counters()
    sent2, recv2 = net_io2.bytes_sent, net_io2.bytes_recv

    divisor = 1
    if show_simple:
        divisor = 1024 * 1024

    sent = round((sent2 - sent1) / divisor / interval, decimal)
    recv = round((recv2 - recv1) / divisor / interval, decimal)

    return {"sent": sent, "recv": recv}


def get_host_ip():
    """
        获取当前主机ip
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def user_link():
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
    datas = out.split("\n")

    user_list = []
    for data in datas:
        if "链接IP总数" in data:
            user_list.append(data)

    result = str(user_list[0]).split()

    return int(result[-1])


def get_instance_bandwidth(instance_id):
    """获取实例的流量使用情况
        vultr 默认算使用高的
    Args:
        instance_id (str): 实例编号
    """
    url = f"https://api.vultr.com/v2/instances/{instance_id}/bandwidth"

    r = requests.get(url=url, headers=headers)
    res = eval(r.text)

    incoming_count = 0
    outgoing_count = 0

    month = datetime.datetime.today().month
    if month < 10: month = f"0{month}"
    for k, v in res["bandwidth"].items():
        if not f"-{month}-" in k:  # 不是本月的数据，跳过统计
            continue
        # 换算为GB 需要 / 1024 / 1024 / 1024
        incoming_bytes = v["incoming_bytes"]  # 进站流量
        incoming_count += incoming_bytes
        outgoing_bytes = v["outgoing_bytes"]  # 出站流量
        outgoing_count += outgoing_bytes
        # print(
        #     f"日期：{k}\n\t进站：{incoming_bytes} 转换为GB={incoming_bytes/1024/1024/1024}\n\t出站：{outgoing_bytes} 转换为GB={outgoing_bytes/1024/1024/1024}"
        # )
    # print(
    #     f"本月总数据：\n\t总进站为：{incoming_count} 转换为GB={incoming_count/1024/1024/1024}\n\t总出站为：{outgoing_count} 转换为GB={outgoing_count/1024/1024/1024}"
    # )
    return incoming_count if incoming_count > outgoing_count else outgoing_count

def get_instance_list(ip):
    """
        获取所有实例
    """
    url = "https://api.vultr.com/v2/instances"
    r = requests.get(url, headers=headers)
    res = eval(r.text)
    nodes_data = None
    instances_all = res.get("instances", None)

    for instances in instances_all:
        main_ip = instances.get("main_ip", None)
        id = instances.get("id", None)
        total_flow = instances.get("allowed_bandwidth", None)
        temp_data = {
            "instace_id": id,
            "host": main_ip,
            "total_flow": total_flow
        }
        if ip == main_ip:
            nodes_data = temp_data
    return nodes_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
