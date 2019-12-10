from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
urlpatterns = [
    url(r'^meiduo_admin/authorizations/$', obtain_jwt_token),
]