# Generated by Django 2.2.5 on 2019-09-05 09:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0046_auto_20190905_0939"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="StandingsEntry",
            new_name="LegacyStandingsEntry",
        ),
    ]
