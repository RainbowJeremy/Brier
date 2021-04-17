# Generated by Django 3.1.3 on 2021-01-31 19:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0008_auto_20210131_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tracked_by',
        ),
        migrations.AddField(
            model_name='question',
            name='tracked_by',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
