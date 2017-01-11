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
# from django.conf.urls import include, url

from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.conf import settings
from activity import views


    # (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT }),


urlpatterns = patterns('',
              (r'^mobile/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MOBILE_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include('api.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    # url(r'^ajax-uploader/', include('ajaxuploader.urls', namespace='ajaxuploader', app_name='ajaxuploader')),
    url(r'^logout/', views.logout_to_home, name='logout_to_home'),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    # url(r'', include('social_auth.urls')),
    # url(r'^index/',include('website.urls')),
    # url(r'^login/','website.views.login',name='order'),
    url(r'^order/?$','website.views.order',name='order'),

    # url(r'^order$','website.views.order',name='order'),
    url(r'^order/(?P<carName>[a-zA-Z0-9\-]*)/(?P<city>[a-zA-Z\-]*)/?$','website.views.orderParse',name='orderParse'),
    url(r'^order_new/(?P<carName>[a-zA-Z0-9\-]*)/(?P<city>[a-zA-Z\-]*)/?$','website.views.orderParseNew',name='orderParseNew'),
    url(r'^checkout/','website.views.checkout',name='checkout'),
    url(r'^checkout','website.views.checkout',name='checkout'),
    url(r'^dashboard','website.views.dashboard',name='dashboard'),
    url(r'^dashboard/','website.views.dashboard',name='dashboard'),
    url(r'^cart','website.views.cart',name='cart'),
    url(r'^cart/','website.views.cart',name='cart'),
    url(r'^upload_test/','website.views.upload_test',name='upload_test'),
    url(r'^loginPage','website.views.loginPage',name='loginPage'),
    url(r'^cars/$','website.views.index',name='index'),
    url(r'^bikes/$','website.views.index',name='index'),
    url(r'^cars/(?P<service>[a-zA-Z0-9\-]*)/$','website.views.ad_landing_cars',name='ad_landing_cars'),
    url(r'^bikes/(?P<service>[a-zA-Z0-9\-]*)/$','website.views.ad_landing_bikes',name='ad_landing_bikes'),
    url(r'^$','website.views.index',name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^auth/', views.auth_and_login, name='auth_and_login'),
    url(r'^signup/', views.sign_up_in, name='sign_up_in'),
    # url(r'^login/(\w*)', views.social_login, name='social_login'),
    url(r'^privacy/', 'website.views.privacy', name='privacy'),
    url(r'^cancel/', 'website.views.cancel', name='cancel'),
    url(r'^tnc/', 'website.views.tnc', name='tnc'),
    url(r'^history/', 'website.views.history', name='history'),
    url(r'^history$','website.views.history',name='history'),
    url(r'^adminpanel$','website.views.adminpanel',name='adminpanel'),	
    url(r'^mobile/', 'website.views.mobile', name='mobile'),
    url(r'^driver1/', 'website.views.drivers', name='drivers'),
    url(r'^sitemap/', 'website.views.sitemap', name='sitemap'),
    url(r'^contact/', 'website.views.contact', name='contact'),
#    url(r'^service-schedule/', 'website.views.serviceSchedule', name='serviceSchedule'),
    url(r'^service-schedule/(?P<carName>[a-zA-Z0-9\-]*)/','website.views.serviceSchedule',name='serviceSchedule'),

                       # website revamp
    url(r'^/advert/Car/', 'website.views.advert', name='advert'),
    url(r'^index_new/', 'website.views.index_new', name='index_new'),
    url(r'^get_quote/', 'website.views.get_quote', name='get_quote'),
    url(r'^(?P<veh_type>[a-zA-Z0-9\-_ ]+)/(?P<veh>[a-zA-Z0-9\-_ ]+)/$', 'website.views.get_quote', name='get_quote'),
    url(r'^(?P<veh_type>[a-zA-Z0-9\-_ ]+)/(?P<veh>[a-zA-Z0-9\-_ ]+)/(?P<service>[a-zA-Z0-9\-_ ]+)/$', 'website.views.get_quote', name='get_quote'),
    url(r'^(?P<veh_type>[a-zA-Z0-9\-_ ]+)/(?P<veh>[a-zA-Z0-9\-_ ]+)/checkout/$', 'website.views.get_quote',name='get_quote'),
)
