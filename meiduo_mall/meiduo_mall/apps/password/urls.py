from django.conf.urls import url

from . import views

urlpatterns = [
            #找回密码的路由
    url(r'^find_password/$', views.FindPasswordView.as_view()),
    url(r'^accounts/(?P<username>[a-zA-Z0-9_-]{5,20})/sms/token/$', views.account.as_view()),
    # url(r'^sms_codes/$', views.SmsCodesView.as_view()),


]