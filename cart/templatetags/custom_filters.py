from django import template

register = template.Library()

@register.filter
def price_format(value):
    try:
        return f"{int(value):,}"
    except:
        return value


@register.filter
def mul(value, arg):
    return value * arg