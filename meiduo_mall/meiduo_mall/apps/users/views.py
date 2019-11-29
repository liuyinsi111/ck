from django.shortcuts import render, redirect
from django.views.generic import View
from django import http
import re
from .models import User

from django_redis import get_redis_connection
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.conf import settings


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        query_dict = request.POST
        username = query_dict.get('username')
        password = query_dict.get('password')
        password2 = query_dict.get('password2')
        mobile = query_dict.get('mobile')
        sms_code = query_dict.get('sms_code')
        allow = query_dict.get('allow')
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')

        #创建redis连接
        #获取当前手机号验证码
        #判断是否国旗
        #判断填写验证码是否符合
        redis_conn = get_redis_connection('verify_codes')
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        redis_conn.delete('sms_%s'% mobile)

        if sms_code_server is None:
            return render(request, 'register.html', {'regist_errmsg': '短信验证码已过期'})

        if sms_code != sms_code_server.decode():
            return render(request, 'register.html', {'register_errmsg':'短信验证码填写错误'})
        #
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        login(request, user)
        # return http.HttpResponse('注册成功即代表登陆成功,重定向到首页')
        response = redirect('/')
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)
        return response



class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'count': count})

class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(username=mobile).count()
        return http.JsonResponse({'count': count})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    # def post(self, request):#1.接收2.校验3.判断用户名和密码是否正确4.状态保持5.重定向
    #     query_dict = request.POST
    #     username = query_dict.get('username')
    #     password = query_dict.get('password')
    #     remembered = query_dict.get('remembered')
    #     if all([username, password]) is False:
    #         return http.HttpResponseForbidden('缺少必传递参数')
    #
    #     # try:
    #     #     user = User.objects.get(username=username)
    #     #     if user.check_password(password) is False:
    #     #         return http.HttpResponseForbidden('用户名或密码错误')
    #     # except User.DoesNotExist:
    #     #     return http.HttpResponseForbidden('用户名或密码错误')
    #     #
    #     user =  authenticate(request, username=username, password=password)
    #     if user is None:
    #         qs = User.objects.filter(Q(username-username) | Q(mobile=username))
    #         if user.check_password(password) is False:
    #             return http.HttpResponseForbidden('用户名或密码错误')
    #         else:
    #             return http.HttpResponseForbidden('用户名或密码错误')
    #     login(request, user)
    #     if remembered is None:
    #         request.session.set_expiry(0)
    #     return http.HttpResponse('跳转到首页')

    def post(self, request):#1.接收2.校验3.判断用户名和密码是否正确4.状态保持5.重定向
        query_dict = request.POST
        username = query_dict.get('username')
        password = query_dict.get('password')
        remembered = query_dict.get('remembered')
        if all([username, password]) is False:
            return http.HttpResponseForbidden('缺少必传递参数')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return http.HttpResponseForbidden('用户名或密码错误')
        login(request, user)
        if remembered is None:
            request.session.set_expiry(0)
        # return http.HttpResponse('跳转到首页')
        response = redirect('/')
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE if remembered == 'on' else None)
        return response

