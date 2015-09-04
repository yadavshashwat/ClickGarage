"""clickgarage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from activity import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include('api.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    # url(r'', include('social_auth.urls')),
    # url(r'^index/',include('website.urls')),
    # url(r'^login/','website.views.login',name='order'),
    url(r'^order/','website.views.order',name='order'),
    url(r'^order$','website.views.order',name='order'),
    url(r'^checkout/','website.views.checkout',name='checkout'),
    url(r'^checkout','website.views.checkout',name='checkout'),
    url(r'^loginPage','website.views.loginPage',name='loginPage'),
    url(r'^$','website.views.index',name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^auth/', views.auth_and_login, name='auth_and_login'),
    url(r'^signup/', views.sign_up_in, name='sign_up_in'),
    # url(r'^login/(\w*)', views.social_login, name='social_login'),
    url(r'^logout/', views.logout, name='logout')
]