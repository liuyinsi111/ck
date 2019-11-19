from django.shortcuts import render

from django_redis import get_redis_connection
from django.views import View
from django import http
from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.response_code import RETCODE


class ImageCodeView(View):
    def get(self, request, uuid):
        name, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex(uuid, 300, text)
        return http.HttpResponse(image, content_type='image/png')

class SMSCodeView(View):
    def get(self, request, mobile):
        query_dict = request.GET

        image_code_client = query_dict.get('image_code')
        uuid = query_dict.get('uuid')
        if all([image_code_client, uuid]) is False:
            return http.HttpResponse('缺少必传参数')
        redis_conn = get_redis_connection('verify_codes')
        image_code_server_bytes = redis_conn.get(uuid)
        if image_code_server_bytes is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg':'图形验证码已过期'})
        image_code_server = image_code_server_bytes.decode()
        if image_code_client.lower() != image_code_server.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码填写错误'})