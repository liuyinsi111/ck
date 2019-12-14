


from rest_framework.response import Response
from rest_framework.views import APIView
from meiduo_admin.serializers.login_serializer import LoginSerializer


class LoginView(APIView):

    def post(self, request):
        # 1、提取前端传值
        # 2、构建序列化器
        serializer = LoginSerializer(data=request.data)
        # 3、启动校验
        serializer.is_valid(raise_exception=True)
        # 4、获得有效数据，并构建响应参数
        return Response({
            "username": serializer.validated_data['user'].username,
            "user_id": serializer.validated_data['user'].id,
            "token": serializer.validated_data['token'],
        })