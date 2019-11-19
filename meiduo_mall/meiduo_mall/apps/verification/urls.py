from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^/verification(?P<verification>/(?P<uuid>[\w-]+)/)/count/$', views.ImageCodeView.as_view())
]