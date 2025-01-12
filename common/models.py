from dataclasses import dataclass
import json
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    FieldRowPanel,
    InlinePanel,
    HelpPanel,
)
from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    RichTextBlock,
)
from wagtail.fields import StreamField
from common.fields import ArcheryLegResultField


class StandingsStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    paragraph = RichTextBlock(icon="pilcrow")


@dataclass
class ThreeLegStanding:
    team_name: str
    leg_1: tuple[int, int, int]
    leg_2: tuple[int, int, int]
    leg_3: tuple[int, int, int]
    champs: tuple[int, int, int]

    @property
    def is_empty(self) -> bool:
        return (
            self.leg_1 == (0, 0, 0)
            and self.leg_2 == (0, 0, 0)
            and self.leg_3 == (0, 0, 0)
            and self.champs == (0, 0, 0)
        )

    @property
    def results(self) -> list[tuple[int, int, int]]:
        return [self.leg_1, self.leg_2, self.leg_3, self.champs]

    def __str__(self) -> str:
        return (
            f"{self.team_name}: {self.leg_1}, {self.leg_2}, {self.leg_3}, {self.champs}"
        )


def leg_results_field_default():
    return (0, 0, 0)


def leg_results_field_to_tuple(value: str) -> tuple[int, int, int]:
    parsed_dict = json.loads(value)
    return parsed_dict["score"], parsed_dict["hits"], parsed_dict["golds"]


class AbstractThreeLegStandingsEntry(models.Model):
    team_name = models.CharField(max_length=50)

    exp_leg_1 = ArcheryLegResultField(default=leg_results_field_default)
    exp_leg_2 = ArcheryLegResultField(default=leg_results_field_default)
    exp_leg_3 = ArcheryLegResultField(default=leg_results_field_default)
    exp_champs = ArcheryLegResultField(default=leg_results_field_default)

    nov_leg_1 = ArcheryLegResultField(default=leg_results_field_default)
    nov_leg_2 = ArcheryLegResultField(default=leg_results_field_default)
    nov_leg_3 = ArcheryLegResultField(default=leg_results_field_default)
    nov_champs = ArcheryLegResultField(default=leg_results_field_default)

    panels = [
        FieldPanel("team_name", classname="title"),
        FieldRowPanel(
            [
                FieldPanel(
                    "exp_leg_1", classname="col6", heading="Experienced results"
                ),
                FieldPanel("nov_leg_1", classname="col6", heading="Novice results"),
            ],
            heading="Leg 1",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "exp_leg_2", classname="col6", heading="Experienced results"
                ),
                FieldPanel("nov_leg_2", classname="col6", heading="Novice results"),
            ],
            heading="Leg 2",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "exp_leg_3", classname="col6", heading="Experienced results"
                ),
                FieldPanel("nov_leg_3", classname="col6", heading="Novice results"),
            ],
            heading="Leg 3",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "exp_champs", classname="col6", heading="Experienced results"
                ),
                FieldPanel("nov_champs", classname="col6", heading="Novice results"),
            ],
            heading="Champs",
        ),
    ]

    @property
    def novice_results(self) -> ThreeLegStanding:
        return ThreeLegStanding(
            team_name=self.team_name,
            leg_1=leg_results_field_to_tuple(self.nov_leg_1),
            leg_2=leg_results_field_to_tuple(self.nov_leg_2),
            leg_3=leg_results_field_to_tuple(self.nov_leg_3),
            champs=leg_results_field_to_tuple(self.nov_champs),
        )

    @property
    def experienced_results(self) -> ThreeLegStanding:
        return ThreeLegStanding(
            team_name=self.team_name,
            leg_1=leg_results_field_to_tuple(self.exp_leg_1),
            leg_2=leg_results_field_to_tuple(self.exp_leg_2),
            leg_3=leg_results_field_to_tuple(self.exp_leg_3),
            champs=leg_results_field_to_tuple(self.exp_champs),
        )

    class Meta:
        abstract = True


class AbstractLeagueResultsPage(Page):
    parent_page_types = ["home.StandingsIndexPage"]
    subpage_types = []

    standings_year = models.TextField(
        "Academic year",
        help_text="The academic year for this set of standings",
        null=True,
        blank=True,
    )
    start_date = models.DateField(
        "Start date", help_text="The start date of the league"
    )
    end_date = models.DateField(
        "End date",
        help_text="The end date of the league. Can be approximate if it is not totally certain.",
    )
    body = StreamField(StandingsStreamBlock)

    base_content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("standings_year"),
                FieldRowPanel(
                    [
                        FieldPanel("start_date", classname="col6"),
                        FieldPanel("end_date", classname="col6"),
                    ]
                ),
                FieldPanel("body"),
            ],
            heading="Standings information",
        ),
    ]

    class Meta:
        abstract = True


class AbstractLegacyLeagueResultsPage(AbstractLeagueResultsPage):
    content_panels = (
        Page.content_panels
        + [
            HelpPanel(
                '<h1 class="title"><strong>This page uses the old data entry format for league standings. Please use the new 3-leg entry format.</h1>'
            ),
        ]
        + AbstractLeagueResultsPage.base_content_panels
        + [
            InlinePanel("results", label="Results", classname="collapsed"),
        ]
    )

    class Meta:
        abstract = True


class AbstractMultiDivisionLeagueResultsPage(AbstractLeagueResultsPage):
    content_panels = (
        Page.content_panels
        + AbstractLeagueResultsPage.base_content_panels
        + [
            InlinePanel("div1_results", label="Division 1 results"),
            InlinePanel("div2_results", label="Division 2 results"),
        ]
    )

    class Meta:
        abstract = True


# @register_snippet
# class AcademicYear(models.Model):
#     year = models.CharField(max_length=9, unique=True)

#     panels = [
#         FieldPanel('year'),
#     ]

#     def __str__(self):
#         return self.year

#     class Meta:
#         verbose_name = 'Academic year'
#         verbose_name_plural = 'Academic years'
#         ordering = ['year']


# @register_snippet
# class Division(models.Model):
#     division_name = models.CharField(max_length=9)
#     academic_year = models.ForeignKey(
#         'AcademicYear',
#         on_delete=models.CASCADE,
#         related_name='divisions'
#     )
#     num_legs = models.IntegerField(default=3)

#     panels = [
#         FieldPanel('academic_year'),
#         FieldPanel('division_name'),
#         FieldPanel('num_legs'),
#     ]

#     def __str__(self):
#         return f'{self.academic_year} {self.division_name} ({self.num_legs} leg{"" if self.num_legs == 1 else "s"})'

#     class Meta:
#         verbose_name = 'Division'
#         verbose_name_plural = 'Divisions'
#         ordering = ['academic_year', 'division_name', 'num_legs']
