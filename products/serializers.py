from rest_framework import serializers
from .models import Product, ProductSubCategory, ProductCategory, Brand, ProductGallery, ProductVisit ,Comment ,CommentReply



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    parent = CategorySerializer(read_only=True)
    class Meta:
        model = ProductSubCategory
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVisit
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = '__all__'
