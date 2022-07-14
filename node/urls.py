from django.urls import path
from node.views import ConnectStatus, GetConfig, UploadConfig, UploadInfo, ClearServers,DelServers,NodeClose
from node.views import NodeUpdateBlacklist, ClearNodeConfig, UpdateNodeConfig, InstanceDelView

urlpatterns = [
    # path('connect_status', ConnectStatus.as_view(), name="connect_status"),
    path('get_config', GetConfig.as_view(), name="get_config"),
    path('upload_config', UploadConfig.as_view(), name="upload_config"),
    path('upload_info', UploadInfo.as_view(), name="upload_info"),
    path('clear_servers', ClearServers.as_view(), name="clear_servers"),
    path('del_servers', DelServers.as_view(), name="del_servers"),
    path('Node_close', NodeClose.as_view(), name="Node_close"),

    path('node_update_blacklist', NodeUpdateBlacklist.as_view(), name="node_update_blacklist"),
    path('instanceDel', InstanceDelView.as_view(), name="instanceDel"),
    path('clear_nodeconfig', ClearNodeConfig.as_view(), name="clear_nodeconfig"),
    path('update_nodeconfig', UpdateNodeConfig.as_view(), name="update_nodeconfig"),

]
