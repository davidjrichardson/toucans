# Generated by Django 2.2.5 on 2019-09-05 10:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('home', '0049_auto_20190905_0958'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LegacyStandingsEntry',
            new_name='FourLegStandingsEntry',
        ),
        migrations.RenameModel(
            old_name='LegacyStandingsPage',
            new_name='FourLegStandingsPage',
        ),
    ]
