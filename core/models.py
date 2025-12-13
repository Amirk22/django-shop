from django.db import models
from products.models import ProductSubCategory


# Create your models here.
class Banner(models.Model):
    class SiteBannerPositions(models.TextChoices):
        home_page_1 = 'home1' , 'بنر اول برای صفحه اصلی'
        home_page_2 = 'home2' , 'بنر دوم برای صفحه اصلی'
        home_page_3 = 'home3' , 'بنر سوم برای صفحه اصلی'


    title = models.CharField(max_length=100,verbose_name='عنوان بنر')
    url = models.URLField(max_length=200,null=True,blank=True,verbose_name='آدرس بنر')
    image = models.ImageField(upload_to='banners/images',verbose_name='تصویر بنر')
    is_active = models.BooleanField(default=True,verbose_name='فعال/غیرفعال')
    position = models.CharField(max_length=20,choices=SiteBannerPositions.choices,verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'


class Slider(models.Model):
    title = models.CharField(max_length=100 , verbose_name='عنوان اسلایدر')
    image = models.ImageField(upload_to='slider/images', verbose_name='عکس اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'


class ProductHomePage(models.Model):
    class ProductHomePagePositions(models.TextChoices):
        product_category_home_page_1 = 'product_home1' , 'نمایش محصولات در اولین دسته بندی'
        product_category_home_page_2 = 'product_home2' , 'نمایش محصولات در دومین دسته بندی'


    category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE,verbose_name='دسته بندی')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    position = models.CharField(max_length=20,choices=ProductHomePagePositions.choices,verbose_name='جایگاه نمایشی')

    class Meta:
        verbose_name = 'نمایش محصولات دسته بندی در صفحه اصلی'
        verbose_name_plural = 'نمایش محصولات دسته بندی ها در صفحه اصلی'


class ListFooter(models.Model):
    txt = models.CharField(max_length=100, verbose_name='متن لیست فوتر')

    class Meta:
        verbose_name = 'محتوای لیست فوتر'
        verbose_name_plural = 'محتوای لیست فوتر'

    def __str__(self):
        return self.txt
