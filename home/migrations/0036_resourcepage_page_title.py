# Generated by Django 2.1.7 on 2019-03-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0035_genericpage_page_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="resourcepage",
            name="page_title",
            field=models.CharField(
                blank=True,
                help_text="Use this to override the title text in the web page itself, useful for keeping the menu title consistent",
                max_length=200,
                null=True,
            ),
        ),
    ]
