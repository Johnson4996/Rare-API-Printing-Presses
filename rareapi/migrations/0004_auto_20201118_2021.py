# Generated by Django 3.1.3 on 2020-11-18 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0003_auto_20201118_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rareuser',
            name='profile_image_url',
            field=models.ImageField(null=True, upload_to='profile_image_url'),
        ),
    ]