# Generated by Django 2.1.7 on 2019-03-07 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20190306_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standingsentry',
            old_name='leg_5_golds',
            new_name='champs_golds',
        ),
        migrations.RenameField(
            model_name='standingsentry',
            old_name='leg_5_hits',
            new_name='champs_hits',
        ),
        migrations.RenameField(
            model_name='standingsentry',
            old_name='leg_5_score',
            new_name='champs_score',
        ),
    ]
