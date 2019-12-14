

from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView
from users.models import User
from meiduo_admin.serializers.user_serializers import UserModelSerializer
from meiduo_admin.custom_paginations import MyPage


class UserListCreateView(ListAPIView, CreateAPIView):
    queryset = User.objects.all()
    #获得所有用户

    serializer_class = UserModelSerializer

    pagination_class =  MyPage


    def get_queryset(self):
        # 根据前端的查询字符串keyword进行过滤，返回需要处理的数据集
        # 过滤逻辑：用户名中包含keyword字串
        # 1、获得keyword
        # 思考：如何在一个非视图函数中，获得当前请求对象request
        #query_params是request的一个类方法，可以用来获得get请求中的字符串
        # self.request: 当前视图对象，所处理的请求对象
        keyword = self.request.query_params.get("keyword")
        # 2、keyword有的话，过滤
        if keyword:
            return self.queryset.filter(username__contains=keyword, is_staff=True)

        # 3、keyword没有，默认返回所有
        return self.queryset.filter(is_staff=True)
