from django.contrib import admin

from node.models import TrajonNode, Country, Operator, NodeConfig,Region,InstanceConfig


class TrajonNodeAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'ip', 'host', "port", "node_type", "country", 'connected', 'quick_access', 'cnt', 'description', 'tag',
    "status", "script_status", "update_time")


class CountryAdmin(admin.ModelAdmin):
    list_display = ("acronym", "name","national_flag","english_name")
    search_fields = ['name']


class OperatorAdmin(admin.ModelAdmin):
    list_display = ["name","snapshot"]


class NodeConfigAdmin(admin.ModelAdmin):
    list_display = ["country", "operator", "node_type", "domain", "name", "ip","region", "config", "status", "run_status", "update_time"]


class RegionAdmin(admin.ModelAdmin):
    list_display = ["name","operator","region","english_name"]


class InstanceConfigAdmin(admin.ModelAdmin):
    list_display = ["name","operator","config"]

admin.site.register(TrajonNode, TrajonNodeAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(NodeConfig, NodeConfigAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(InstanceConfig, InstanceConfigAdmin)
