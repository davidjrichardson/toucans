# Generated by Django 2.1.7 on 2019-03-10 13:29

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20190307_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='standingsindexpage',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
