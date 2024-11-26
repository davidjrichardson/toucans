from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.shortcuts import render
from django.views.generic.base import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


def response_403_handler(request, exception=None):
    return render(request, '403.html', status=403)


def response_400_handler(request, exception=None):
    return render(request, '400.html', status=400)


def response_404_handler(request, exception=None):
    return render(request, '404.html', status=404)


def response_500_handler(request, exception=None):
    return render(request, '500.html', status=500)


urlpatterns = [
    re_path(r'^sitemap\.xml', sitemap),
    re_path(
        r'^robots\.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
    ),
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    re_path(r'^pages/', include(wagtail_urls)),
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
