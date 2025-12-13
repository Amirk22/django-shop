from django.urls import path
from . import views
urlpatterns = [
    path('', views.ContactUSView.as_view(), name='contact_us'),
    path('api/', views.ContactUsAPIView.as_view(), name='contact_us_api'),
]