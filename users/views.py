from django.views.generic.base import View
from django.http import JsonResponse

from users.core import Trojan
from node.models import TrajonNode, Country


class CreateUser(View):
    def post(self, request):
        """
        创建用户
        :param request:
        :return:
        """
        password = request.POST.get("password", "")
        if not password:
            return JsonResponse({"code": 404, "message": "not found password"})
        nodes = TrajonNode.objects.filter(status=1)

        if not nodes.count():
            return JsonResponse({"code": 404, "message": "not found nodes"})
        ip = []
        for node in nodes:
            ip.append(node.ip)
        trojan = Trojan()
        cmd = trojan.create(ip, password)
        data = trojan.execute(cmd)
        return JsonResponse({"code": 200, "message": "success", "data": data})


class DelelteUser(View):
    def post(self, request):
        """
        删除用户
        :param request:
        :return:
        """
        password = request.POST.get("password", "")
        if not password:
            return JsonResponse({"code": 404, "message": "not found password"})
        nodes = TrajonNode.objects.filter(status=True)

        if not nodes.count():
            return JsonResponse({"code": 404, "message": "not found nodes"})
        ip = []
        for node in nodes:
            ip.append(node.ip)
        trojan = Trojan()
        cmd = trojan.delete(ip, password)
        data = trojan.execute(cmd)
        return JsonResponse({"code": 200, "message": "success", "data": data})


class ModifyUser(View):
    def post(self, request):
        """
        修改用户
        :param request:
        :return:
        """
        password = request.POST.get("password", "")
        ip_limit = request.POST.get("ip_limit", "")
        speed_limit = request.POST.get("speed_limit", "")

        if not password:
            return JsonResponse({"code": 404, "message": "not found password"})

        nodes = TrajonNode.objects.all()

        ip = []
        for node in nodes:
            ip.append(node.ip)
        trojan = Trojan()
        cmd = trojan.modify(ip, password, ip_limit, speed_limit)
        data = trojan.execute(cmd)

        return JsonResponse({"code": 200, "message": "success", "data": data})


class QueryUserAll(View):

    def post(self, request):
        """
        查询所有服务器
        :param request:
        :return:
        """
        nodes = TrajonNode.objects.filter(status=True)
        if not nodes.count():
            return JsonResponse({"code": 404, "message": "not found nodes"})
        ip = []
        for node in nodes:
            ip.append(node.ip)
        trojan = Trojan()
        cmds = trojan.query_all(ip)
        data = trojan.execute(cmds)
        return JsonResponse({"code": 200, "message": "success", "data": data})


class QueryUser(View):
    def post(self, request):
        """
        查看用户
        :param request:
        :return:
        """
        password = request.POST.get("password", "")
        if not password:
            return JsonResponse({"code": 404, "message": "not found password"})
        nodes = TrajonNode.objects.filter(status=True)
        if not nodes.count():
            return JsonResponse({"code": 404, "message": "not found nodes"})
        ip = []
        for node in nodes:
            ip.append(node.ip)
        trojan = Trojan()
        cmds = trojan.query(ip, password)

        data = trojan.execute(cmds)
        return JsonResponse({"code": 200, "message": "success", "data": data})


class QueryUserNumber(View):

    def post(self, request):
        """
        查询所有服务器
        :param request:
        :return:
        """
        nodes = TrajonNode.objects.filter(status=True)
        if not nodes.count():
            return JsonResponse({"code": 404, "message": "not found nodes"})
        ip = []
        for node in nodes:
            ip.append(node.ip)
        trojan = Trojan()
        cmds = trojan.query_all(ip)
        datas = trojan.execute_user_link(cmds)

        for i in range(len(ip)):
            TrajonNode.objects.filter(ip=ip[i]).update(connected=datas[i])

        return JsonResponse({"code": 200, "message": "success"})


