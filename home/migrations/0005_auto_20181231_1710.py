# Generated by Django 2.1.4 on 2018-12-31 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_schedulepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedulepage',
            name='menu_order',
        ),
        migrations.RemoveField(
            model_name='schedulepage',
            name='menu_title',
        ),
    ]
