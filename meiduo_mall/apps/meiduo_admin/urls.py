
from django.conf.urls import url
from meiduo_admin.views.login_view import LoginView

# obtain_jwt_token: 视图(响应登陆请求，完成传统身份认证并签发token)
# 该接口视图，只响应token值。不符合我们自己的业务需求，所以我们要修改该视图的返回数据
from rest_framework_jwt.views import obtain_jwt_token
from meiduo_admin.views.home_views import *

urlpatterns = [
    # url(r'^authorizations/$', LoginView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),


    # 用户总数统计
    url(r'^statistical/total_count/$', UserTotalView.as_view()),
    # 日新增用户统计
    url(r'^statistical/day_increment/$', UserDayIncrView.as_view()),
    # 日活跃用户统计
    url(r'^statistical/day_active/$', UserActiveView.as_view()),
    # 当日下单用户统计
    url(r'^statistical/day_orders/$', UserOrderCount.as_view()),
    # 最近30日增用户统计
    url(r'^statistical/month_increment/$', UserMonthIncrView.as_view()),
]
