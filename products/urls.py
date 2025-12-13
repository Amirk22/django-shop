from django.urls import path
from . import views
from .models import Product
urlpatterns = [
    path('product-list-discount/', views.ProductListDiscount.as_view(),name = 'product-list-discount'),
    path('<slug:category_slug>/<slug:subcategory_slug>',views.ProductList.as_view(),name='product_list'),
    path('<slug:brand_slug>/',views.ProductListBrand.as_view(),name='product_list_brand'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<int:pk>/', views.ProductDetail.as_view(),name = 'product_detail'),
    # API
    path('api/category/', views.ProductCategoryAPIView.as_view(), name='product_subcategory_api'),
    path('api/subcategory/', views.ProductSubCategoryAPIView.as_view(), name='product_subcategory_api'),
    path('api/brand/', views.ProductBrandAPIView.as_view(), name='product_list_brand_api'),
    path('api/gallery/', views.ProductGalleryAPI.as_view(), name='product_gallery_api'),
    path('api/visit/', views.ProductVisitAPIView.as_view(), name='product_visit_api'),
    path('api/comment/', views.CommentVisitAPIView.as_view(), name='comment_api'),
    path('api/comment-reply/', views.CommentReplyVisitAPIView.as_view(), name='comment_reply_api'),
    path('api/product/', views.ProductListAPI.as_view(), name='product_list_api'),
    path('api/product-list-discount/', views.ProductListDiscountAPIView.as_view(), name='product-list-discount_api'),
    path('api/<slug:category_slug>/<slug:subcategory_slug>', views.ProductListFilterWithCategoryAPIView.as_view(), name='product_list_filter_with_category_api'),
    path('api/<slug:brand_slug>/', views.ProductFilterWithBrandAPIView.as_view(), name='product_list_filter_with_brand_api'),
]