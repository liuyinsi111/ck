from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^username/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UsernameCountView.as_view(), name='username'),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view(), name='mobiles'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='login'),
    url(r'^info/$', views.InfoView.as_view(), name='info'),
    url(r'^emails/$', views.EmailView.as_view()),
    url(r'^emails/verification/$', views.EmailVerifyView.as_view()),
    url(r'^addresses/$', views.AddressView.as_view()),
    url(r'^addresses/create/$', views.AddressCreateView.as_view()),
    url(r'^browse_histories/$', views.UserBrowseHistory.as_view()),

]