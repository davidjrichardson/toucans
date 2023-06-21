# Generated by Django 3.2.15 on 2023-06-15 16:47

from django.db import migrations
import home.models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0052_auto_20220920_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulepage',
            name='timeline',
            field=wagtail.core.fields.StreamField([('season_start_block', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateBlock(help_text='The start date of the TOUCAN League for the year', required=True)), ('season_name', wagtail.core.blocks.TextBlock(help_text='The name of this season e.g.: TOUCAN 2018-19', required=True))])), ('league_leg_block', home.models.LeagueCombinedLegBlock(wagtail.core.blocks.StructBlock([('leg_name', wagtail.core.blocks.TextBlock(help_text='The name of this leg e.g.: "TOUCAN Leg 2 (Oxford)"', required=True)), ('leg_host', wagtail.core.blocks.TextBlock(help_text='The host club of this TOUCAN Leg', required=True)), ('leg_date', wagtail.core.blocks.DateBlock(help_text='The date of this TOUCAN Leg', required=True)), ('leg_attendees', wagtail.core.blocks.TextBlock(help_text='The clubs attending this TOUCAN Leg, separated by a comma', required=True))]))), ('league_event_block', wagtail.core.blocks.StructBlock([('leg_name', wagtail.core.blocks.TextBlock(help_text='The name of this leg e.g.: "TOUCAN Leg 2 (Oxford)"', required=True)), ('leg_host', wagtail.core.blocks.TextBlock(help_text='The host club of this TOUCAN Leg', required=True)), ('leg_date', wagtail.core.blocks.DateBlock(help_text='The date of this TOUCAN Leg', required=True)), ('leg_attendees', wagtail.core.blocks.TextBlock(help_text='The clubs attending this TOUCAN Leg, separated by a comma', required=True))])), ('league_champs_block', wagtail.core.blocks.StructBlock([('champs_name', wagtail.core.blocks.TextBlock(help_text='The name of this championship e.g.: "TOUCAN Field Champs"', required=True)), ('champs_venue', wagtail.core.blocks.TextBlock(help_text='The host club of this championship event', required=True)), ('champs_date', wagtail.core.blocks.DateBlock(help_text='The date of this championship event', required=True)), ('champs_attendees', wagtail.core.blocks.TextBlock(help_text='The clubs attending this champs, separated by a comma', null=True, required=False))])), ('league_midseason_marker_block', wagtail.core.blocks.StructBlock([('marker_text', wagtail.core.blocks.CharBlock(help_text='The name of the thing you would like to mark', max_length=50, required=True))])), ('season_end_block', wagtail.core.blocks.StructBlock([('season_name', wagtail.core.blocks.TextBlock(help_text='The name of this season e.g.: TOUCAN 2018-19', required=True))]))]),
        ),
    ]