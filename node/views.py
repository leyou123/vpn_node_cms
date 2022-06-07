import json
import datetime
import time
from django.contrib import auth
from node.models import TrajonNode, NodeConfig
from django.http import JsonResponse, HttpResponseNotFound
from utils.dingding import DataLoggerAPI
from django.views.generic.base import View


def get_now_time():
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def node_status(request):
    """
        节点状态
    """
    data = json.loads(request.body.decode(encoding="utf-8"))
    nodes = data.get("nodes", "")
    if not nodes:
        return JsonResponse({"code": 404, "message": "not found node"})

    for node in nodes:
        host = node.get("host", None)
        cpu = node.get("cpu", None)
        memory = node.get("memory", None)
        network_send = node.get("network_send", None)
        network_recv = node.get("network_recv", None)
        already_flow = node.get("already_flow", None)
        total_flow = node.get("total_flow", None)
        instace_id = node.get("instace_id", None)
        connected = nodes.get("connected", 0)
        # print(host,cpu,memory,network_send,network_recv,connected)

        nodes_all = TrajonNode.objects.filter(ip=host).all()
        for node_one in nodes_all:
            TrajonNode.objects.filter(id=node_one.id).update(
                cpu=cpu,
                memory=memory,
                network_send=f"{network_send}",
                network_recv=f"{network_recv}",
                already_flow=f"{already_flow}",
                total_flow=f"{total_flow}",
                instance_id=instace_id,
                connected=connected,
                update_time=datetime.datetime.now()
            )
    return JsonResponse({"code": 200, "message": "success"})


def trojan_node_network_status(request):
    """
        节点网络测速数据
    """
    data = json.loads(request.body.decode(encoding="utf-8"))
    ip = data.get("ip", None)
    download = round(int(data.get("download", 0)) / 1024 / 1024 / 8, 2)
    upload = round(int(data.get("upload", 0)) / 1024 / 1024 / 8, 2)
    ping = str(data.get("ping", 0))

    TrajonNode.objects.filter(ip=ip).update(
        download=download,
        upload=upload,
        ping=ping,
    )
    return JsonResponse({"code": 200, "message": "success"})


def trojan_node_status(request):
    data = json.loads(request.body.decode(encoding="utf-8"))
    ip = data.get("ip", None)
    cpu = data.get("cpu", None)
    memory = data.get("memory", None)
    network_send = data.get("flow_send", None)
    network_recv = data.get("flow_recv", None)
    already_flow = data.get("already_flow", None)
    total_flow = data.get("total_flow", None)
    instace_id = data.get("instace_id", None)
    connected = data.get("connected", 0)
    nodes = TrajonNode.objects.filter(ip=ip).first()

    if not nodes:
        return JsonResponse({"code": 404, "message": "not found ip"})

    if nodes.status:
        TrajonNode.objects.filter(id=nodes.id).update(
            cpu=cpu,
            memory=memory,
            network_send=f"{network_send}",
            network_recv=f"{network_recv}",
            already_flow=f"{already_flow}",
            total_flow=f"{total_flow}",
            instance_id=instace_id,
            connected=connected,
            update_time=datetime.datetime.now()
        )
        return JsonResponse({"code": 200, "message": "success"})
    else:
        return JsonResponse({"code": 404, "message": "node status close"})


def get_trajon_node(request):
    """
        获取节点列表
    """
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        return HttpResponseNotFound()
    nodes = []

    for i in TrajonNode.objects.filter(status=1).all():
        # use_flow_rate = i.use_flow_rate()
        # if use_flow_rate >= 0.95:
        #     TrajonNode.objects.filter(id=i.id).update(status=0)
        #     message = f"{i.name} IP:{i.ip} 流量即将用尽,使用率{use_flow_rate * 100}%,节点状态:关闭"
        #     api.dd_send_message(message, UserGroup.VPN_OPERATOR)
        #     continue
        nodes.append(i.to_dict())

    return JsonResponse({"nodes": nodes}, status=200, json_dumps_params={"ensure_ascii": False})


