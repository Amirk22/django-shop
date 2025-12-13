from django.shortcuts import render, get_object_or_404 , redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, Product
import json

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, Product
import json
from django.contrib.auth.decorators import login_required

from .serializers import CartSerializer


def add_to_cart_form_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    items = Cart.objects.filter(user=request.user)
    is_item = Cart.objects.filter(user=request.user).exists()
    total = sum([item.product.price * item.quantity for item in items])
    total_discount = sum([
        (item.product.final_price if item.product.has_discount else item.product.price) * item.quantity
        for item in items
    ])
    total_profit = sum([(item.product.price -item.product.final_price) * item.quantity for item in items if item.product.has_discount])
    has_discount_in_cart = any([item.product.has_discount for item in items])
    return render(request, 'cart/cart.html', {'items': items, 'total': total , 'total_discount': total_discount , 'has_discount_in_cart': has_discount_in_cart , 'total_profit': total_profit , 'is_item': is_item})

def add_cart_item_quantity(request, product_id):
    cart_item =Cart.objects.get(user=request.user, product=Product.objects.get(id=product_id))
    if request.method == "POST":
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')

def remove_cart_item_quantity(request, product_id):
    cart_item =Cart.objects.get(user=request.user, product=Product.objects.get(id=product_id))
    if request.method == "POST":
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
        return redirect('cart')

def delete_item_card(request, product_id):
    cart_item =Cart.objects.get(user=request.user, product=Product.objects.get(id=product_id))
    cart_item.delete()
    return redirect('cart')

#.................................................. API
class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()
            return Response({'message': 'تعداد محصول در سبد خرید افزایش یافت'}, status=status.HTTP_200_OK)

        return Response({'message': 'محصول جدید به سبد خرید اضافه شد'}, status=status.HTTP_201_CREATED)

class CartViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Cart.objects.filter(user=request.user)
        data = []
        for item in items:
            data.append({
                'id': item.id,
                'product': item.product.id,
                'quantity': item.quantity,
            })
        return Response({'items': data})

class AddCartItemQuantityAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            cart_item.quantity += 1
            cart_item.save()
            return Response({'message': 'کلا با موفقیت به سبد خرید اضافه شد'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'آیتمی یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

class RemoveCartItemQuantityAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
            else:
                cart_item.save()
                return Response({'message': 'Quantity decreased successfully'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

class DeleteCartItemAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)



