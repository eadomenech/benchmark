from django.urls import path
from . import views

app_name = 'watermarking'
urlpatterns = [
    path('', views.index, name='index'),
    path('methods', views.ListWatermarking.as_view(), name='methods'),
    path(
        'detail/<int:pk>/', views.DetailWatermarking.as_view(),
        name='detail'),
    path('newMethod', views.CreateWatermarking.as_view(), name='newMethod'),
    path('coverImages', views.ListCoverImage.as_view(), name='coverImages'),
    path(
        'detail_coverImage/<int:pk>/', views.DetailCoverImage.as_view(),
        name='detail_coverImage'),
    path(
        'newCoverImage', views.CreateCoverImage.as_view(),
        name='newCoverImage'),
    path(
        'watermarkImages', views.ListWatermarkImage.as_view(),
        name='watermarkImages'),
    path(
        'detail_watermarkImage/<int:pk>/', views.DetailWatermarkImage.as_view(),
        name='detail_watermarkImage'),
    path(
        'newWatermarkImage', views.CreateWatermarkImage.as_view(),
        name='newWatermarkImage'),
    path(
        'metrics', views.ListMetric.as_view(),
        name='metrics'),
    path(
        'detail_metric/<int:pk>/', views.DetailMetric.as_view(),
        name='detail_metric'),
    path(
        'newMetric', views.CreateMetric.as_view(),
        name='newMetric'),
]