def node_switch(request):
    """
        关闭节点
    """
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    domain = request.POST.get("domain", None)
    status = request.POST.get("status", None)
    flow_rate = request.POST.get("flow_rate", None)
    link_rate = request.POST.get("link_rate", None)
    server_status = request.POST.get("server_status", None)

    user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        return HttpResponseNotFound()

    node = TrajonNode.objects.filter(host=domain).first()

    if not node:
        return JsonResponse({"code": 404, "message": "not found ip"})

    res = TrajonNode.objects.filter(host=domain).update(
        status=status
    )

    if not res:
        return JsonResponse({"code": 404, "message": "update failure"})

    status_message = "关闭"
    if status:
        if int(status):
            status_message = "开启"

    flow_message = ""
    if flow_rate:
        flow_message = f"流量使用率{flow_rate}%"

    link_message = ""
    if link_rate:
        link_message = f"连接成功率{link_rate}%"

    server_message = ""
    if server_status:
        server_status_message = "无法连接"
        if int(server_status):
            server_status_message = "正常"

        server_message = f"服务器状态:{server_status_message}"
    dingding_api = DataLoggerAPI("6543720081", "1mtv8ux938ykgw030vi2tuc3yc201ikr")
    now_time = get_now_time()

    message = f"{now_time} \r\n" \
              f"服务器{node.name} \r\n" \
              f"域名:{domain} \r\n" \
              f"{flow_message} \r\n" \
              f"{link_message} \r\n" \
              f"{server_message} \r\n" \
              f"状态:{status_message}"
    res1 = dingding_api.dd_send_message(message, "vpnoperator")
    return JsonResponse({"code": 200, "message": "success"})


def add_node(request):
    """
        添加节点
    """
    data = json.loads(request.body.decode(encoding="utf-8"))

    name = data.get("name", "")
    domain = data.get("domain", "")
    node_type = data.get("node_type", "")
    ip = data.get("ip", "")
    port = data.get("port", "")
    country = data.get("country", "")
    region = data.get("region", "")
    national_flag = data.get("national_flag", "")
    nodes = TrajonNode.objects.filter(ip=ip).first()
    if nodes:
        TrajonNode.objects.filter(id=nodes.id).update(
            name=name,
            host=domain,
            port=port,
            country=country,
            region=region,
            node_type=node_type,
            circle_image_url=national_flag,
            image_url=national_flag,
            update_time=datetime.datetime.now()
        )
        return JsonResponse({"code": 200, "message": "node update success"})
    try:

        speed = 0
        if node_type:
            if int(node_type) == 2:
                speed = 0

        TrajonNode.objects.create(
            name=name,
            host=domain,
            ip=ip,
            port=port,
            country=country,
            region=region,
            node_type=node_type,
            circle_image_url=national_flag,
            image_url=national_flag,
            already_flow=0,
            total_flow=1000,
            speed_limit=speed,
            status=True,
            max_user_connected=500,
            update_time=datetime.datetime.now()
        )
        now_time = get_now_time()
        message = f"时间:{now_time} \r\n" \
                  f"新增节点服务器{name} \r\n" \
                  f"IP: {ip}"
        create_api = DataLoggerAPI("6543720081", "1mtv8ux938ykgw030vi2tuc3yc201ikr")

        create_api.dd_send_message(message, "vpnoperator")

        return JsonResponse({"code": 200, "message": "success"})
    except Exception as e:
        return JsonResponse({"code": 404, "message": "create error"})


def get_all_node(request):
    """
        获取节点列表
    """
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        return HttpResponseNotFound()
    nodes_all = []
    nodes = TrajonNode.objects.all()

    for node in nodes:
        nodes_all.append(node.to_dict())
    return JsonResponse({"nodes": nodes_all}, status=200, json_dumps_params={"ensure_ascii": False})


def del_node(request):
    """
        删除节点
    """
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    domain = request.POST.get("domain", "")

    user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        return HttpResponseNotFound()

    node = TrajonNode.objects.filter(host=domain).first()

    if not node:
        return JsonResponse({"code": 404, "message": "not found domain"})

    if node.status:
        return JsonResponse({"code": 404, "message": "node status open"})

    del_res = TrajonNode.objects.filter(host=domain).delete()

    if del_res:
        return JsonResponse({"code": 200, "message": "success"})
    else:
        return JsonResponse({"code": 404, "message": "not found domain"})


def get_netflix_node(request):
    """
        获取节点列表
    """
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        return HttpResponseNotFound()
    nodes_all = []

    vip_line = 2
    node_name = "U.S. Los Angeles Plus"
    nodes = TrajonNode.objects.filter(node_type=vip_line, name=node_name, status=True).first()

    json_data = {}
    if nodes:
        json_data["nodes"] = nodes.to_dict()

    # for node in nodes:
    #     nodes_all.append(node.to_dict())
    return JsonResponse(json_data, status=200, json_dumps_params={"ensure_ascii": False})