class InsertCountry(View):

    def post(self, request):
        """
        查询所有服务器
        :param request:
        :return:
        """
        countrys = [
            ["AO", "安哥拉"],
            ["AF", "阿富汗"],
            ["AL", "阿尔巴尼亚"],
            ["DZ", "阿尔及利亚"],
            ["AD", "安道尔共和国"],
            ["AI", "安圭拉岛"],
            ["AG", "安提瓜和巴布达"],
            ["AR", "阿根廷"],
            ["AM", "亚美尼亚"],
            ["AU", "澳大利亚"],
            ["AT", "奥地利"],
            ["AZ", "阿塞拜疆"],
            ["BS", "巴哈马"],
            ["BH", "巴林"],
            ["BD", "孟加拉国"],
            ["BB", "巴巴多斯"],
            ["BY", "白俄罗斯"],
            ["BE", "比利时"],
            ["BZ", "伯利兹"],
            ["BJ", "贝宁"],
            ["BM", "百慕大群岛"],
            ["BO", "玻利维亚"],
            ["BW", "博茨瓦纳"],
            ["BR", "巴西"],
            ["BN", "文莱"],
            ["BG", "保加利亚"],
            ["BF", "布基纳法索"],
            ["MM", "缅甸"],
            ["BI", "布隆迪"],
            ["CM", "喀麦隆"],
            ["CA", "加拿大"],
            ["CF", "中非共和国"],
            ["TD", "乍得"],
            ["CL", "智利"],
            ["CN", "中国"],
            ["CO", "哥伦比亚"],
            ["CG", "刚果"],
            ["CK", "库克群岛"],
            ["CR", "哥斯达黎加"],
            ["CU", "古巴"],
            ["CY", "塞浦路斯"],
            ["CZ", "捷克"],
            ["DK", "丹麦"],
            ["DJ", "吉布提"],
            ["DO", "多米尼加共和国"],
            ["EC", "厄瓜多尔"],
            ["EG", "埃及"],
            ["SV", "萨尔瓦多"],
            ["EE", "爱沙尼亚"],
            ["ET", "埃塞俄比亚"],
            ["FJ", "斐济"],
            ["FI", "芬兰"],
            ["FR", "法国"],
            ["GF", "法属圭亚那"],
            ["GA", "加蓬"],
            ["GM", "冈比亚"],
            ["GE", "格鲁吉亚"],
            ["DE", "德国"],
            ["GH", "加纳"],
            ["GI", "直布罗陀"],
            ["GR", "希腊"],
            ["GD", "格林纳达"],
            ["GU", "关岛"],
            ["GT", "危地马拉"],
            ["GN", "几内亚"],
            ["GY", "圭亚那"],
            ["HT", "海地"],
            ["HN", "洪都拉斯"],
            ["HK", "香港"],
            ["HU", "匈牙利"],
            ["IS", "冰岛"],
            ["IN", "印度"],
            ["ID", "印度尼西亚"],
            ["IR", "伊朗"],
            ["IQ", "伊拉克"],
            ["IE", "爱尔兰"],
            ["IL", "以色列"],
            ["IT", "意大利"],
            ["JM", "牙买加"],
            ["JP", "日本"],
            ["JO", "约旦"],
            ["KH", "柬埔寨"],
            ["KZ", "哈萨克斯坦"],
            ["KE", "肯尼亚"],
            ["KR", "韩国"],
            ["KW", "科威特"],
            ["KG", "吉尔吉斯坦"],
            ["LA", "老挝"],
            ["LV", "拉脱维亚"],
            ["LB", "黎巴嫩"],
            ["LS", "莱索托"],
            ["LR", "利比里亚"],
            ["LY", "利比亚"],
            ["LI", "列支敦士登"],
            ["LT", "立陶宛"],
            ["LU", "卢森堡"],
            ["MO", "澳门"],
            ["MG", "马达加斯加"],
            ["MW", "马拉维"],
            ["MY", "马来西亚"],
            ["MV", "马尔代夫"],
            ["ML", "马里"],
            ["MT", "马耳他"],
            ["MU", "毛里求斯"],
            ["MX", "墨西哥"],
            ["MD", "摩尔多瓦"],
            ["MC", "摩纳哥"],
            ["MN", "蒙古"],
            ["MS", "蒙特塞拉特岛"],
            ["MA", "摩洛哥"],
            ["MZ", "莫桑比克"],
            ["NA", "纳米比亚"],
            ["NR", "瑙鲁"],
            ["NP", "尼泊尔"],
            ["NL", "荷兰"],
            ["NZ", "新西兰"],
            ["NI", "尼加拉瓜"],
            ["NE", "尼日尔"],
            ["NG", "尼日利亚"],
            ["KP", "朝鲜"],
            ["NO", "挪威"],
            ["OM", "阿曼"],
            ["PK", "巴基斯坦"],
            ["PA", "巴拿马"],
            ["PG", "巴布亚新几内亚"],
            ["PY", "巴拉圭"],
            ["PE", "秘鲁"],
            ["PH", "菲律宾"],
            ["PL", "波兰"],
            ["PF", "法属玻利尼西亚"],
            ["PT", "葡萄牙"],
            ["PR", "波多黎各"],
            ["QA", "卡塔尔"],
            ["RO", "罗马尼亚"],
            ["RU", "俄罗斯"],
            ["LC", "圣卢西亚"],
            ["VC", "圣文森特岛"],
            ["SM", "圣马力诺"],
            ["ST", "圣多美和普林西比"],
            ["SA", "沙特阿拉伯"],
            ["SN", "塞内加尔"],
            ["SC", "塞舌尔"],
            ["SL", "塞拉利昂"],
            ["SG", "新加坡"],
            ["SK", "斯洛伐克"],
            ["SI", "斯洛文尼亚"],
            ["SB", "所罗门群岛"],
            ["SO", "索马里"],
            ["ZA", "南非"],
            ["ES", "西班牙"],
            ["LK", "斯里兰卡"],
            ["SD", "苏丹"],
            ["SR", "苏里南"],
            ["SZ", "斯威士兰"],
            ["SE", "瑞典"],
            ["CH", "瑞士"],
            ["SY", "叙利亚"],
            ["TW", "台湾省"],
            ["TJ", "塔吉克斯坦"],
            ["TZ", "坦桑尼亚"],
            ["TH", "泰国"],
            ["TG", "多哥"],
            ["TO", "汤加"],
            ["TT", "特立尼达和多巴哥"],
            ["TN", "突尼斯"],
            ["TR", "土耳其"],
            ["TM", "土库曼斯坦"],
            ["UG", "乌干达"],
            ["UA", "乌克兰"],
            ["AE", "阿拉伯联合酋长国"],
            ["GB", "英国"],
            ["US", "美国"],
            ["UY", "乌拉圭"],
            ["UZ", "乌兹别克斯坦"],
            ["VE", "委内瑞拉"],
            ["VN", "越南"],
            ["YE", "也门"],
            ["YU", "南斯拉夫"],
            ["ZW", "津巴布韦"],
            ["ZR", "扎伊尔"],
            ["ZM", "赞比亚"]
        ]

        for country in countrys:
            acronym = country[0]
            china = country[1]
            Country.objects.update_or_create(
                acronym=acronym,
                name=china
            )
        return JsonResponse({"code": 200, "message": "success"})


