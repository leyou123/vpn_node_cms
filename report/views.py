import requests
import json
import time

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q

from node.models import TrajonNode
from node_manage import settings

from .pagination import PageInfo
# Create your views here.


# base_url = "http://54.177.55.54:10050/v2/"
base_url = "http://54.177.55.54:8000/v2/"

def CountryView(request):



    if request.method == "GET":
        # begin_time = time.time()
        #
        url = base_url + "report/country_rate"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        countrys = json_data.get("data").get("countrys") or []

        # all_count = len(results)
        # page_info = PageInfo(request.GET.get('page'), all_count, '')      # 生成分页对象
        # user_list = results[page_info.start_data():page_info.end_data()]      # 利用分页对象获取当前页显示数据
        # end_time = time.time()
        # print(end_time - begin_time)
        # return render(request, 'report/country.html', {
        #     'results': user_list,
        #     'page_info': page_info,
        #     "countrys":results
        # })
        return render(request, 'report/country.html', {"countrys" : countrys})

    elif request.method == "POST":

        type = request.POST.get("type", "")
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        data = request.POST or {}

        # if not type:
        #     return JsonResponse({"code": 404, "message": "params error!"})
        #
        # if type == "range":
        #
        #     url = base_url + "report/country_rate"
        #     response = requests.post(url, data)
        #     if response.status_code != 200:
        #         return JsonResponse({"code": 404, "message": "Statistics failed!"})
        #
        #     json_data = json.loads(response.text)
        #     results = json_data.get("data").get("results") or []
        #
        #     # all_count = len(results)
        #     # page_info = PageInfo(request.GET.get('page'), all_count, '')  # 生成分页对象
        #     # user_list = results[page_info.start_data():page_info.end_data()]  # 利用分页对象获取当前页显示数据
        #
        #
        #     return JsonResponse({
        #         "code": 200,
        #         "message": "success",
        #         "results": results,
        #         # "page_info": page_info
        #     })

        url = base_url + "report/country_rate"
        response = requests.post(url, data)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        results = json_data.get("data").get("results") or []

        return JsonResponse({
            "code": 200,
            "message": "success",
            "results": results,
            # "page_info": page_info
        })


def NodeView(request):

    if request.method == 'GET':
        url = base_url + "report/node_rate"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        countrys = json_data.get("data").get("countrys") or []

        return render(request, "report/node.html", {"countrys":countrys})

    elif request.method == 'POST':
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        data = request.POST or {}


        url = base_url + "report/node_rate"
        response = requests.post(url, data)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        results = json_data.get("data").get("results") or []

        return JsonResponse({
            "code": 200,
            "message": "success",
            "results": results,
            # "page_info": page_info
        })


def UserView(request):

    if request.method == 'GET':
        url = base_url + "report/user_rate"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        countrys = json_data.get("data").get("countrys") or []

        return render(request, "report/user.html", {"countrys":countrys})

    elif request.method == 'POST':
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        data = request.POST or {}


        url = base_url + "report/user_rate"
        response = requests.post(url, data)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        results = json_data.get("data").get("results") or []

        return JsonResponse({
            "code": 200,
            "message": "success",
            "results": results,
            # "page_info": page_info
        })


def NodeHeadView(request):

    if request.method == 'GET':
        url = base_url + "report/node_head"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        countrys = json_data.get("data").get("countrys") or []

        return render(request, "report/node_head.html", {"countrys":countrys})

    elif request.method == 'POST':

        data = request.POST or {}
        url = base_url + "report/node_head"
        response = requests.post(url, data)
        if response.status_code != 200:
            return JsonResponse({"code": 404, "message": "Statistics failed!"})

        json_data = json.loads(response.text)
        results = json_data.get("data").get("results") or []

        return JsonResponse({
            "code": 200,
            "message": "success",
            "results": results,
            # "page_info": page_info
        })


def CountryNodesView(request):
    """
    统计所有国家线路数量
    @param request:
    @return:
    """

    if request.method == 'GET':
        # 1.获取用户国家列表
        url = base_url + "user/get_all_users"
        response = requests.post(url)
        json_data = json.loads(response.text)
        users = json_data.get("users", "")
        if not users:
            return JsonResponse({"code":404, "message":"not found users"})
        results = []

        for item in users:
            country = item.get("country", "")
            if not country:
                continue
            # 统计免费
            free_total = Count('id', filter=Q(node_type=1) & ~Q(test_black__contains=country))
            # 统计vip
            vip_total = Count('id', filter=Q(node_type=2) & ~Q(test_black__contains=country))



            r1 = TrajonNode.objects.all().aggregate(free_total=free_total, vip_total=vip_total)
            results.append({
                "country":country,
                "free":r1.get("free_total", 0),
                "vip":r1.get("vip_total", 0),
            })

        print(results)
        return render(request, "report/country_nodes.html", {"nodes":results})


def NodeOnlineView(request):
    """
    统计所有节点的上线率
    @param request:
    @return:
    """

    if request.method == 'GET':
        results = []
        # 1.获取用户国家总数和用户国家列表
        url = base_url + "user/get_all_users"
        response = requests.post(url)
        json_data = json.loads(response.text)
        all_country = json_data.get("count", 0)
        # 2.遍历每个节点，获取有几个国家在黑名单
        nodes = TrajonNode.objects.values("ip", "test_black", "name", "node_type").all()
        # 3.用户国家总数 / （用户国家总数-在黑名单数量） = 上线率
        for node in nodes:
            node_type = node.get("node_type", "")
            if node_type == 1:
                node_type = "免费"
            elif node_type == 2:
                node_type = "付费"
            else:
                node_type = ""
            # blacks = node.get("test_black", "").split(",")[:-1]
            blacks = node.get("test_black", "").split(",")
            if blacks[-1] == "":
                blacks = blacks[:-1]
            count = len(blacks)

            results.append({
                "ip": node.get("ip", ""),
                "name": node.get("name", ""),
                "node_type": node_type,
                "online": round((all_country - count) / all_country * 100, 2)
            })

        return render(request, "report/node_online.html", {"nodes":results, "node_nums": len(nodes)})

