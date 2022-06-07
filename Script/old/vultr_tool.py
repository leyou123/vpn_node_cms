from datetime import datetime
from pprint import pprint

import requests

VULTR_API_KEY = "TRRT2DMP5PD6WYYBM6PIQJPNBKPEW4OHEZIA"
headers = {'Authorization': f'Bearer {VULTR_API_KEY}'}


class Vultr_base:
    headers = None

    def __init__(self, VULTR_API_KEY: str):
        self.headers = {'Authorization': f'Bearer {VULTR_API_KEY}'}

    def is_error(self, response):
        try:
            res = eval(response)
            if "error" in res:
                return res["error"]
            return None
        except Exception as e:
            return e


class Account(Vultr_base):
    name = None  # 用户名
    email = None  # 邮箱
    balance = None  # 总花费
    pending_charges = None  # 待支付
    last_payment = {
        'last_payment_date': None,
        'last_payment_amount': None
    }  # 最后支付的时间和金额
    get_value_date = None  # 获取数据的时间

    def __init__(self, VULTR_API_KEY):
        super().__init__(VULTR_API_KEY)
        self.__accont()

    def __set_value(self, account):
        self.name = account["name"]
        self.email = account["email"]
        self.balance = account["balance"]
        self.pending_charges = account["pending_charges"]
        self.last_payment = {
            'last_payment_date': account["last_payment_date"],
            'last_payment_amount': account["last_payment_amount"]
        }
        self.get_value_date = datetime.now()

    def __accont(self):
        """
        获取账户信息
        curl "https://api.vultr.com/v2/account" \
        -X GET \
        -H "Authorization: Bearer ${VULTR_API_KEY}"
        """
        url = "https://api.vultr.com/v2/account"
        r = requests.get(url=url, headers=self.headers)
        err = self.is_error(r.text)
        if err: return None, err
        res = eval(r.text)
        self.__set_value(res["account"])

    def refresh_data(self):
        self.__accont()


class Instance(Vultr_base):
    def __init__(self, VULTR_API_KEY):
        super().__init__(VULTR_API_KEY)

    def __for_page(self, url, type, data_list=[], next=""):
        if next:
            url = f"{url}cursor={next}"

        r = requests.get(url=url, headers=self.headers)
        err = self.is_error(r.text)
        if err:
            return None, err
        res = eval(r.text)
        data_list += res[type]
        next = res["meta"]["links"]["next"]
        if next == "":
            return data_list
        else:
            self.__for_page(url, type, data_list, next)

    def get_instances(self, main_ip=None):
        """
            获取所有实例
            curl "https://api.vultr.com/v2/instances" \
            -X GET \
            -H "Authorization: Bearer ${VULTR_API_KEY}"
        """
        url = "https://api.vultr.com/v2/instances?"
        instances = self.__for_page(url, "instances")
        return instances

    def get_instances_info(self, instance_id):
        """
        curl "https://api.vultr.com/v2/instances/{instance-id}" \
        -X GET \
        -H "Authorization: Bearer ${VULTR_API_KEY}"

        Args:
            instance_id (str): 实例id
        """
        url = f"https://api.vultr.com/v2/instances/{instance_id}"
        r = requests.get(url=url, headers=self.headers)
        err = self.is_error(r.text)
        if err:
            return None, err
        res = eval(r.text)
        instance = res["instance"]
        return instance

    def get_regions(self):
        """
        curl "https://api.vultr.com/v2/regions" \
        -X GET \
        -H "Authorization: Bearer ${VULTR_API_KEY}"
        """
        url = "https://api.vultr.com/v2/regions?"
        reginos = self.__for_page(url, "regions")
        return reginos

    def get_plans(self, type="vc2"):
        """
        curl "https://api.vultr.com/v2/plans" \
        -X GET \
        -H "Authorization: Bearer ${VULTR_API_KEY}"

        type:
            all:    All available plan types
            vc2:    Cloud Compute
            vhf:	High Frequency Compute
            vdc:	Dedicated Cloud
        """
        type_list = ["all", "vc2", "vhf", "vdc"]
        if type not in type_list:
            type = "vc2"
        url = f"https://api.vultr.com/v2/plans?type={type}&"
        plans = self.__for_page(url, "plans")
        return plans

    def add_instance(self, region, label, snapshot_id, plan="vc2-1c-1gb"):
        """
        curl "https://api.vultr.com/v2/instances" \
        -X POST \
        -H "Authorization: Bearer ${VULTR_API_KEY}" \
        -H "Content-Type: application/json" \
        --data '{
            "region" : "ewr",
            "plan" : "vc2-6c-16gb",
            "label" : "Example Instance",
            "os_id" : 215,
            "user_data" : "QmFzZTY0IEV4YW1wbGUgRGF0YQ==",
            "backups" : "enabled"
        }'

        Args:
            region (str): 地区
            label (str): 标签
            snapshot_id (str): 快照id
            plan (str): 计划. Defaults to "vc2-1c-1gb".
        """
        url = "https://api.vultr.com/v2/instances"
        data = {
            "region": region,
            "plan": plan,
            "label": label,
            "snapshot_id": snapshot_id
        }
        r = requests.post(url=url, headers=self.headers, json=data)
        err = self.is_error(r.text)
        if err:
            return None, err
        res = eval(r.text)
        id = res["instance"]["id"]
        instance = self.get_instances_info(id)
        return instance

    def del_instances(self, instance_id):
        """
        curl "https://api.vultr.com/v2/instances/{instance-id}" \
        -X GET \
        -H "Authorization: Bearer ${VULTR_API_KEY}"

        Args:
            instance_id (str): 实例id
        """
        url = f"https://api.vultr.com/v2/instances/{instance_id}"
        requests.delete(url=url, headers=self.headers)

    def get_instance_bandwidth(self, instance_id):
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

        month = datetime.today().month
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


if __name__ == "__main__":
    # get_instance_list()
    # instance_id = "4d0fef71-3f07-439a-9ec6-4db8a11eb136"  # ip:144.202.55.212 name:ios_Chicago 01
    # get_instance_bandwidth(instance_id)
    # account = Account(VULTR_API_KEY)
    # print(account.last_payment)
    instance = Instance(VULTR_API_KEY)

    # 获取实例
    # instances = instance.get_instances()
    # pprint(instances)

    # 获取地区
    # regions = instance.get_regions()
    # pprint(regions)

    # 获取计划
    # plans = instance.get_plans()
    # pprint(plans)

    # 创建实例
    # city = "Frankfurt"
    # region = [i for i in regions if i["city"] == city][0]

    # print(region)

    # size = 2 + 1

    # lable = f"{region['continent']} {region['city']} {size}"

    # snapshot_id = "36621152-d48f-41aa-80ff-c26e51b62639"
    # instance = instance.add_instance(region["id"], lable, snapshot_id)
    # pprint(instance)

    # 删除实例
    # id = '620a2b6b-25e1-4cd5-8c04-ecebf47e82aa'
    # instance.del_instances(id)

    # 获取流量
    id = "75229bc9-c314-4d8d-a9dd-874c00225e91"
    bandwidth = instance.get_instance_bandwidth(id)
    print(bandwidth)