class CreateSingleUser(View):
    def post(self, request):
        """
        创建用户
        :param request:S
        :return:
        """
        password = request.POST.get("password", "")
        ip = request.POST.get("ip", "")

        if not password or not ip:
            return JsonResponse({"code": 404, "message": "data error"})

        query_ip = TrajonNode.objects.filter(ip=ip).first()
        if not query_ip:
            return JsonResponse({"code": 404, "message": "not found ip"})

        trojan = Trojan()
        data = trojan.execute_single(ip, password)
        if "already exist" in data or "Done" in data:
            return JsonResponse({"code": 200, "message": "success", "data": data})
        else:
            return JsonResponse({"code": 404, "message": data})


class QuerySingleUser(View):
    def post(self, request):
        """
        创建用户
        :param request:S
        :return:
        """
        password = request.POST.get("password", "")
        ip = request.POST.get("ip", "")

        if not password or not ip:
            return JsonResponse({"code": 404, "message": "data error"})
        trojan = Trojan()
        data = trojan.execute_query_single(ip, password)
        return JsonResponse({"code": 200, "message": "success", "data": data})


class DeleteSingleUser(View):
    def post(self, request):
        """
        创建用户
        :param request:S
        :return:
        """
        password = request.POST.get("password", "")
        ip = request.POST.get("ip", "")

        if not password or not ip:
            return JsonResponse({"code": 404, "message": "data error"})

        trojan = Trojan()
        data = trojan.execute_delete_single(ip, password)
        return JsonResponse({"code": 200, "message": "success", "data": data})