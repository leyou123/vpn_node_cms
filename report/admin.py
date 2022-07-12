from django.contrib import admin
from report.views import CountryView, NodeView, UserView, NodeHeadView, CountryNodesView, NodeOnlineView
from report.models import NodeBlack
# Register your models here.


# class Country(type):
#     class Meta:
#         verbose_name = '国家成功率'
#         model_name = 'Country'
#         app_label = 'report'
#         abstract = False
#         swapped = False
#         app_config = False
#         verbose_name_plural = verbose_name
#         object_name = 'Country'
#
#     _meta = Meta
#
#
# class Node(type):
#     class Meta:
#         verbose_name = '节点成功率'
#         model_name = 'Node'
#         app_label = 'report'
#         abstract = False
#         swapped = False
#         app_config = False
#         verbose_name_plural = verbose_name
#         object_name = 'Node'
#
#     _meta = Meta
#
#
# class User(type):
#     class Meta:
#         verbose_name = '用户成功率'
#         model_name = 'User'
#         app_label = 'report'
#         abstract = False
#         swapped = False
#         app_config = False
#         verbose_name_plural = verbose_name
#         object_name = 'User'
#
#     _meta = Meta
#
#
# class NodeHead(type):
#     class Meta:
#         verbose_name = '节点热度'
#         model_name = 'NodeHead'
#         app_label = 'report'
#         abstract = False
#         swapped = False
#         app_config = False
#         verbose_name_plural = verbose_name
#         object_name = 'NodeHead'
#
#     _meta = Meta
#
#
# class CountryNodes(type):
#     class Meta:
#         verbose_name = '国家节点在线数'
#         model_name = 'CountryNodes'
#         app_label = 'report'
#         abstract = False
#         swapped = False
#         app_config = False
#         verbose_name_plural = verbose_name
#         object_name = 'CountryNodes'
#
#     _meta = Meta
#
#
# class NodeOnline(type):
#     class Meta:
#         verbose_name = '节点上线率'
#         model_name = 'NodeOnline'
#         app_label = 'report'
#         abstract = False
#         swapped = False
#         app_config = False
#         verbose_name_plural = verbose_name
#         object_name = 'NodeOnline'
#
#     _meta = Meta
#
#
#
# @admin.register(Country)
# class CountryAdmin(admin.ModelAdmin):
#
#     def changelist_view(self, request, extra_content=None):
#         return CountryView(request)
#
#
# @admin.register(Node)
# class NodeAdmin(admin.ModelAdmin):
#
#     def changelist_view(self, request, extra_content=None):
#         return NodeView(request)
#
#
# @admin.register(User)
# class NodeAdmin(admin.ModelAdmin):
#
#     def changelist_view(self, request, extra_content=None):
#         return UserView(request)
#
#
# @admin.register(NodeHead)
# class NodeHeadAdmin(admin.ModelAdmin):
#
#     def changelist_view(self, request, extra_content=None):
#         return NodeHeadView(request)
#
#
# @admin.register(CountryNodes)
# class CountryNodesAdmin(admin.ModelAdmin):
#
#     def changelist_view(self, request, extra_content=None):
#         return CountryNodesView(request)
#
#
# @admin.register(NodeOnline)
# class NodeOnlineAdmin(admin.ModelAdmin):
#
#     def changelist_view(self, request, extra_content=None):
#         return NodeOnlineView(request)
#
# class NodeBlackAdmin(admin.ModelAdmin):
#     list_display = ['node_ip', 'node_name', 'country', 'ping_rate_val', 'connect_rate_val']
#     list_filter = ['country', 'node_ip']
#     search_fields = ['node_ip']
#
#
#     def ping_rate_val(self, obj):
#         val = str(obj.ping_rate)
#         try:
#             vlist = val.split(".")
#             val = vlist[0] + "." + vlist[1][:2] + "%"
#         except Exception as e:
#             return obj.ping_rate
#         return val
#
#     def connect_rate_val(self, obj):
#         val = str(obj.connect_rate)
#         try:
#             vlist = val.split(".")
#             val = vlist[0] + "." + vlist[1][:2] + "%"
#         except Exception as e:
#             return obj.connect_rate
#         return val
#
#     ping_rate_val.admin_order_field = "ping_rate"
#     connect_rate_val.admin_order_field = "connect_rate"
#
#
# admin.site.register(NodeBlack, NodeBlackAdmin)