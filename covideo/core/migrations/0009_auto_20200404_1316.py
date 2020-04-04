# Generated by Django 2.2.11 on 2020-04-04 17:16

from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    Video = apps.get_model('core', 'Video')
    for row in Video.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_video_uuid'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]