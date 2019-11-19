from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^/usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.RegisterView.as_view(), name='register'),
    url(r'^/mobiles/(?P<mobile>1[3-9]\d{9})/count/$',views.UsernameCountView.as_view()),
    url(r'^/verification(?P<verification>/(?P<uuid>[\w-]+)/)/count/$', views.ImageCodeView.as_view())
]