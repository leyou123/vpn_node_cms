import requests
import json
import time

HOST = "http://3.101.129.40:9000"


class UploadFlow(object):

    def test(self):
        pass


def query_user(ip, password):
    print(password)
    query_url = f"{HOST}/user/query_single_user"
    error_status = 2
    data = {
        "password": password,
        "ip": ip
    }
    print(data)
    user_response = requests.post(url=query_url, data=data)
    if user_response.status_code != 200:
        return error_status
    try:
        datas = json.loads(user_response.text)
    except Exception as e:
        return error_status
    query_data = datas.get("data", "")
    if not query_data:
        return error_status
    json_data = json.loads(query_data)
    upload_speed = json_data["status"]["speed_current"].get("upload_speed", "")
    print(upload_speed)
    if upload_speed:
        return True
    else:
        return False

if __name__ == '__main__':
    user_password = "66ADAA86-0921-4E7A-B121-D32150154CAA"
    ip = "216.155.157.223"
    res = query_user(ip, user_password)
    print(res)