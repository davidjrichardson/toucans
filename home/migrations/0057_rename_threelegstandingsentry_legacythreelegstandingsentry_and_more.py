# Generated by Django 4.2.14 on 2024-08-07 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0093_uploadedfile'),
        ('home', '0056_rename_fourlegstandingsentry_legacyfourlegstandingsentry_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ThreeLegStandingsEntry',
            new_name='LegacyThreeLegStandingsEntry',
        ),
        migrations.RenameModel(
            old_name='ThreeLegStandingsPage',
            new_name='LegacyThreeLegStandingsPage',
        ),
    ]