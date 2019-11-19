from django.shortcuts import render
from django.views.generic import View
from django import http
import re
from .models import User
from django.contrib.auth import login

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
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        #TODO：短信验证码的验证代码后期补充
        user = User.objects.create(
            username=username,
            password=password,
            mobile=mobile
        )
        # user.set_password(password)
        # user.save()
        # user.check_password()
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        login(request, user)
        return http.HttpResponse('注册成功即代表登陆成功')



class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'count': count})

class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(username=mobile).count()
        return http.JsonResponse({'count': count})