def modify_node(request):
    """
        修改节点属性
    """
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    ip_addr = request.POST.get("ip", "")

    user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        return HttpResponseNotFound()

    node = TrajonNode.objects.filter(ip=ip_addr).first()

    if not node:
        return JsonResponse({"code": 404, "message": "not found ip"})

    modify_res = TrajonNode.objects.filter(ip=ip_addr).update(
        name="Netflix",
        circle_image_url="netflix",
        image_url="netflix",
        quick_access=1,
        tag="U.S. Los Angeles Plus",
        description="netflix"
    )

    if modify_res:
        return JsonResponse({"code": 200, "message": "success"})
    else:
        return JsonResponse({"code": 404, "message": "not found ip"})


class ConnectStatus(View):
    """
        连接状态接口
    """

    def post(self, request):
        json_datas = json.loads(request.body.decode(encoding="utf-8"))
        print(json_datas)
        username = json_datas.get("username", None)
        password = json_datas.get("password", None)
        datas = json_datas.get("datas", None)
        user_obj = auth.authenticate(username=username, password=password)
        if not user_obj:
            return HttpResponseNotFound()

        if not datas:
            return JsonResponse({"code": 404, "message": "not found datas"})

        for data in datas:
            ip_addr = data.get("ip", None)
            state = data.get("state", None)
            check_type = data.get("check_type", None)
            check_result = data.get("check_result", None)
            if not ip_addr or not state or not check_type or not check_result:
                continue
            node = TrajonNode.objects.filter(ip=ip_addr).first()
            if not node:
                continue
            all_json_data = {}

            connect_data = node.connect_data

            if connect_data:
                all_json_data = json.loads(connect_data)
                user_state = all_json_data.get(state, "")

                if user_state:
                    all_json_data[state][check_type] = check_result
                else:
                    all_json_data.update({state: {check_type: check_result}})

            else:
                all_json_data.update({state: {check_type: check_result}})
            modify_res = TrajonNode.objects.filter(ip=ip_addr).update(
                connect_data=json.dumps(all_json_data)
            )

            if modify_res:
                if check_result == "close":
                    now_time = get_now_time()
                    node_type = node.node_type
                    node_type_str = "免费线路"
                    if node_type == 2:
                        node_type_str = "VIP线路"

                    message = f"时间: {now_time} \r\n" \
                              f"节点服务器：{node.ip} \r\n" \
                              f"国家：{node.country} \r\n" \
                              f"上报地区：{state} \r\n" \
                              f"节点类型: {node_type_str} \r\n" \
                              f"检测类型: {check_type} \r\n" \
                              f"检测状态：{check_result} \r\n"
                    create_api = DataLoggerAPI("6543720081", "1mtv8ux938ykgw030vi2tuc3yc201ikr")
                    create_api.dd_send_message(message, "vpnoperator")
        return JsonResponse({"code": 200, "message": "success"})


class GetConfig(View):
    """
        获取配置参数
    """

    def post(self, request):
        data = json.loads(request.body.decode(encoding="utf-8"))
        run_status = data.get("run_status", "")
        nodes = NodeConfig.objects.filter(run_status=run_status).all()
        config_datas = []
        for node in nodes:
            config_datas.append(node.to_json())
        return JsonResponse({"code": 200, "message": "success", "datas": config_datas})


