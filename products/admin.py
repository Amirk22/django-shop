from django.contrib import admin

from .models import Product, Brand, ProductGallery, ProductCategory, ProductSubCategory , ProductVisit , Comment ,CommentReply


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','is_active']

class ProductCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

class ProductSubCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

class ProductBrandAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product','image']

admin.site.register(Product,ProductAdmin)
admin.site.register(Brand,ProductBrandAdmin)
admin.site.register(ProductGallery,ProductGalleryAdmin)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(ProductSubCategory,ProductSubCategoryAdmin)
admin.site.register(ProductVisit)
admin.site.register(Comment)
admin.site.register(CommentReply)


