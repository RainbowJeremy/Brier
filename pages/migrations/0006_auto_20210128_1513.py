# Generated by Django 3.1.3 on 2021-01-28 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20210112_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estimate',
            old_name='score',
            new_name='evaluation',
        ),
    ]