class UploadConfig(View):
    """
        上传配置参数
    """

    def post(self, request):
        data = json.loads(request.body.decode(encoding="utf-8"))
        stop = 0
        running = 1
        start_server = 2
        available = 3
        generate_domain = 4
        complete_ssl = 5
        succeed = 6
        clear_ssl = 7


        config_id = data.get("id", "")
        instance_id = data.get("instance_id", "")
        ip = data.get("ip", "")
        domain_id = data.get("domain_id", "")
        domain = data.get("domain", "")
        cert_id = data.get("cert_id", "")
        cname_validation_p1 = data.get("cname_validation_p1", "")
        cname_validation_p2 = data.get("cname_validation_p2", "")

        status = data.get("status", "")

        run_status = data.get("run_status", "")
        if not config_id:
            return JsonResponse({"code": 404, "message": "data error"})

        node = NodeConfig.objects.filter(id=config_id).first()

        if not node:
            return JsonResponse({"code": 404, "message": "not found ip"})

        if run_status == start_server:
            node_res = NodeConfig.objects.filter(id=config_id).update(
                instance_id=instance_id,
                run_status=run_status,
            )
            if node_res:
                return JsonResponse({"code": 200, "message": "success"})

        if run_status == available:
            node_res = NodeConfig.objects.filter(id=config_id).update(
                ip=ip,
                run_status=run_status,
            )
            if node_res:
                return JsonResponse({"code": 200, "message": "success"})

        if run_status == generate_domain:
            node_res = NodeConfig.objects.filter(id=config_id).update(
                domain_id=domain_id,
                domain=domain,
                run_status=run_status,
            )
            if node_res:
                return JsonResponse({"code": 200, "message": "success"})

        if run_status == complete_ssl:
            if cert_id:
                node_res = NodeConfig.objects.filter(id=config_id).update(
                    ssl_id=cert_id,
                    cname_validation_p1=cname_validation_p1,
                    cname_validation_p2=cname_validation_p2
                )
                if node_res:
                    return JsonResponse({"code": 200, "message": "success"})
            else:
                node_res = NodeConfig.objects.filter(id=config_id).update(
                    run_status=run_status
                )
                if node_res:
                    return JsonResponse({"code": 200, "message": "success"})

        if run_status == succeed:
            node_res = NodeConfig.objects.filter(id=config_id).update(
                status=status,
                run_status=1
            )
            if node_res:
                return JsonResponse({"code": 200, "message": "success"})

        if run_status == clear_ssl:
            node_res = NodeConfig.objects.filter(id=config_id).update(
                cname_validation_p1="",
                cname_validation_p2=""
            )
            if node_res:
                return JsonResponse({"code": 200, "message": "success"})

        return JsonResponse({"code": 404, "message": "submit error"})


class UploadInfo(View):
    def post(self, request):
        """
        上传信息
        :param request:
        :return:
        """
        data = json.loads(request.body.decode(encoding="utf-8"))
        id = data.get("id", "")
        info = data.get("info", "")

        NodeConfig.objects.filter(id=id).update(
            info=info,
        )
        return JsonResponse({"code": 200, "message": "success",})


class ClearServers(View):

    def post(self, request):
        """
        清理服务器
        :param request:
        :return:
        """
        data = json.loads(request.body.decode(encoding="utf-8"))
        instance_id = data.get("instance_id", "")
        TrajonNode.objects.filter(instance_id=instance_id).delete()
        NodeConfig.objects.filter(instance_id=instance_id).update(
            old_instance_id=instance_id,
            instance_id="",
            domain_id="",
            ssl_id="",
            domain="",
            ip="",
            cname_validation_p1="",
            cname_validation_p2="",
            status=0,
            info="",
            run_status=0
        )
        return JsonResponse({"code": 200, "message": "success"})


class DelServers(View):

    def post(self, request):
        """
            删除服务器
        :param request:
        :return:
        """
        data = json.loads(request.body.decode(encoding="utf-8"))
        instance_id = data.get("instance_id", "")
        NodeConfig.objects.filter(instance_id=instance_id).update(
            old_instance_id="",
        )
        return JsonResponse({"code": 200, "message": "success"})



class NodeClose(View):

    def post(self, request):
        """
            删除节点
        :param request:
        :return:
        """
        data = json.loads(request.body.decode(encoding="utf-8"))
        instance_id = data.get("instance_id", "")
        if not instance_id:
            return JsonResponse({"code": 404, "message": "data error"})

        node = TrajonNode.objects.filter(instance_id=instance_id).first()

        if not node:
            return JsonResponse({"code": 404, "message": "data error"})

        TrajonNode.objects.filter(instance_id=instance_id).delete()
        NodeConfig.objects.filter(instance_id=instance_id).update(
            old_instance_id=instance_id,
            instance_id="",
            domain_id="",
            ssl_id="",
            domain="",
            ip="",
            cname_validation_p1="",
            cname_validation_p2="",
            status=0,
            info="",
            run_status=0
        )

        dingding_api = DataLoggerAPI("6543720081", "1mtv8ux938ykgw030vi2tuc3yc201ikr")
        now_time = get_now_time()

        message = f"{now_time} \r\n" \
                  f"服务器{node.name} \r\n" \
                  f"域名:{node.host} \r\n" \
                  f"状态:关闭  \r\n" \
                  f"使用流量超过95%"
        dingding_api.dd_send_message(message, "vpnoperator")
        return JsonResponse({"code": 200, "message": "success"})