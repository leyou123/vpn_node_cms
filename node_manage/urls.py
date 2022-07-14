"""node_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path,include
from django.views.static import serve

from node.views import get_trajon_node, node_status, trojan_node_status, trojan_node_network_status, add_node,node_switch,get_all_node
from node.views import del_node,modify_node,get_netflix_node,ConnectStatus, get_test_node
from node_manage import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_node', add_node),
    path('node_switch', node_switch),

    path('node_status', trojan_node_status),
    path('get_trajon_node', get_trajon_node),
    path('get_test_node', get_test_node),
    path('get_all_node', get_all_node),
    path('delete_node', del_node),
    path('modify_node', modify_node),
    path('get_netflix_node', get_netflix_node),
    path('connect_status', ConnectStatus.as_view()),
    path('upload_trojan_node_data', node_status),
    path('trojan_node_network_status', trojan_node_network_status),
    path('user/', include('users.urls'), name="user"),
    path('node/', include('node.urls'), name="node"),
    path('report/', include('report.urls'), name="report"),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
