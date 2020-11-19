# Generated by Django 3.1.3 on 2020-11-19 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0004_auto_20201118_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postreactions',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postreactions', to='rareapi.posts'),
        ),
        migrations.AlterField(
            model_name='postreactions',
            name='reaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postreactions', to='rareapi.reaction'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='image_url',
            field=models.ImageField(null=True, upload_to='profile_image_url'),
        ),
    ]