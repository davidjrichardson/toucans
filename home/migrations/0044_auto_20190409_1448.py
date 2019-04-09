# Generated by Django 2.1.7 on 2019-04-09 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0043_badgespage_leaguebadgeroundentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badgespage',
            name='body',
        ),
        migrations.RemoveField(
            model_name='badgespage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='badgespage',
            name='page_title',
        ),
        migrations.AddField(
            model_name='badgespage',
            name='genericpage_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.GenericPage'),
            preserve_default=False,
        ),
    ]
