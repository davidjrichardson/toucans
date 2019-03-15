from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.shortcuts import render
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views


def response_403_handler(request, exception=None):
    return render(request, '403.html', status=403)


def response_400_handler(request, exception=None):
    return render(request, '400.html', status=400)


def response_404_handler(request, exception=None):
    return render(request, '404.html', status=404)


def response_500_handler(request, exception=None):
    return render(request, '500.html', status=500)


urlpatterns = [
    url(r'^sitemap\.xml', sitemap),
    url(r'^admin/', admin.site.urls),

    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]

handler_403 = response_403_handler
handler_400 = response_400_handler
handler_404 = response_404_handler
handler_500 = response_500_handler

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
