from django.urls import path
from . import views

urlpatterns = [
    #Template
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart_form_detail, name='cart_add'),
    path('add-to/<int:product_id>/', views.add_to_cart_form_detail, name='add_to_item_cart'),
    path('remove-to/<int:product_id>/', views.remove_cart_item_quantity, name='remove_to_item_cart'),
    path('delete/<int:product_id>/', views.delete_item_card, name='delete_item_card'),
    #API
    path('api/', views.CartViewAPI.as_view(), name='api_cart_view'),
    path('api-to/add/<int:product_id>/', views.AddCartItemQuantityAPI.as_view(), name='api_add_cart_item'),
    path('api/remove/<int:product_id>/', views.RemoveCartItemQuantityAPI.as_view(), name='api_remove_cart_item'),
    path('api/delete/<int:product_id>/', views.DeleteCartItemAPI.as_view(), name='api_delete_cart_item'),
    path('api/add/<int:product_id>/', views.AddToCartAPIView.as_view(), name='api_cart_view'),
]