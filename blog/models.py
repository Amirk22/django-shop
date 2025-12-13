from django.db import models
from accounts.models import User
from slugify import slugify

# Create your models here.


class BlogCategory(models.Model):
    title = models.CharField(max_length=100 ,verbose_name='عنوان')
    e_name = models.CharField(max_length=100 ,verbose_name='هنوان انگلیسی')
    slug = models.SlugField(max_length=100 ,verbose_name='URL')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


    def save(self,*args,**kwargs):
        self.slug = slugify(self.e_name)
        super().save(*args,**kwargs)



    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=30 ,verbose_name= 'عنوان')
    short_description = models.CharField(max_length=100,verbose_name= 'توضیحات کوتاه')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE,verbose_name= 'دسته بندی')
    content = models.TextField(verbose_name= 'محتوا')
    image = models.ImageField(upload_to="blog/images/",verbose_name= 'عکس')
    author = models.ForeignKey(User, on_delete=models.CASCADE , editable=False,verbose_name= 'نویسنده')
    is_active = models.BooleanField(default=True,verbose_name= 'فعال')
    created_at = models.DateTimeField(auto_now_add=True, editable=False ,verbose_name= 'زمان ساخت مقاله')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'

    def __str__(self):
        return self.title