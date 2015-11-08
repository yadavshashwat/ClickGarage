from django.conf.urls import include, url

urlpatterns = [
    url(r'^index/?$','website.views.index',name='index'),
    url(r'^order/?$','website.views.order',name='order'),
    url(r'^.','website.views.defResponse',name='defResponse'),
    url(r'^$','website.views.index',name='index'),

   url(r'^ajax-uploader/', include('ajaxuploader.urls', namespace='ajaxuploader', app_name='ajaxuploader')),
]
