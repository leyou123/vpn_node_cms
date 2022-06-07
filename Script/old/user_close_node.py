import requests
import json
import redis
import time
pool = redis.ConnectionPool(host="54.219.178.245",port=6379,password="leyou2020",db=4)
r = redis.Redis(connection_pool=pool)


def convert_flow(flow, unit):
    '''
    转换流量，
    flow float 流量
    unit string 流量单位
    return 返回流量单位 GB
    '''

    setflow = 0
    if unit == "B":
        setflow = round(((float(flow) / 1024) / 1024) / 1024, 4)
    elif unit == "KB":
        setflow = round((float(flow) / 1024) / 1024, 4)
    elif unit == "MB":
        setflow = round(float(flow) / 1024, 4)
    elif unit == "GB":
        setflow = flow
    elif unit == "TB":
        setflow = round(float(flow) * 1024, 4)
    return setflow


def close_node(host, port):

    url = "https://node.9527.click/deluser"
    user_name = "getnodes"
    password = "TxPo4gNO3FpEiWYT9bgp"

    response = requests.post(url=url,
                             data={"username": user_name, "host": host, "port": port,
                                   "password": password})

    if response.status_code != 200:
        return None
    datas = json.loads(response.text)
    flow = datas.get("flow", "")
    unit = datas.get("unit", "")
    if not flow:
        return None
    return convert_flow(flow, unit)


def upload_flow(uuid, flow):
    url = "https://9527.click/api/v1/node/user_node_flow"
    json = {
        "uuid": uuid,
        "flow": flow
    }
    response = requests.post(url=url, json=json)
    print(response.status_code)
    print(response.text)

def main():
    while True:
        try:
            redis_data = r.lpop('close_node')
            if not redis_data:
                time.sleep(30)
                print("等待30秒")
                continue
            datas = json.loads(str(redis_data, "utf-8"))
            uuid = datas.get("uuid", "")
            host = datas.get("host", "")
            port = datas.get("port", "")
            flow = close_node(host, port)

            print(f"关闭 host:{host} 端口:{port}")
            # if flow:
            #     upload_flow(uuid, flow)
            #     print(flow)
            # else:
            #     print(f"没流量")
            #     print(f"uuid={uuid},host={host},prot={port},没流量")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
