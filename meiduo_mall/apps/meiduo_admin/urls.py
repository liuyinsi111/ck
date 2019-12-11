
from django.conf.urls import url
from meiduo_admin.views.login_view import LoginView

# obtain_jwt_token: 视图(响应登陆请求，完成传统身份认证并签发token)
# 该接口视图，只响应token值。不符合我们自己的业务需求，所以我们要修改该视图的返回数据
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # url(r'^authorizations/$', LoginView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
]
