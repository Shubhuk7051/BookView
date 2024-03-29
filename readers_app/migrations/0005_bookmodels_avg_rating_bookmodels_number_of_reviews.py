# Generated by Django 4.2 on 2023-04-27 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readers_app', '0004_reviewmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodels',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='bookmodels',
            name='number_of_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
