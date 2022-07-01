##########################################################################################
# 基于新的dl后台（使用了rest）的api封装
##########################################################################################

import hashlib
import json
from urllib.parse import urlencode
from datetime import datetime, timezone

import requests

URL_DL_ADMIN = "https://agri-dl.holdingbyte.com"


def get_utc_timestamp():
    """
    获取utc时间戳（秒）
    """
    # 获取utc时间
    now = datetime.now(timezone.utc)
    # 获取时间戳
    delta_v = now - datetime(1970, 1, 1, tzinfo=timezone.utc)
    return int(delta_v.total_seconds())


class DataLoggerAPI:
    """
    数据采集平台api
    """

    def __init__(self, client_id, client_key, **kwargs):
        self.client_id = client_id
        self.client_key = client_key

        # 单元测试
        self.unittest_client = kwargs.get("unittest_client", None)

    def _send_request(self, api_url, data: dict = None, method: str = "GET", sign: bool = True):
        """
        发送请求

        @param method       请求类型，GET、POST、DELETE
        @param sign         是否签名
        """

        method = method.upper()

        if not api_url.startswith("/"):
            api_url = "/" + api_url
        if not api_url.endswith("/"):
            api_url + "/"

        url = URL_DL_ADMIN + api_url

        # url_parts = list(urlparse.urlparse(url))
        # query = dict(urlparse.parse_qsl(url_parts[4]))

        # ========================================================
        # 添加签名
        # ========================================================
        if sign:
            url += "&" if "?" in url else "?"

            client_t = get_utc_timestamp()

            md5 = hashlib.md5()
            md5.update("{}{}{}".format(self.client_id, client_t,
                                       self.client_key).encode("utf-8"))
            client_md5 = md5.hexdigest()

            url += "client_id={}&client_t={}&client_md5={}".format(self.client_id, client_t, client_md5)
        # ========================================================

        if method == "GET" and data is not None:
            url += "&" if "?" in url else "?"
            url += urlencode(data, doseq=True)

        # print("\trequest url is:", url)
        # print("\trequest data is:", data)
        # print("\trequest method is:", method)
        # print("\tunittest_client is:", self.unittest_client)

        if self.unittest_client is not None:
            if method == "GET":
                resp = self.unittest_client.get(url)
            elif method == "POST":
                resp = self.unittest_client.post(
                    url, data=json.dumps(data), content_type='application/json')
            elif method == "PUT":
                resp = self.unittest_client.put(url, data=json.dumps(
                    data), content_type='application/json')
            elif method == "DELETE":
                resp = self.unittest_client.delete(
                    url, params=data, content_type='application/json')
        else:
            if method == "GET":
                resp = requests.get(url)
            elif method == "POST":
                resp = requests.post(url, json=data)
            elif method == "PUT":
                resp = requests.put(url, json=data)
            elif method == "DELETE":
                resp = requests.delete(url, params=data)

        resp_data = None

        try:
            resp_data = json.loads(resp.text)
        except Exception as e:
            # print("解析resp.text失败！", e)
            pass

        if resp_data is None:
            try:
                resp_data = json.loads(resp.content)
            except Exception as e:
                # print("解析resp.content失败！", e)
                pass

        # print("\tresponse is:", resp_data)
        return resp_data

    def device_register(self, device_id,
                        connect_ip=None,
                        server_id=None,
                        vendor=None,
                        the_type=None,
                        **kwargs
                        ):
        """
        注册一个设备

        @param  device_id           设备id
        @param  connect_ip          设备当前ip
        @param  server_id           设备连接的服务器id，比如agri-dl-01
        @param  vendor              厂商
        @param  the_type            设备类型
        @param  kwargs
                    info            携带信息
                    iccid           sim卡的iccid

        返回数据：
        {
            "agri_id":string,
            "type":int,
            "vender":int,
            "cmds":[
                {"id":int, ...}
            ],
        }
        """
        data = {

        }

        if device_id is not None:
            data["device_id"] = device_id

        # 设备ip
        if connect_ip is not None:
            data["connect_ip"] = connect_ip

        # 服务器id
        if server_id is not None:
            data["server_id"] = server_id

        if vendor is not None:
            data["vendor"] = vendor

        if the_type is not None:
            data["the_type"] = the_type

        if "iccid" in kwargs:
            data["iccid"] = kwargs["iccid"]

        # 附带信息
        if kwargs.get("info", None) is not None:
            data["info"] = kwargs["info"]

        result = self._send_request("/api/device/", data, "POST")
        return result

    def device_heartbeat(self, device_id):
        """
        设备心跳

        @param  device_id           设备id

        返回数据：
        {
        }
        """
        result = self._send_request(
            "/api/device/{}/heartbeat/".format(device_id), None, "GET")
        return result

    def device_check(self, device_id, safe_code):
        """
        检查一个设备是否属于我们自己的产品

        @param  device_id               设备id
        @param  safe_code               设备安全码

        返回数据：
        {
            "agri_id":string,
            "model":string,
        }
        """
        data = {
            "safe_code": safe_code
        }

        result = self._send_request(
            "/api/device/{}/check/".format(device_id), data, "GET", False)
        return result

    def device_detail(self, device_id):
        """
        注册一个设备

        @param  device_id           设备id

        返回数据：
        {
            "agri_id":string,
            "model":string,
        }
        """

        result = self._send_request("/api/device/{}/".format(device_id))
        return result

    def device_filter(self, vendor, the_type):
        """
        搜索设备

        返回数据：
        {
            "devices":[
                {"id":int, ...}
            ],
        }
        """
        data = {
            "vendor": vendor,
            "type": the_type,
        }

        result = self._send_request("/api/device/filter/", data)
        return result

    def device_set_data(self, device_data: list):
        """
        设置设备数据
        """

        result = self._send_request("/api/device/data/", device_data, "POST")
        return result

    def device_get_data(self, agri_ids: list):
        """
        获取设备数据
        """

        # url = ""
        # for a_agri_id in agri_ids:
        #     if url != "":
        #         url += "&"
        #     url += "agri_id={}".format(a_agri_id)

        # url = "/api/device/data/?" + url
        # device_datas = self._send_request(url)

        data = {
            "agri_id": agri_ids
        }
        device_datas = self._send_request("/api/device/data/", data)

        return device_datas

    def cmd_create(self, agri_id: str, cmd_type: int, cmd_value: float, r_token: str = None, info: str = None):
        """
        针对目标设备创建一条新的命令

        @param      agri_id         目标设备id
        @param      cmd_type        命令类型。CommandType
        @param      cmd_value       命令携带值
        @param      r_token         请求token

        返回数据：
        {
            "id":int,
            "type":int,
            "value":float
        }
        """

        data = {
            "t_agri_id": agri_id,
            "cmd_type": cmd_type,
            "cmd_value": cmd_value,
            "r_token": r_token,
            "info": info,
        }

        result = self._send_request("/api/command/", data, "POST")
        return result

    def cmd_mine(self, agri_id):
        """
        获取指定设备的所有需要执行的命令

        返回数据：
        {
            "cmds":[
                {"id":int, "type":int, "value":float}
            ],
        }
        """

        result = self._send_request(
            "/api/command/filter/{}/".format(agri_id), None)
        return result

    def cmd_executing(self, cmd_id: int):
        """
        开始执行一个命令

        @param      cmd_id          命令id

        返回数据：
        {
            "id":int,
            "type":int,
            "value":float
        }
        """

        """
        cmd_status = (
            (0, "等待执行"),
            (1, "正在执行"),
            (10, "执行成功"),
            (11, "执行失败"),
        )
        """

        data = {
            "status": 1
        }

        result = self._send_request(
            "/api/command/{}/".format(cmd_id), data, "PUT")
        return result

    def cmd_success(self, cmd_id: int, info: str = None):
        """
        执行一个命令成功
        Args:
            cmd_id:
            info:

        Returns:

        """

        data = {
            "status": 10
        }

        result = self._send_request(
            "/api/command/{}/".format(cmd_id), data, "PUT")
        return result

    def cmd_fail(self, cmd_id: int, info: str = None):
        """
        执行一个命令失败
        Args:
            cmd_id:
            info:

        Returns:

        """

        data = {
            "status": 11
        }

        result = self._send_request(
            "/api/command/{}/".format(cmd_id), data, "PUT")
        return result

    ####################################
    # 钉钉相关
    ####################################

    def dd_send_message(self, content: str, group: str):
        """
        发送消息

        :param  content     消息内容
        :param  group       发送目标组。默认为运营人员。
        """

        data = {
            "content": content,
            "to_group_name": group,
        }

        result = self._send_request("/dingding/message/", data, "POST")
        return result


if __name__ == "__main__":
    api = DataLoggerAPI("6543720081", "1mtv8ux938ykgw030vi2tuc3yc201ikr")
    # api = DataLoggerAPI("6543720081", "moykfz78chkfonkgs7p0kuwz13yvsy4w")

    import time

    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(api.dd_send_message(f"测试钉钉通知999{otherStyleTime}", "vpnoperator"))
    print(api.dd_send_message(f"测试钉钉通知999", "vpnoperator"))