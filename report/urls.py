from django.urls import path

from report.views import CountryView, NodeView, UserView, NodeHeadView
app_name = "report"

urlpatterns = [
    path('country', CountryView, name="country"),
    path('node', NodeView, name="node"),
    path('user', UserView, name="user"),
    path('node_head', NodeHeadView, name="node_head"),

]
