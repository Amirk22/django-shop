from django.contrib import admin

from contact_us.models import Contact

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ['__str__','name']

admin.site.register(Contact , ContactAdmin)