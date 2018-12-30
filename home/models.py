from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet


@register_snippet
class Footer(models.Model):
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)

    panels = [
        FieldPanel('facebook_url'),
        FieldPanel('twitter_url'),
    ]

    def __str__(self):
        return 'Footer URLs'


class BlogPage(Page):
    pass


class HomePage(Page):
    description = models.TextField(max_length=400, default='')

    @property
    def posts(self):
        return BlogPage.objects.live().order_by('-first_published_at')[:5]

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]
