"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('users.urls', namespace='users')),
    url(r'^', include('verification.urls', namespace='verification')),
    url(r'^', include('contents.urls', namespace='contents')),
    url(r'^', include('oauth.urls', namespace='oauth')),
    url(r'^', include('areas.urls', namespace='areas')),  # 省市区模块
    url(r'^', include('goods.urls', namespace='goods')),  # 省市区模块
    url(r'^', include('carts.urls', namespace='carts')),
    url(r'^', include('orders.urls', namespace='orders')),
    url(r'^', include('payment.urls', namespace='payment')),
    url(r'^', include('password.urls', namespace='password')),
    url(r'^', include('meiduo_admin.urls', namespace='meiduo_admin')),

]