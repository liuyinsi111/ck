from django.shortcuts import render

from django_redis import get_redis_connection
from django.views import View
from django import http
from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.response_code import RETCODE
from meiduo_mall.libs.yuntongxun.sms import CCP
from random import randint
import logging
from . import constants

logger = logging.getLogger('django')



class ImageCodeView(View):
    def get(self, request, uuid):
        name, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex(uuid, 300, text)
        redis_conn.delete(uuid)
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

        # CCP().send_template_sms('接收短信的手机号', ['验证码', '提示用户的过期时间：单妙分钟'], 1)

        sms_code = '%06d'% randint(0,999999)
        logger.info(sms_code)
        #except里面用error（）
        #随机生成6位数字，为了方便测试将验证码发到控制台
        CCP().send_template_sms('接收短信的手机号', ['验证码', '提示用户的过期时间：单秒分钟'], 1)
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_EXPIRE, sms_code)
        #保存验证码到redis，方便以后验证
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
    #ok代表字符串0，


