from django.contrib import admin

from blog.models import Blog, BlogCategory

# Register your models here.


class BlogCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Blog , BlogAdmin)
admin.site.register(BlogCategory ,BlogCategoryAdmin)