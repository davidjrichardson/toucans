# Generated by Django 2.1.7 on 2019-03-06 13:52

from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0019_auto_20190306_1345"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standingspage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("h2", wagtail.blocks.CharBlock(classname="title", icon="title")),
                    ("h3", wagtail.blocks.CharBlock(classname="title", icon="title")),
                    ("h4", wagtail.blocks.CharBlock(classname="title", icon="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "table",
                        wagtail.contrib.table_block.blocks.TableBlock(
                            table_options={
                                "colHeaders": True,
                                "height": 324,
                                "rowHeaders": True,
                                "startCols": 6,
                                "startRows": 9,
                            },
                            template="blocks/league_results_block.html",
                        ),
                    ),
                ]
            ),
        ),
    ]
