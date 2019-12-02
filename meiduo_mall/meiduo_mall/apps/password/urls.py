from django.conf.urls import url

from . import views

urlpatterns = [
            #找回密码的路由
    url(r'^find_password/$', views.FindPasswordView.as_view()),
]