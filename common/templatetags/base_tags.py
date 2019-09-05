import mimetypes
from collections import OrderedDict

from django import template

from home.models import Footer, BlogIndexPage, BlogPage, LegacyStandingsPage, SchedulePage, StandingsIndexPage, \
    GenericPage, \
    ResourcePage, NewStandingsPage

register = template.Library()


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


@register.filter
def contains_title(streamfield):
    return bool([x for x in streamfield if x.block_type == 'h2' or x.block_type == 'h3' or x.block_type == 'h4'])


@register.filter
def get_image_mime_type(image):
    return mimetypes.guess_type(image.url)[0]


@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None


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
    # Get the site root to find top-level pages
    root = context['request'].site.root_page
    # Find the navbar-level categories
    standings = NewStandingsPage.objects.live().child_of(root).order_by('-standings_year').first()
    standings_archive = StandingsIndexPage.objects.live().child_of(standings).first()
    schedule = SchedulePage.objects.live().child_of(root).first()
    news_root = BlogIndexPage.objects.live().child_of(root).first()
    news_article = BlogPage.objects.live().child_of(news_root).order_by('-date').first()
    league = GenericPage.objects.live().child_of(root).filter(title__iexact='league').first()
    league_subpages = GenericPage.objects.live().child_of(league).all()
    records = GenericPage.objects.live().child_of(root).filter(title__iexact='records').first()
    records_subpages = GenericPage.objects.live().child_of(records).all()
    resources = ResourcePage.objects.live().child_of(root).first()
    resources_subpages = ResourcePage.objects.live().child_of(resources).all()

    return {
        # Footer link categories
        'standings': standings,
        'standings_archive': standings_archive,
        'schedule': schedule,
        'news': news_root,
        'news_article': news_article,
        'league': league,
        'league_subpages': league_subpages,
        'records': records,
        'records_subpages': records_subpages,
        'resources': resources,
        'resources_subpages': resources_subpages,
        # Social media links
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


@register.inclusion_tag('common/tags/sidebar.html', takes_context=True)
def sidebar(context):
    blog_index = BlogIndexPage.objects.live().in_menu().first()
    archives = OrderedDict()

    for blog in BlogPage.objects.live().order_by('-date'):
        archives.setdefault(blog.date.year, {}).setdefault(blog.date.month, []).append(blog)

    return {
        'blog_index': blog_index,
        'archives': archives,
        'request': context['request']
    }


@register.inclusion_tag('common/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, calling_page):
    parent_list = []

    current = calling_page
    while current.depth >= 3:
        parent_list = [current] + parent_list
        current = current.get_parent()

    return {
        'request': context['request'],
        'parent_list': parent_list,
        'calling_page': calling_page
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


@register.simple_tag
def date_filter(year, month):
    return "{year}-{month:02d}".format(year=year, month=month)


@register.simple_tag
def filters_to_str(tag, date):
    filter_str = 'Post(s)'
    if tag:
        filter_str += ' marked as "{tag}"'.format(tag=tag)

    if date:
        # date is YYYY-MM -->
        year, month = date.split("-")
        month = int(month)
        filter_str += ' from {month} {year}'.format(month=to_month_str(month), year=year)

    return filter_str


@register.filter
def to_month_str(value):
    return {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
    }[value]
