# Generated by Django 4.2 on 2023-04-25 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readers_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineRetailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('about', models.CharField(max_length=150)),
                ('website', models.URLField(max_length=100)),
            ],
        ),
    ]
