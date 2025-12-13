from django.db import models
from django.core.validators import MinValueValidator
from slugify import slugify
from accounts.models import User
from django.utils import timezone
from django.db.models import Q, F

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=225,verbose_name='عنوان محصول')
    price = models.IntegerField(verbose_name='قیمت محصول', validators=[MinValueValidator(1)])
    description = models.TextField(verbose_name='توضیحات محصول', blank=True, null=True)
    category = models.ForeignKey('ProductSubCategory',on_delete=models.CASCADE,related_name='products',verbose_name='دسته بندی')
    brand = models.ForeignKey('Brand',on_delete = models.CASCADE,related_name='products',null=True,blank=True,verbose_name='برند')
    image = models.ImageField(upload_to='products/images/', verbose_name='عکس اصلی')
    color = models.CharField(max_length=100, verbose_name='رنگ', blank=True, null=True)
    size = models.CharField(max_length=100, verbose_name='سایز', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inventory = models.PositiveIntegerField(default=0, verbose_name='تعداد موجودی')
    discount_price = models.IntegerField(verbose_name='قیمت تخفیف خورده',null=True,blank=True, validators=[MinValueValidator(1)])
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    single_product = models.BooleanField(default=False,verbose_name='نمایش تکی در صفحه اصلی')

    class Meta:
        verbose_name= 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    @property
    def has_discount(self):
        if not self.discount_price:
            return False
        now = timezone.now()
        if self.discount_price is None:
            return False
        if self.discount_start and now < self.discount_start:
            return False
        if self.discount_end and now > self.discount_end:
            return False
        return True
    @property
    def final_price(self):
        if self.has_discount:
            return self.discount_price
        return self.price


class ProductCategory(models.Model):
    title= models.CharField(max_length=300,verbose_name='عنوان دسته بندی')
    e_title = models.CharField(max_length=200, verbose_name='عنوان لاتین دسته بندی')
    slug = models.SlugField(default='',unique=True,db_index=True,verbose_name='اسلاگ دسته بندی')

    def save(self,*args,**kwargs):
        self.slug = slugify(self.e_title)
        super().save(*args,**kwargs)
    
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class ProductSubCategory(models.Model):
    title= models.CharField(max_length=300,verbose_name='عنوان ریز دسته بندی')
    e_title = models.CharField(max_length=200, verbose_name='عنوان لاتین ریز دسته بندی')
    parent = models.ForeignKey('ProductCategory',on_delete=models.CASCADE, related_name='subcategories',verbose_name='دسته اصلی')
    slug = models.SlugField(default='',unique=True,db_index=True, verbose_name='اسلاگ ریز دسته بندی')

    def save(self,*args,**kwargs):
        self.slug = slugify(self.e_title)
        super().save(*args,**kwargs)


    class Meta:
        verbose_name = 'ریز دسته بندی'
        verbose_name_plural = 'ریز دسته بندی ها'


    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=200,verbose_name='عنوان برند')
    e_title = models.CharField(max_length=200,verbose_name= 'عنوان انگلیسی برند')
    image = models.ImageField(null=True,blank=True,upload_to='products/brand/', verbose_name='لوگو برند')
    slug = models.SlugField(default='', unique=True, db_index=True, verbose_name='اسلاگ برند')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.e_title)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'برند'
        verbose_name_plural =  'برند ها'

    def __str__(self):
        return self.title


class ProductGallery(models.Model):
    product=models.ForeignKey('Product',on_delete=models.CASCADE,verbose_name='محصول')
    image = models.ImageField(upload_to='products/gallery/', verbose_name='عکس گالری')

    class Meta:
        verbose_name = 'گالری عکس'
        verbose_name_plural = 'گالری عکس ها'

    def __str__(self):
        return self.product.title


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE , verbose_name= 'محصول')
    ip = models.CharField(max_length=30,verbose_name='IP')
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE , verbose_name= 'کاربر')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    name = models.CharField(max_length=100 ,verbose_name='نام')
    massage = models.TextField(verbose_name='پیام')
    def __str__(self):
        return self.massage

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class CommentReply(models.Model):
    comment = models.ForeignKey('Comment' , on_delete=models.CASCADE , verbose_name='کامنت')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    name = models.CharField(max_length=100, verbose_name='نام')
    massage = models.TextField(verbose_name='پیام')

    def __str__(self):
        return self.massage

    class Meta:
        verbose_name = 'پاسخ نظر'
        verbose_name_plural = 'پاسخ نظرات'

