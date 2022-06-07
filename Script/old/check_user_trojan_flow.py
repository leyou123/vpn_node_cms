import requests
import json
import time

DOMAIN = "https://test.9527.click"
NODE_DOMAIN = "https://nodes.9527.click"

def get_user():
    user_url = f"{DOMAIN}/api/v1/user/query"
    print(user_url)
    user_response = requests.post(user_url)

    if user_response.status_code != 200:
        pass

    datas = json.loads(user_response.text)
    users = datas.get("data")

    uuid = []
    for user in users:
        uuid.append(user.get("uuid", ""))
    return uuid


def upload_flow(uuid, flow):
    user_url = f"{DOMAIN}/api/v1/user/upload_flow"

    data = {
        "uuid": uuid,
        "flow": flow
    }
    print(data)
    user_response = requests.post(url=user_url, json=data)
    # print(user_response.status_code)
    # print(user_response.text)


def calculated_flow(data):
    users = data.get("data")
    flows = []
    for user in users:
        try:
            traffic_total = user["traffic_total"].get("upload_traffic", 0)
            download_traffic = user["traffic_total"].get("download_traffic", 0)

        except Exception as e:
            traffic_total = 0
            download_traffic = 0

        total_flow = traffic_total + download_traffic
        if total_flow:
            flows.append(total_flow)

    if not flows:
        return None
    return sum(flows)


def get_flow():
    users = get_user()
    for user in users:
        url = f"{NODE_DOMAIN}/user/query"
        data = {
            "password": user
        }
        try:
            response = requests.post(url=url, data=data,timeout=20)
        except Exception as e:
            print(e)
            continue

        if response.status_code != 200:
            continue

        datas = json.loads(response.text)
        flows = calculated_flow(datas)
        if not flows:
            print(f"没有流量要上传ID:{user},flow:{flows}")
            continue
        flow = str(round(flows / 1024 / 1024 / 1024, 4))
        upload_flow(user, flow)


if __name__ == '__main__':

    while True:
        try:
            get_flow()
        except Exception as e:
            print(e)
        print("睡眠12小时")
        time.sleep(60*60*12)
