# Generated by Django 2.2.5 on 2019-09-05 09:54

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
        ("home", "0047_auto_20190905_0946"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewStandingsPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "standings_year",
                    models.TextField(
                        help_text="The academic year for this set of standings",
                        verbose_name="Academic year",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "h2",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            (
                                "h3",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            (
                                "h4",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="NewStandingsEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("team_name", models.CharField(max_length=50)),
                ("team_is_novice", models.BooleanField(default=False)),
                ("leg_1_score", models.IntegerField(blank=True, default=0)),
                ("leg_1_hits", models.IntegerField(blank=True, default=0)),
                ("leg_1_golds", models.IntegerField(blank=True, default=0)),
                ("leg_2_score", models.IntegerField(blank=True, default=0)),
                ("leg_2_hits", models.IntegerField(blank=True, default=0)),
                ("leg_2_golds", models.IntegerField(blank=True, default=0)),
                ("leg_3_score", models.IntegerField(blank=True, default=0)),
                ("leg_3_hits", models.IntegerField(blank=True, default=0)),
                ("leg_3_golds", models.IntegerField(blank=True, default=0)),
                ("champs_score", models.IntegerField(blank=True, default=0)),
                ("champs_hits", models.IntegerField(blank=True, default=0)),
                ("champs_golds", models.IntegerField(blank=True, default=0)),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="home.NewStandingsPage",
                    ),
                ),
            ],
        ),
    ]
