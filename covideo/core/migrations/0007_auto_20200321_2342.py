# Generated by Django 2.2.11 on 2020-03-21 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_video_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]