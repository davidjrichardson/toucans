# Generated by Django 2.1.4 on 2018-12-31 21:15

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0005_auto_20181231_1710"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedulepage",
            name="page_description",
            field=wagtail.fields.RichTextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="schedulepage",
            name="page_title",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="schedulepage",
            name="timeline",
            field=wagtail.fields.StreamField(
                [
                    (
                        "league_leg_block",
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
                                        help_text="The host club or venue of this championship event",
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
                ],
                default=None,
            ),
            preserve_default=False,
        ),
    ]
