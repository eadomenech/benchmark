# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
from django.urls import path
from django.contrib import admin
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    # url(r'^index/$', index, name='index'),
    path('logout', views.logout, name='logout'),
    path('cambiar_passwd', views.cambiar_passwd, name='cambiar_passwd'),
    path('uploads_simple', views.simple_upload, name='simple_upload'),
    # path('uploads_form/$', views.model_form_upload, name='model_form_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
