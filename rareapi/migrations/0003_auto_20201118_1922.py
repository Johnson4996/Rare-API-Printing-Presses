# Generated by Django 3.1.3 on 2020-11-18 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0002_auto_20201118_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rareuser',
            name='profile_image_url',
            field=models.ImageField(blank=True, upload_to='profile_image_url'),
        ),
    ]
