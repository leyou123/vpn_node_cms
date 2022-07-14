import paramiko
import json
from node.models import TrajonNode

class Trojan(object):

    def __init__(self):
        self.trojan_path = "/etc/trojan/bin/trojan-go"
        self.trojan_port = 10000
        # self.host = '54.219.250.96'
        self.host = '127.0.0.1'
        self.port = 22
        self.username = 'root'
        self.host_password = 'Leyou2020_!@'

    def iterate_over_all(self, hosts, cmd):
        cmds = []
        for host in hosts:
            cmd_res = f"{self.trojan_path} -api-addr {host}:{self.trojan_port} {cmd}"
            cmds.append(cmd_res)
        return cmds

    def create(self, hosts, password):
        cmd = f"-api set -add-profile -target-password {password}"
        return self.iterate_over_all(hosts, cmd)

    def delete(self, hosts, password):
        cmd = f"-api set -delete-profile -target-password {password}"
        return self.iterate_over_all(hosts, cmd)

    def modify(self, hosts, password, ip_limit, speed_limit):
        cmd = f"-api set -modify-profile -target-password {password}  -ip-limit {ip_limit} -upload-speed-limit {speed_limit} -download-speed-limit {speed_limit}"
        return self.iterate_over_all(hosts, cmd)

    def query(self, hosts, password):
        cmd = f"-api get -target-password {password}"
        return self.iterate_over_all(hosts, cmd)

    def query_all(self, hosts):
        cmd = f"-api list"
        return self.iterate_over_all(hosts, cmd)

    def execute(self, cmds):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, 22, username=self.username, password=self.host_password, timeout=20)
        result = []
        try:
            for cmd in cmds:
                stdin, stdout, stderr = client.exec_command(cmd)
                results = stdout.readlines()
                # print(cmd)
                # print(results)
                if "[" in results[0]:
                    str_data = str(results[0]).replace('[', "").replace(']', "")
                    json_data = json.loads(str_data)
                    data = json_data.get("status", "")
                elif '{' in results[0]:
                    json_data = json.loads(results[0])
                    data = json_data.get("status", "")
                else:
                    data = results

                result.append(data)
        except Exception as e:
            print(e)

        client.close()
        return result

    def execute_user_link(self, cmds):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, 22, username=self.username, password=self.host_password, timeout=30)
        result = []
        try:
            for cmd in cmds:
                # print(cmd)
                stdin, stdout, stderr = client.exec_command(cmd)
                datas = stdout.readlines()

                conv_datas = eval(datas[0])
                count = 0
                for data in conv_datas:
                    speed_current = data['status'].get("speed_current", "")
                    if speed_current:
                        count += 1
                result.append(count)
        except Exception as e:
            print(e)

        client.close()
        return result

    def get_speed(self,host):
        speed_limit = 0
        node = TrajonNode.objects.filter(ip=host).first()
        if node.speed_limit:
            speed_limit = int(1024 * (1024 * node.speed_limit))

        return speed_limit

    def create_single(self, host, password,speed_limit):
        cmd = f"-api set -add-profile -target-password {password}"
        cmd_res = f"{self.trojan_path} -api-addr {host}:{self.trojan_port} {cmd} -upload-speed-limit {speed_limit} -download-speed-limit {speed_limit}"
        return cmd_res


    def modify_single(self, host, password,speed_limit):
        cmd = f"-api set -modify-profile -target-password {password}  -upload-speed-limit {speed_limit} -download-speed-limit {speed_limit}"
        cmd_res = f"{self.trojan_path} -api-addr {host}:{self.trojan_port} {cmd} "
        return cmd_res


    def query_single(self, host, password):
        cmd = f"-api get -target-password {password}"
        cmd_res = f"{self.trojan_path} -api-addr {host}:{self.trojan_port} {cmd}"
        return cmd_res

    def delete_single(self, host, password):
        cmd = f"-api set -delete-profile -target-password {password}"
        cmd_res = f"{self.trojan_path} -api-addr {host}:{self.trojan_port} {cmd}"
        return cmd_res

    def execute_single(self, host, password):
        speed_limit = self.get_speed(host)
        cmd = self.create_single(host, password,speed_limit)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, 22, username=self.username, password=self.host_password, timeout=20)
        # client.connect(host, 22, username=self.username, password=server_password, timeout=20)

        data = ""
        try:
            stdin, stdout, stderr = client.exec_command(cmd)
            results = stdout.readlines()
            data = results[0]

            if speed_limit:
                if "already exist" in data:
                    modify_cmd = self.modify_single(host, password,speed_limit)
                    stdin_m, stdout_m, stderr_m = client.exec_command(modify_cmd)
                    modify_results = stdout_m.readlines()
                    modify_data = modify_results[0]

        except Exception as e:
            print("read cms result error :",e)
        client.close()
        # print(host,password,f"结果:{data}")
        return data

    def execute_query_single(self, host, password):
        cmd = self.query_single(host, password)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, 22, username=self.username, password=self.host_password, timeout=15)
        data = ""
        try:
            stdin, stdout, stderr = client.exec_command(cmd)
            results = stdout.readlines()
            data = results[0]
        except Exception as e:
            print(e)
        client.close()
        return data

    def execute_delete_single(self, host, password):
        cmd = self.delete_single(host, password)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, 22, username=self.username, password=self.host_password, timeout=15)
        data = ""
        try:
            stdin, stdout, stderr = client.exec_command(cmd)
            results = stdout.readlines()
            data = results[0]
        except Exception as e:
            print(e)
        client.close()
        return data

if __name__ == '__main__':
    trojan_host = "45.76.2.45"
    password = "leyou2020"
    trojan = Trojan()
    cmd = trojan.query(trojan_host, password)
    # cmd = trojan.query_all(trojan_host)
    json_data = trojan.execute(cmd)
    # print(json_data, type(json_data))

    # cmds1 = "/etc/trojan/bin/trojan-go -api-addr 45.76.2.45:10000 -api get -target-password leyou2020"

    # execmd2 = "touch /opt/123456/test.txt"

# class User(object):
#     """
#     app创建
#     """
#
#     def __init__(self):
#         self.host = '54.219.250.96'
#         self.prot = 22
#         self.host_name = 'root'
#         self.host_password = 'Leyou2020_!@'
#         self.cmd = 'ls'
#
#
#     def create(self):
#         trans = paramiko.Transport((self.host, self.prot))
#         trans.start_client()
#         trans.auth_password(username=self.host_name, password=self.host_password)
#         self.channel = trans.open_session()  # 打开一个通道
#         self.channel.settimeout(60)
#         self.channel.get_pty()  # 获取一个终端
#         self.channel.invoke_shell()  # 激活器
#         self.channel.send(self.cmd)  # 发送要执行的命令
#         time.sleep(0.5)
#         status = self.channel.recv(1024).decode('utf-8')
#         print(status)
#
# if __name__ == '__main__':
#     user=User()
#
#     user.create()
