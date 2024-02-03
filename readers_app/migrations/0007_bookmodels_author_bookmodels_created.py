# Generated by Django 4.2 on 2023-05-03 08:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('readers_app', '0006_alter_bookmodels_retailer'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodels',
            name='author',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookmodels',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
