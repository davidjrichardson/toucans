from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.blocks import StructBlock, DateBlock, CharBlock, TextBlock, StreamBlock, IntegerBlock, StaticBlock, \
    ListBlock, RichTextBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
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


class SeasonStartDateBlock(StructBlock):
    start_date = DateBlock(
        required=True,
        help_text="The start date of the B.U.T.T.S. League for the year"
    )
    season_name = TextBlock(
        required=True,
        help_text="The name of this season e.g.: Indoor, Outdoor"
    )

    class Meta:
        label = 'Season start date'
        icon = 'date'


class LeagueNewYearBlock(StructBlock):
    new_year = IntegerBlock(
        required=True,
        help_text="The new year for the league"
    )

    class Meta:
        label = 'New year marker'
        icon = 'date'


class SeasonEndBlock(StructBlock):
    season_name = TextBlock(
        required=True,
        help_text="The name of this season e.g.: Indoor, Outdoor"
    )

    class Meta:
        label = 'Season end marker'
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
        label = 'League event'
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
    season_start_block = SeasonStartDateBlock()
    league_leg_block = LeagueCombinedLegBlock(LeagueLegBlock())
    league_event_block = LeagueLegBlock()
    league_champs_block = LeagueChampsBlock()
    league_new_year_block = LeagueNewYearBlock()
    season_end_block = SeasonEndBlock()


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


class PullQuoteBlock(StructBlock):
    quote = TextBlock('quote title')
    attribution = CharBlock()

    class Meta:
        icon = 'openquote'


class CreditImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(help_text='Photo caption', required=False)
    credit = TextBlock(help_text='Image credit')

    class Meta:
        icon = 'image'


class PlainImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(help_text='Photo caption', required=False)

    class Meta:
        icon = 'image'


class BlogStreamBlock(StreamBlock):
    h2 = CharBlock(icon='title', classname='title')
    h3 = CharBlock(icon='title', classname='title')
    h4 = CharBlock(icon='title', classname='title')
    paragraph = RichTextBlock(icon='pilcrow')
    credit_image = CreditImageBlock()
    plain_image = PlainImageBlock()
    pullquote = PullQuoteBlock()
    document = DocumentChooserBlock(icon='doc-full-inverse')
    table = TableBlock(table_options={
        'startRows': 1,
        'startCols': 4,
    }, template='blocks/table_block.html')


class StandingsStreamBlock(StreamBlock):
    h2 = CharBlock(icon='title', classname='title')
    h3 = CharBlock(icon='title', classname='title')
    h4 = CharBlock(icon='title', classname='title')
    paragraph = RichTextBlock(icon='pilcrow')


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('home.BlogPage', related_name='tagged_items')


class BlogPage(Page):
    parent_page_types = ['home.BlogIndexPage']

    body = StreamField(BlogStreamBlock)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateTimeField('Post date', default=timezone.now)
    excerpt = RichTextField(help_text='This is displayed on the home and blog listing pages', default='')
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This is the image displayed on the home page as the first thing a user will see'
    )
    cover_image_credit = models.CharField(blank=True, max_length=100, default='')
    cover_invert_title = models.BooleanField(blank=True, default=False)

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="full title"),
            FieldPanel('excerpt'),
            FieldPanel('date'),
            StreamFieldPanel('body')
        ], heading='Post content'),
        MultiFieldPanel([
            ImageChooserPanel('cover_image'),
            FieldPanel('cover_image_credit'),
            FieldPanel('cover_invert_title', help_text='If the cover image is dark, tick this box')
        ], heading='Blog post cover image')
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    @property
    def further_reading(self):
        siblings = BlogPage.objects.live().sibling_of(self, inclusive=False).order_by('-date')

        if siblings:
            latest = siblings.first()
            next_article = siblings.filter(date__lte=self.date).exclude(id=latest.id).order_by('-date').first()
            if next_article:
                return [latest, next_article]
            else:
                return [latest]
        else:
            return []


