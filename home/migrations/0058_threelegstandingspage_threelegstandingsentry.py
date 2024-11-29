# Generated by Django 4.2.14 on 2024-08-09 13:38

from django.db import migrations, models
import django.db.models.deletion
import common.fields
import modelcluster.fields
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0093_uploadedfile"),
        (
            "home",
            "0057_rename_threelegstandingsentry_legacythreelegstandingsentry_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ThreeLegStandingsPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
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
                                    form_classname="title", icon="title"
                                ),
                            ),
                            (
                                "h3",
                                wagtail.blocks.CharBlock(
                                    form_classname="title", icon="title"
                                ),
                            ),
                            (
                                "h4",
                                wagtail.blocks.CharBlock(
                                    form_classname="title", icon="title"
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
            name="ThreeLegStandingsEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("team_name", models.CharField(max_length=50)),
                (
                    "exp_leg_1",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "exp_leg_2",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "exp_leg_3",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "exp_champs",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "nov_leg_1",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "nov_leg_2",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "nov_leg_3",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "nov_champs",
                    common.fields.ArcheryLegResultField(
                        default=common.models.leg_results_field_default
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="home.threelegstandingspage",
                    ),
                ),
            ],
        ),
    ]
