import requests
import json
import time

def get_ip():
    user_url = "https://node.9527.click/getnode/"
    data = {
        "username": "getnodes",
        "password": "TxPo4gNO3FpEiWYT9bgp"
    }
    user_response = requests.post(user_url, data=data)

    if user_response.status_code != 200:
        return
    host_all = []
    datas = json.loads(user_response.text)
    nodes = datas.get("nodes",None)
    for node in nodes:
        ip = node.get("host","")
        if ip in host_all:
            continue
        host_all.append(ip)

    return host_all


def get_node_status():
    hosts = get_ip()
    nodes = []
    for host in hosts:
        try:
            # url = "http://199.247.0.123:5000/server_status"
            url = f"http://{host}:5000/server_status"
            json_data = {"host": host}
            response = requests.post(url=url, json=json_data)
            # print(response.status_code)
        except Exception as e:
            print(e)
            continue

        if response.status_code != 200:
            continue

        json_datas = json.loads(response.text)

        datas = json_datas.get("data",None)
        cpu = datas.get("cpu", None)
        memory = datas.get("memory", None)
        network_send = datas.get("flow_send", None)
        network_recv = datas.get("flow_recv", None)
        connected = datas.get("link_count", None)
        instace_id = datas.get("instace_id", None)
        total_flow = datas.get("total_flow", None)
        already_flow = datas.get("already_flow", None)

        data = {
            "host": host,
            "cpu": cpu,
            "memory": memory,
            "network_send": network_send,
            "network_recv": network_recv,
            "connected": connected,
            "instace_id": instace_id,
            "total_flow": total_flow,
            "already_flow": already_flow
        }

        nodes.append(data)
    return nodes



class UpdateTrojanNode(object):

    def get_ip(self):
        user_url = "https://node.9527.click/get_trajon_node"
        data = {
            "username": "getnodes",
            "password": "TxPo4gNO3FpEiWYT9bgp"
        }
        user_response = requests.post(user_url, data=data)

        if user_response.status_code != 200:
            return
        host_all = []
        datas = json.loads(user_response.text)
        nodes = datas.get("nodes", None)
        for node in nodes:
            ip = node.get("ip", "")
            if ip in host_all:
                continue
            host_all.append(ip)
        print(host_all)
        return host_all

    def get_node_status(self):
        hosts = self.get_ip()
        nodes = []
        for host in hosts:
            try:
                # url = "http://199.247.0.123:5000/server_status"
                url = f"http://{host}:5000/server_status"
                json_data = {"host": host}
                response = requests.post(url=url, json=json_data)
                # print(response.status_code)
            except Exception as e:
                print(e)
                continue

            if response.status_code != 200:
                continue

            json_datas = json.loads(response.text)

            datas = json_datas.get("data", None)
            cpu = datas.get("cpu", None)
            memory = datas.get("memory", None)
            network_send = datas.get("flow_send", None)
            network_recv = datas.get("flow_recv", None)
            instace_id = datas.get("instace_id", None)
            total_flow = datas.get("total_flow", None)
            already_flow = datas.get("already_flow", None)

            data = {
                "host": host,
                "cpu": cpu,
                "memory": memory,
                "network_send": network_send,
                "network_recv": network_recv,
                "instace_id": instace_id,
                "total_flow": total_flow,
                "already_flow": already_flow
            }
            nodes.append(data)
        return nodes

    def update_trojan_node(self):
        nodes = self.get_node_status()

        url = "https://node.9527.click/upload_trojan_node_data"
        json_data = {
            "nodes": nodes,
        }
        print(json_data)
        user_response = requests.post(url=url, json=json_data)
        print(user_response.status_code)

    def update_trojan_node_link(self):
        url = "https://node.9527.click/user/query_user_number"

        user_response = requests.post(url=url)
        print(user_response.status_code)




if __name__ == '__main__':



    while True:
        try:
            trojan_node = UpdateTrojanNode()
            trojan_node.update_trojan_node()
            trojan_node.update_trojan_node_link()
        except Exception as e:
            print("错误")
            print(e)
        print("睡眠30分钟")
        time.sleep(60*30)
