
from django.conf.urls import url
from meiduo_admin.views.login_view import LoginView

# obtain_jwt_token: 视图(响应登陆请求，完成传统身份认证并签发token)
# 该接口视图，只响应token值。不符合我们自己的业务需求，所以我们要修改该视图的返回数据
from rest_framework_jwt.views import obtain_jwt_token
from meiduo_admin.views.home_views import *
from rest_framework.routers import SimpleRouter

urlpatterns = [
    # url(r'^authorizations/$', LoginView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),


    # 用户总数统计
    # url(r'^statistical/total_count/$', HomeViewSet.as_view({"get": "total_count"})),
    # 日新增用户统计
    # url(r'^statistical/day_increment/$', HomeViewSet.as_view({"get": "day_increment"})),
    # 日活跃用户统计
    # url(r'^statistical/day_active/$', HomeViewSet.as_view({"get": "day_active"})),
    # 当日下单用户统计
    # url(r'^statistical/day_orders/$', HomeViewSet.as_view({"get": "day_orders"})),
    # 最近30日增用户统计
    # url(r'^statistical/month_increment/$', HomeViewSet.as_view({"get": "month_increment"})),
    # 日分类商品访问量
    url(r'^statistical/goods_day_views/$', GoodsVisitCountView.as_view()),
]


# 使用drf的路由自动生成路径映射的时候，注意，自动生成的路径一定要复合接口的定义
router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='home')
urlpatterns += router.urls









