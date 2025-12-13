from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50,verbose_name='نام')
    email = models.EmailField(max_length=200,verbose_name='ایمیل')
    subject = models.CharField(max_length=100,verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name ='تماس'
        verbose_name_plural = 'تماس ها'