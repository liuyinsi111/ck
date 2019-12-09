
# 需要定义一个序列化器
# 来校验username和password，并且校验成功后需要生成token(有效数据)

from rest_framework import serializers
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler

# authenticate: 是django原生的传统身份认证全局函数
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    # 类属性指明校验字段
    username = serializers.CharField(write_only=True, required=True, max_length=20)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        # 1、实现传统身份认证
        username = attrs.get("username")
        password = attrs.get("password")

        # 传统身份认证成功之后，返回用户对象
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            # 用户验证不通过，用户已经注销
            raise serializers.ValidationError("传统身份认证失败！")


        # 2、签发token，返回有效数据
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return {
            'user': user,
            'token': token
        }
















