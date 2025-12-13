from core.models import Banner, Slider, ProductHomePage, ListFooter
from products.models import ProductCategory, ProductSubCategory, Product, Brand
from django import template

register = template.Library()

@register.inclusion_tag('site_header_partial.html', takes_context=True)
def site_header_partial(context):
    request = context['request']
    user = request.user
    categories = ProductCategory.objects.all()
    subcategories = ProductSubCategory.objects.all()
    return {'categories': categories, 'subcategories': subcategories, 'request': request ,'user': user}

@register.inclusion_tag('site_footer_partial.html', takes_context=True)
def site_footer_partial(context):
    request = context['request']
    list_footer = ListFooter.objects.all()
    return {'list_footer': list_footer, 'request': request}