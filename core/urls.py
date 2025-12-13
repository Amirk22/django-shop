from django.urls import path
from . import views
from .views import BannerAPIView, SliderAPIView

urlpatterns = [
    #Template
    path('',views.home,name= 'home_page'),
    #API
    path('banner/api/',BannerAPIView.as_view(),name = 'banner-api'),
    path('slider/api/',SliderAPIView.as_view(),name = 'slider-api'),
]