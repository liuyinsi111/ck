from django.shortcuts import render

from django_redis import get_redis_connection
from django.views import View
from django import http
from meiduo_mall.libs.captcha.captcha import captcha
#TODO 没有导captcha

class ImageCodeView(View):
    def get(self, request, uuid):
        name, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex(uuid, 300, text)
        return http.HttpResponse(image, content_type='image/png')
