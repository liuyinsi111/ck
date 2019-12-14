

from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', # 默认映射的主键字段，read_only=True
            'username',
            'mobile',
            'email',

            'password',
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }


    def validate(self, attrs):
        # 在校验流程中

        # 1、密码加密
        password = attrs.get('password')
        password = make_password(password) # 密闻密码
        attrs['password'] = password # 有效数据中的明文密码改为密闻密码

        # 2、额外添加is_staff=True有效数据
        attrs['is_staff'] = True

        return attrs


   # def create(self, validated_data):
        # 重写create函数。实现自定义对象新建
        # 调整：密码加密，is_staff=True

        # 新建超级管理员
        # create(): 构建莫模型类对象。不会对参数做任务额外操作
        # create_superuser(): 传入原数据，自动密码加密，自动添is_staff=True
        # create_user(): 传入原数据，自动密码加密
        # return self.Meta.model.objects.create_superuser(**validated_data)














