from rest_framework import serializers

from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    product_final_price = serializers.DecimalField(source='product.final_price', read_only=True, max_digits=10, decimal_places=2)
    has_discount = serializers.BooleanField(source='product.has_discount', read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
