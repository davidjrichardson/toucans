# Generated by Django 4.2.14 on 2024-08-07 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0093_uploadedfile'),
        ('home', '0055_alter_blogpage_body_alter_fourlegstandingspage_body_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FourLegStandingsEntry',
            new_name='LegacyFourLegStandingsEntry',
        ),
        migrations.RenameModel(
            old_name='FourLegStandingsPage',
            new_name='LegacyFourLegStandingsPage',
        ),
    ]
