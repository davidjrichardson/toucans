import functools
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.blocks import StructBlock, DateBlock, CharBlock, TextBlock, StreamBlock, IntegerBlock, ListBlock, \
    RichTextBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
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
        help_text="The name of this season e.g.: B.U.T.T.S. 2018-19"
    )

    class Meta:
        label = 'Start of academic year marker'
        icon = 'date'


class LeagueMidSeasonMarkerBlock(StructBlock):
    marker_text = CharBlock(
        max_length=50,
        required=True,
        help_text="The name of the thing you would like to mark"
    )

    class Meta:
        label = 'Mid-season marker'
        icon = 'date'


class SeasonEndBlock(StructBlock):
    season_name = TextBlock(
        required=True,
        help_text="The name of this season e.g.: B.U.T.T.S. 2018-19"
    )

    class Meta:
        label = 'End of year marker'
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
        label = 'Tournament leg'
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
    champs_attendees = TextBlock(
        required=False,
        null=True,
        help_text="The clubs attending this champs, separated by a comma"
    )

    class Meta:
        label = 'Champs'
        icon = 'pick'


class TimelineStreamBlock(StreamBlock):
    season_start_block = SeasonStartDateBlock()
    league_leg_block = LeagueCombinedLegBlock(LeagueLegBlock())
    league_event_block = LeagueLegBlock()
    league_champs_block = LeagueChampsBlock()
    league_midseason_marker_block = LeagueMidSeasonMarkerBlock()
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


class RelatedLink(models.Model):
    title = models.CharField(max_length=255)
    link_external = models.URLField("External link", blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('link_external'),
    ]

    class Meta:
        abstract = True


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('home.BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


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

    description = RichTextField(blank=True, null=True)

    @property
    def archives(self):
        return StandingsPage.objects.live().child_of(self).order_by('-standings_year').all()

    @property
    def resources(self):
        return filter(lambda x: x.depth > 3, ResourcePage.objects.live().all())

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]


class StandingsEntry(models.Model):
    page = ParentalKey('StandingsPage', related_name='results', on_delete=models.CASCADE)

    team_name = models.CharField(max_length=50)
    team_is_novice = models.BooleanField(default=False)

    leg_1_score = models.IntegerField(blank=True, default=0)
    leg_1_hits = models.IntegerField(blank=True, default=0)
    leg_1_golds = models.IntegerField(blank=True, default=0)

    leg_2_score = models.IntegerField(blank=True, default=0)
    leg_2_hits = models.IntegerField(blank=True, default=0)
    leg_2_golds = models.IntegerField(blank=True, default=0)

    leg_3_score = models.IntegerField(blank=True, default=0)
    leg_3_hits = models.IntegerField(blank=True, default=0)
    leg_3_golds = models.IntegerField(blank=True, default=0)

    leg_4_score = models.IntegerField(blank=True, default=0)
    leg_4_hits = models.IntegerField(blank=True, default=0)
    leg_4_golds = models.IntegerField(blank=True, default=0)

    champs_score = models.IntegerField(blank=True, default=0)
    champs_hits = models.IntegerField(blank=True, default=0)
    champs_golds = models.IntegerField(blank=True, default=0)

    @property
    def leg_1(self):
        return self.leg_1_score, self.leg_1_hits, self.leg_1_golds

    @property
    def leg_2(self):
        return self.leg_2_score, self.leg_2_hits, self.leg_2_golds

    @property
    def leg_3(self):
        return self.leg_3_score, self.leg_3_hits, self.leg_3_golds

    @property
    def leg_4(self):
        return self.leg_4_score, self.leg_4_hits, self.leg_4_golds

    @property
    def champs(self):
        return self.champs_score, self.champs_hits, self.champs_golds

    @property
    def results(self):
        return [self.leg_1, self.leg_2, self.leg_3, self.leg_4, self.champs]

    @property
    def is_empty(self):
        return not bool(list(filter(lambda x: x != (0, 0, 0), self.results)))

    @property
    def aggregate(self):
        return functools.reduce(lambda acc, new: (acc[0] + new[0], acc[1] + new[1], acc[2] + new[2]), self.results)

    panels = [
        FieldPanel('team_name', classname='title'),
        FieldPanel('team_is_novice'),
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
            FieldPanel('champs_score'),
            FieldPanel('champs_hits'),
            FieldPanel('champs_golds'),
        ]),
    ]


class StandingsPage(Page):
    parent_page_types = ['home.HomePage', 'home.StandingsIndexPage']
    subpage_types = ['home.StandingsIndexPage']

    standings_year = models.TextField('Academic year',
                                      help_text='The academic year for this set of standings')
    body = StreamField(StandingsStreamBlock)

    @property
    def experienced_results(self):
        return self.results.filter(team_is_novice=False).all()

    @property
    def novice_results(self):
        return self.results.filter(team_is_novice=True).all()

    @property
    def archives(self):
        return StandingsIndexPage.objects.live().child_of(self).first()

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('standings_year'),
            StreamFieldPanel('body'),
        ], heading='Standings Info'),
        InlinePanel('results', label='Results')
    ]


class ResourceRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.ResourcePage', on_delete=models.CASCADE, related_name='related_links')


class ResourcePage(Page):
    subpage_types = ['home.ResourcePage']
    parent_page_types = ['home.ResourcePage', 'home.HomePage']

    page_title = models.CharField(max_length=200, blank=True, null=True,
                                  help_text='Use this to override the title text in the web page itself, useful for '
                                            'keeping the menu title consistent')
    description = RichTextField(blank=True, null=True)
    body = StreamField(BlogStreamBlock)

    @property
    def child_resources(self):
        return ResourcePage.objects.live().child_of(self).all()

    @property
    def related(self):
        return self.related_links.all()

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="full title"),
            FieldPanel('page_title', classname="title"),
            FieldPanel('description'),
            StreamFieldPanel('body')
        ], heading='Page content'),
        InlinePanel('related_links', label='Related links')
    ]


class GenericRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.GenericPage', on_delete=models.CASCADE, related_name='related_links')


class GenericPage(Page):
    subpage_types = ['home.GenericPage', 'home.ResourcePage']
    parent_page_types = ['home.GenericPage', 'home.ResourcePage', 'home.HomePage']

    page_title = models.CharField(max_length=200, blank=True, null=True,
                                  help_text='Use this to override the title text in the web page itself, useful for '
                                            'keeping the menu title consistent')
    body = StreamField(BlogStreamBlock)

    @property
    def related(self):
        return self.related_links.all()

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="full title"),
            FieldPanel('page_title', classname="title"),
            StreamFieldPanel('body')
        ], heading='Page content'),
        InlinePanel('related_links', label='Related links')
    ]


class HomePage(Page):
    subpage_types = ['home.SchedulePage', 'home.BlogIndexPage', 'home.StandingsPage', 'home.ResourcePage',
                     'home.GenericPage']

    description = models.TextField(max_length=400, default='')

    @property
    def posts(self):
        return self.news_index.blogs[:5]

    @property
    def news_index(self):
        return BlogIndexPage.objects.live().child_of(self).first()

    @property
    def experienced_standings(self):
        return StandingsPage.objects.live().child_of(self).first().experienced_results

    @property
    def novice_standings(self):
        return StandingsPage.objects.live().child_of(self).first().novice_results

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]
