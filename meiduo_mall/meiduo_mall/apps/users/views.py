from django.shortcuts import render, redirect
from django.views import View
from django import http
import re
from django.contrib.auth import login, authenticate, logout
from django_redis import get_redis_connection
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.db.utils import DataError, DatabaseError

from .models import User, Address
from meiduo_mall.utils.views import LoginRequiredView
from meiduo_mall.utils.response_code import RETCODE
from celery_tasks.email.tasks import send_verify_url
from .utils import generate_email_verify_url, get_user_token
import logging

logger = logging.getLogger('django')

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
        response = redirect(request.GET.get('next') or '/')
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE if remembered == 'on' else None)
        return response

class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect('/login/')
        response.delete_cookie('username')
        return response

# class InfoView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             return render(request, 'user_center_info.html')
#         else:
#             return redirect('/login/?next=/info/')
class InfoView(LoginRequiredMixin, View):
    def get(self, request):
        # if request.user.is_authenticated:
        #     return render(request, 'user_center_info.html')
        # else:
        #     return redirect('/login/?next=/info')
        return render(request, 'user_center_info.html')


class EmailView(LoginRequiredView):
    """设置邮箱"""

    def put(self, request):
        # 1. 接收
        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')
        # 2. 校验
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('邮箱格式有误')

        # 3. 修改user的email字段, save
        user = request.user
        if user.email == '':  # 只有当用户真的没有邮箱时再去设置
            user.email = email
            user.save()

        verify_url = generate_email_verify_url(user)
        # 添加到celery任务队列
        send_verify_url.delay(email, verify_url)
        # 4. 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class EmailVerifyView(View):
    """激活邮箱"""

    def get(self, request):
        # 1.接收查询参数token
        token = request.GET.get('token')
        # 2. 对token进行解密
        user = get_user_token(token)
        # 判断是否拿到user,如果有
        if user is None:
            return http.HttpResponseForbidden('邮箱激活失败')
        # 将user的email_active改国True 再save
        user.email_active = True
        user.save()
        # 响应
        # return render(request, 'user_center_info.html')
        return redirect('/info/')

class AddressView(LoginRequiredView):
    """用户收货地址"""

    def get(self, request):
        user = request.user
        # 查询当前用户未逻辑删除的所有收货地址
        address_qs = Address.objects.filter(user=user, is_deleted=False)

        # 模型转字典并包装到列表中
        address_list = []
        for address in address_qs:
            address_list.append({
                'id': address.id,
                'title': address.title,
                'receiver': address.receiver,
                'province_id': address.province_id,
                'province': address.province.name,
                'city_id': address.city_id,
                'city': address.city.name,
                'district_id': address.district_id,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email,
            })

        context = {
            'addresses': address_list,  # 用户的所有收货地址
            'default_address_id': user.default_address_id
        }
        return render(request, 'user_center_site.html', context)