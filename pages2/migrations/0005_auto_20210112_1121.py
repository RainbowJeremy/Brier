# Generated by Django 3.1.3 on 2021-01-12 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_question_forum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.forum'),
        ),
    ]
