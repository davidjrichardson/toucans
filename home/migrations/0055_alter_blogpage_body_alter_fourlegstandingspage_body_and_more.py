# Generated by Django 4.1.9 on 2023-06-21 15:02

from django.db import migrations
import home.models
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0054_alter_blogpagetag_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('credit_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.TextBlock(help_text='Photo caption', required=False)), ('credit', wagtail.blocks.TextBlock(help_text='Image credit'))])), ('plain_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.TextBlock(help_text='Photo caption', required=False))])), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title')), ('attribution', wagtail.blocks.CharBlock())])), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), ('table', wagtail.contrib.table_block.blocks.TableBlock(table_options={'startCols': 4, 'startRows': 1}, template='blocks/table_block.html'))], use_json_field=True),
        ),
        migrations.AlterField(
            model_name='fourlegstandingspage',
            name='body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow'))], use_json_field=True),
        ),
        migrations.AlterField(
            model_name='genericpage',
            name='body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('credit_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.TextBlock(help_text='Photo caption', required=False)), ('credit', wagtail.blocks.TextBlock(help_text='Image credit'))])), ('plain_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.TextBlock(help_text='Photo caption', required=False))])), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title')), ('attribution', wagtail.blocks.CharBlock())])), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), ('table', wagtail.contrib.table_block.blocks.TableBlock(table_options={'startCols': 4, 'startRows': 1}, template='blocks/table_block.html'))], use_json_field=True),
        ),
        migrations.AlterField(
            model_name='resourcepage',
            name='body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('credit_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.TextBlock(help_text='Photo caption', required=False)), ('credit', wagtail.blocks.TextBlock(help_text='Image credit'))])), ('plain_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.TextBlock(help_text='Photo caption', required=False))])), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title')), ('attribution', wagtail.blocks.CharBlock())])), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), ('table', wagtail.contrib.table_block.blocks.TableBlock(table_options={'startCols': 4, 'startRows': 1}, template='blocks/table_block.html'))], use_json_field=True),
        ),
        migrations.AlterField(
            model_name='schedulepage',
            name='timeline',
            field=wagtail.fields.StreamField([('season_start_block', wagtail.blocks.StructBlock([('start_date', wagtail.blocks.DateBlock(help_text='The start date of the TOUCAN League for the year', required=True)), ('season_name', wagtail.blocks.TextBlock(help_text='The name of this season e.g.: TOUCAN 2018-19', required=True))])), ('league_leg_block', home.models.LeagueCombinedLegBlock(wagtail.blocks.StructBlock([('leg_name', wagtail.blocks.TextBlock(help_text='The name of this leg e.g.: "TOUCAN Leg 2 (Oxford)"', required=True)), ('leg_host', wagtail.blocks.TextBlock(help_text='The host club of this TOUCAN Leg', required=True)), ('leg_date', wagtail.blocks.DateBlock(help_text='The date of this TOUCAN Leg', required=True)), ('leg_attendees', wagtail.blocks.TextBlock(help_text='The clubs attending this TOUCAN Leg, separated by a comma', required=True))]))), ('league_event_block', wagtail.blocks.StructBlock([('leg_name', wagtail.blocks.TextBlock(help_text='The name of this leg e.g.: "TOUCAN Leg 2 (Oxford)"', required=True)), ('leg_host', wagtail.blocks.TextBlock(help_text='The host club of this TOUCAN Leg', required=True)), ('leg_date', wagtail.blocks.DateBlock(help_text='The date of this TOUCAN Leg', required=True)), ('leg_attendees', wagtail.blocks.TextBlock(help_text='The clubs attending this TOUCAN Leg, separated by a comma', required=True))])), ('league_champs_block', wagtail.blocks.StructBlock([('champs_name', wagtail.blocks.TextBlock(help_text='The name of this championship e.g.: "TOUCAN Field Champs"', required=True)), ('champs_venue', wagtail.blocks.TextBlock(help_text='The host club of this championship event', required=True)), ('champs_date', wagtail.blocks.DateBlock(help_text='The date of this championship event', required=True)), ('champs_attendees', wagtail.blocks.TextBlock(help_text='The clubs attending this champs, separated by a comma', null=True, required=False))])), ('league_midseason_marker_block', wagtail.blocks.StructBlock([('marker_text', wagtail.blocks.CharBlock(help_text='The name of the thing you would like to mark', max_length=50, required=True))])), ('season_end_block', wagtail.blocks.StructBlock([('season_name', wagtail.blocks.TextBlock(help_text='The name of this season e.g.: TOUCAN 2018-19', required=True))]))], use_json_field=True),
        ),
        migrations.AlterField(
            model_name='threelegstandingspage',
            name='body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow'))], use_json_field=True),
        ),
    ]