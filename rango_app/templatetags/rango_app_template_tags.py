from django import template
from rango_app.models import Category

register = template.Library()

@register.inclusion_tag('rango_app/cats.html')
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list