class BlogIndexPage(Page):
    subpage_types = ['home.BlogPage']
    parent_page_types = ['home.HomePage']

    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page ordered by most recent
        return BlogPage.objects.live().descendant_of(self).order_by('-date')

    def get_context(self, request, *args, **kwargs):
        # Get blogs
        blogs = self.blogs

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)

        # Filter by date
        filter_date = request.GET.get('date')
        if filter_date:
            filter_date = datetime.strptime(filter_date, '%Y-%m')
            blogs = blogs.filter(date__month=filter_date.month, date__year=filter_date.year)

        # Pagination
        paginator = Paginator(blogs, 10)  # Show 10 blogs per page
        try:
            blogs = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        context['paginator'] = paginator

        return context


class StandingsIndexPage(Page):
    parent_page_types = ['home.StandingsPage']
    subpage_types = ['home.StandingsPage']

    @property
    def archives(self):
        return StandingsPage.objects.live().childof(self).order_by('-standings_year').all()


class StandingsEntry(models.Model):
    page = ParentalKey('StandingsPage', related_name='results')

    university = models.CharField(max_length=50)

    leg_1_score = models.IntegerField(blank=True, default=None, null=True)
    leg_1_hits = models.IntegerField(blank=True, default=None, null=True)
    leg_1_golds = models.IntegerField(blank=True, default=None, null=True)

    leg_2_score = models.IntegerField(blank=True, default=None, null=True)
    leg_2_hits = models.IntegerField(blank=True, default=None, null=True)
    leg_2_golds = models.IntegerField(blank=True, default=None, null=True)

    leg_3_score = models.IntegerField(blank=True, default=None, null=True)
    leg_3_hits = models.IntegerField(blank=True, default=None, null=True)
    leg_3_golds = models.IntegerField(blank=True, default=None, null=True)

    leg_4_score = models.IntegerField(blank=True, default=None, null=True)
    leg_4_hits = models.IntegerField(blank=True, default=None, null=True)
    leg_4_golds = models.IntegerField(blank=True, default=None, null=True)

    leg_5_score = models.IntegerField(blank=True, default=None, null=True)
    leg_5_hits = models.IntegerField(blank=True, default=None, null=True)
    leg_5_golds = models.IntegerField(blank=True, default=None, null=True)

    panels = [
        FieldPanel('university', classname='title'),
        FieldRowPanel([
            FieldPanel('leg_1_score'),
            FieldPanel('leg_1_hits'),
            FieldPanel('leg_1_golds'),
        ]),
        FieldRowPanel([
            FieldPanel('leg_2_score'),
            FieldPanel('leg_2_hits'),
            FieldPanel('leg_2_golds'),
        ]),
        FieldRowPanel([
            FieldPanel('leg_3_score'),
            FieldPanel('leg_3_hits'),
            FieldPanel('leg_3_golds'),
        ]),
        FieldRowPanel([
            FieldPanel('leg_4_score'),
            FieldPanel('leg_4_hits'),
            FieldPanel('leg_4_golds'),
        ]),
        FieldRowPanel([
            FieldPanel('leg_5_score'),
            FieldPanel('leg_5_hits'),
            FieldPanel('leg_5_golds'),
        ]),
    ]


class StandingsPage(Page):
    parent_page_types = ['home.HomePage', 'home.StandingsIndexPage']
    subpage_types = ['home.StandingsIndexPage']

    standings_year = models.TextField('Academic year',
                                      help_text='The academic year for this set of standings')
    body = StreamField(StandingsStreamBlock)
    # TODO: Create a nice way to do the table
    #   > Multiple unis, 5 legs (w/ champs)
    #   > Each leg has score/golds/hits

    @property
    def results_table(self):
        return self.results.all()

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('standings_year'),
            StreamFieldPanel('body'),
        ], heading='Standings Info'),
        InlinePanel('results', label='Results')
    ]


class HomePage(Page):
    subpage_types = ['home.SchedulePage', 'home.BlogIndexPage', 'home.StandingsPage']

    description = models.TextField(max_length=400, default='')

    @property
    def posts(self):
        return self.news_index.blogs[:5]

    @property
    def news_index(self):
        return BlogIndexPage.objects.live().child_of(self).first()

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]
