# Generated by Django 2.1.7 on 2019-03-12 14:57

from django.db import migrations
import home.models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0036_resourcepage_page_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedulepage",
            name="timeline",
            field=wagtail.fields.StreamField(
                [
                    (
                        "season_start_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "start_date",
                                    wagtail.blocks.DateBlock(
                                        help_text="The start date of the B.U.T.T.S. League for the year",
                                        required=True,
                                    ),
                                ),
                                (
                                    "season_name",
                                    wagtail.blocks.TextBlock(
                                        help_text="The name of this season e.g.: Indoor, Outdoor",
                                        required=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "league_leg_block",
                        home.models.LeagueCombinedLegBlock(
                            wagtail.blocks.StructBlock(
                                [
                                    (
                                        "leg_name",
                                        wagtail.blocks.TextBlock(
                                            help_text='The name of this leg e.g.: "B.U.T.T.S. Leg 2 (Oxford)"',
                                            required=True,
                                        ),
                                    ),
                                    (
                                        "leg_host",
                                        wagtail.blocks.TextBlock(
                                            help_text="The host club of this B.U.T.T.S. Leg",
                                            required=True,
                                        ),
                                    ),
                                    (
                                        "leg_date",
                                        wagtail.blocks.DateBlock(
                                            help_text="The date of this B.U.T.T.S. Leg",
                                            required=True,
                                        ),
                                    ),
                                    (
                                        "leg_attendees",
                                        wagtail.blocks.TextBlock(
                                            help_text="The clubs attending this B.U.T.T.S. Leg, separated by a comma",
                                            required=True,
                                        ),
                                    ),
                                ]
                            )
                        ),
                    ),
                    (
                        "league_event_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "leg_name",
                                    wagtail.blocks.TextBlock(
                                        help_text='The name of this leg e.g.: "B.U.T.T.S. Leg 2 (Oxford)"',
                                        required=True,
                                    ),
                                ),
                                (
                                    "leg_host",
                                    wagtail.blocks.TextBlock(
                                        help_text="The host club of this B.U.T.T.S. Leg",
                                        required=True,
                                    ),
                                ),
                                (
                                    "leg_date",
                                    wagtail.blocks.DateBlock(
                                        help_text="The date of this B.U.T.T.S. Leg",
                                        required=True,
                                    ),
                                ),
                                (
                                    "leg_attendees",
                                    wagtail.blocks.TextBlock(
                                        help_text="The clubs attending this B.U.T.T.S. Leg, separated by a comma",
                                        required=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "league_champs_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "champs_name",
                                    wagtail.blocks.TextBlock(
                                        help_text='The name of this championship e.g.: "B.U.T.T.S. Field Champs"',
                                        required=True,
                                    ),
                                ),
                                (
                                    "champs_venue",
                                    wagtail.blocks.TextBlock(
                                        help_text="The host club of this championship event",
                                        required=True,
                                    ),
                                ),
                                (
                                    "champs_date",
                                    wagtail.blocks.DateBlock(
                                        help_text="The date of this championship event",
                                        required=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "league_new_year_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "marker_text",
                                    wagtail.blocks.CharBlock(
                                        help_text="The name of the thing you would like to mark",
                                        min_length=50,
                                        required=True,
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "season_end_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "season_name",
                                    wagtail.blocks.TextBlock(
                                        help_text="The name of this season e.g.: B.U.T.T.S. 2018-19",
                                        required=True,
                                    ),
                                )
                            ]
                        ),
                    ),
                ]
            ),
        ),
    ]
