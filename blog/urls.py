from django.urls import path
from unicodedata import category

from blog import views

urlpatterns = [
    #Template
    path('',views.blog_list, name='blog_list'),
    path('<int:blog_id>',views.blog_detail, name='blog_detail'),
    #API
    path('api/',views.BlogListViewAPI.as_view(),name='api_blog_list'),
    path('api/category/',views.BlogCategoryListAPIView.as_view(),name='api_blog_list_category'),
]