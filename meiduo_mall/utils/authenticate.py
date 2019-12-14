from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest
import re
from users.models import User
from django.utils import timezone

class MeiduoModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        自定义认证流程
        :param request: 请求对象
        :param username: 用户名
        :param password: 密码
        :param kwargs: 额外参数
        :return: 返回None表示认证失败，返回User对象表明认证成功(对应的权限：IsAuthentication)
        """

        try:

            user = User.objects.get(username=username)
        except:
            # 如果未查到数据，则返回None，用于后续判断
            try:
                user = User.objects.get(mobile=username)
            except:
                return None


        # 区分当前登陆请求是商城主页登陆还是MIS后台登陆
        if not request:
            # 如果请求对象是None：后台MIS站点登陆
            # 必须验证is_staff == True
            if not user.is_staff:
                return None # 返回一个空对象，表示身份认证失败



        # 判断密码
        if user.check_password(password):
            return user
        else:
            return None

