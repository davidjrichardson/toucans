# Generated by Django 2.1.7 on 2019-03-10 20:33

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
        ("home", "0030_standingsindexpage_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResourcePage",
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
                ("description", wagtail.fields.RichTextField(blank=True, null=True)),
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
                            (
                                "credit_image",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "caption",
                                            wagtail.blocks.TextBlock(
                                                help_text="Photo caption",
                                                required=False,
                                            ),
                                        ),
                                        (
                                            "credit",
                                            wagtail.blocks.TextBlock(
                                                help_text="Image credit"
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "plain_image",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "caption",
                                            wagtail.blocks.TextBlock(
                                                help_text="Photo caption",
                                                required=False,
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "pullquote",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "quote",
                                            wagtail.blocks.TextBlock("quote title"),
                                        ),
                                        ("attribution", wagtail.blocks.CharBlock()),
                                    ]
                                ),
                            ),
                            (
                                "document",
                                wagtail.documents.blocks.DocumentChooserBlock(
                                    icon="doc-full-inverse"
                                ),
                            ),
                            (
                                "table",
                                wagtail.contrib.table_block.blocks.TableBlock(
                                    table_options={"startCols": 4, "startRows": 1},
                                    template="blocks/table_block.html",
                                ),
                            ),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
