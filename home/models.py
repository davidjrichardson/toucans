from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StructBlock, DateBlock, CharBlock, TextBlock, StreamBlock, IntegerBlock, StaticBlock, \
    ListBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
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


class LeagueStartDateBlock(StructBlock):
    start_date = DateBlock(
        required=True,
        help_text="The start date of the B.U.T.T.S. League for the year"
    )

    class Meta:
        label = 'League start date'
        icon = 'date'


class LeagueNewYearBlock(StructBlock):
    new_year = IntegerBlock(
        required=True,
        help_text="The new year for the league"
    )

    class Meta:
        label = 'New year marker'
        icon = 'date'


class LeagueEndBlock(StaticBlock):
    class Meta:
        label = 'League end marker'
        icon = 'date'


class LeagueLegBlock(StructBlock):
    leg_name = TextBlock(
        required=True,
        help_text="The name of this leg e.g.: \"B.U.T.T.S. Leg 2 (Oxford)\""
    )
    leg_host = TextBlock(
        required=True,
        help_text="The host club of this B.U.T.T.S. Leg"
    )
    leg_date = DateBlock(
        required=True,
        help_text="The date of this B.U.T.T.S. Leg"
    )
    leg_attendees = TextBlock(
        required=True,
        help_text="The clubs attending this B.U.T.T.S. Leg, separated by a comma"
    )

    class Meta:
        label = 'Tournament leg'
        icon = 'table'


class LeagueCombinedLegBlock(ListBlock):
    class Meta:
        label = 'Combined tournament leg'
        icon = 'table'
        admin_text = 'For when two legs are on the same weekend'


class LeagueChampsBlock(StructBlock):
    champs_name = TextBlock(
        required=True,
        help_text="The name of this championship e.g.: \"B.U.T.T.S. Field Champs\""
    )
    champs_venue = TextBlock(
        required=True,
        help_text="The host club of this championship event"
    )
    champs_date = DateBlock(
        required=True,
        help_text="The date of this championship event"
    )

    class Meta:
        label = 'Champs'
        icon = 'pick'


class TimelineStreamBlock(StreamBlock):
    league_start_block = LeagueStartDateBlock()
    league_combined_leg_block = LeagueCombinedLegBlock(LeagueLegBlock())
    league_leg_block = LeagueLegBlock()
    league_champs_block = LeagueChampsBlock()
    league_new_year_block = LeagueNewYearBlock()
    league_end_block = LeagueEndBlock()


# TODO: Create a streamblock for the timeline w/ a few types of blocks: leg block, champs block
# Each block needs a date, host/venue, clubs attending
# Handle the case when a leg is split across different weekends
class SchedulePage(Page):
    parent_page_types = ['home.HomePage']

    page_title = models.TextField(blank=False)
    page_description = RichTextField(blank=False)

    timeline = StreamField(TimelineStreamBlock)

    content_panels = Page.content_panels + [
        FieldPanel('page_title', help_text="This is the title that is shown at the top of the page"),
        FieldPanel('page_description', help_text="The description text for this web page"),
        StreamFieldPanel('timeline', help_text="The B.U.T.T.S. League schedule timeline for the coming year")
    ]


class HomePage(Page):
    subpage_types = ['home.SchedulePage']

    description = models.TextField(max_length=400, default='')

    @property
    def posts(self):
        return BlogPage.objects.live().order_by('-first_published_at')[:5]

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]
