from django.urls import path

from users.views import CreateUser, DelelteUser, QueryUserAll, ModifyUser, QueryUser,QueryUserNumber,InsertCountry,CreateSingleUser
from users.views import QuerySingleUser,DeleteSingleUser
urlpatterns = [
    path('create', CreateUser.as_view(), name="create"),
    path('delete', DelelteUser.as_view(), name="delete"),
    path('modify', ModifyUser.as_view(), name="modify"),
    path('query', QueryUser.as_view(), name="query"),
    path('query_all', QueryUserAll.as_view(), name="query_all"),
    path('query_user_number', QueryUserNumber.as_view(), name="query_user_number"),
    path('insert_country', InsertCountry.as_view(), name="insert_country"),
    path('create_single_user', CreateSingleUser.as_view(), name="create_single_user"),
    path('query_single_user', QuerySingleUser.as_view(), name="query_single_user"),
    path('delete_single_user', DeleteSingleUser.as_view(), name="delete_single_user"),

]
