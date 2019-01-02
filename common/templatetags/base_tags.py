from django import template

from home.models import Footer

register = template.Library()


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


@register.filter()
def last_three(l):
    return l[-3:-1]


@register.filter()
def first_three(l):
    return l[1:3]


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.inclusion_tag('common/tags/footer.html', takes_context=True)
def footer(context):
    # TODO: Get all of the items marked to be in a menu bar
    # Standings, Schedule, News, League, Records, Resources (in that order)

    return {
        'facebook_url': Footer.objects.first().facebook_url if Footer.objects.first() else None,
        'twitter_url': Footer.objects.first().twitter_url if Footer.objects.first() else None,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('common/tags/footer_menu_child.html', takes_context=True)
def footer_menu_child(context, parent):
    # Get only the children
    children = parent.get_children().live().in_menu()

    return {
        'parent': parent,
        'child_items': children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('common/tags/navbar.html', takes_context=True)
def navigation(context, calling_page=None):
    # Get all of the items marked to be in a menu bar
    menu_items = context['request'].site.root_page.get_children().live().in_menu()

    for item in menu_items:
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        item.active = (calling_page.url.startswith(item.url) if calling_page else False)

    return {
        'is_home': (calling_page.url == u'/' if calling_page else False),
        'menu_items': menu_items,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
