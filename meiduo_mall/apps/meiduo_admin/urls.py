
from django.conf.urls import url
from meiduo_admin.views.login_view import LoginView

# obtain_jwt_token: 视图(响应登陆请求，完成传统身份认证并签发token)
# 该接口视图，只响应token值。不符合我们自己的业务需求，所以我们要修改该视图的返回数据
from rest_framework_jwt.views import obtain_jwt_token
from meiduo_admin.views.home_views import *
from meiduo_admin.views.user_views import *
from meiduo_admin.views.sku_views import *
from meiduo_admin.views.spu_views import *
from meiduo_admin.views.specs_views import *
from meiduo_admin.views.options_views import *
from meiduo_admin.views.image_views import *
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

    # 用户多条数据返回
    url(r'^users/$', UserListCreateView.as_view()),

    # SKU表管理
    url(r'^skus/$', SKUViewSet.as_view({'get':'list', 'post':'create'})),
    url(r'^skus/(?P<pk>\d+)/$', SKUViewSet.as_view({'delete':'destroy',
                                                    'get': 'retrieve',
                                                    'put': 'update'})),
    # 新增sku可选三级分类
    url(r'^skus/categories/$', SKUCategoryListView.as_view()),
    # 新增sku可选spu信息
    url(r'^goods/simple/$', SPUSimpleListView.as_view()),
    # 新增sku可选规格选项信息
    url(r'^goods/(?P<pk>\d+)/specs/$', SKUSpecOptListView.as_view()),

    # SPU表管理
    # url(r'^goods/$', SPUViewSet.as_view({'get': 'list', 'post':'create'})),
    # url(r'^goods/(?P<pk>\d+)/$', SPUViewSet.as_view({'get': 'retrieve',
                                                     # 'put': 'update',
                                                     # 'delete': 'destroy'})),
    # 新增spu可选brand
    url(r'^goods/brands/simple/$', SPUViewSet.as_view({'get': 'get_spu_brands'})),
    # 新增spu可选1及分类
    url(r'^goods/channel/categories/$', SPUCategoryListView.as_view()),
    # 新增spu可选2、3及分类
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', SPUCategoryListView.as_view()),


    # 规格表管理
    # url(r'goods/specs/$', SpecViewSet.as_view({'get': 'list', 'post':'create'})),
    # url(r'goods/specs/(?P<pk>\d+)/$', SpecViewSet.as_view({'get': 'retrieve',
                                                           # 'put': 'update',
                                                           # 'delete': 'destroy'})),

    # 选项管理
    url(r'^specs/options/$', OptionsViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^specs/options/(?P<pk>\d+)/$', OptionsViewSet.as_view({'get': 'retrieve',
                                                                 'put': 'update',
                                                                 'delete': 'destroy'})),

    # 新增选项可选规格信息
    url(r'^goods/specs/simple/$', OptionSpecsListView.as_view()),
    url(r'^skus/images/$', ImageViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^skus/simple/$', ImageViewSet.as_view({'get': 'simple'})),
]

# 使用drf的路由自动生成路径映射的时候，注意，自动生成的路径一定要复合接口的定义
router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='home')

# goods/specs/
# goods/specs/ -- self.list()  -- 序列化返回多条规格对象
router.register(prefix='goods/specs', viewset=SpecViewSet, base_name='specs')

# goods/<pk>/  -- self.retrieve() -- 序列化返回单一spu对象
# goods/(?P<pk>[^/.]+)/
router.register(prefix='goods', viewset=SPUViewSet, base_name='spu')

urlpatterns += router.urls









