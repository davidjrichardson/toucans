from django import template

register = template.Library()

@register.inclusion_tag('common/tags/navbar.html', takes_context=True)
def navigation(context, calling_page=None):
    pass