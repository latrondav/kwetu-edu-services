# Generated by Django 4.1.5 on 2023-02-09 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuapp', '0007_alter_events_eparlink_alter_events_epytlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='eparlink',
            field=models.FileField(default='eaudios.mp3', upload_to='Event Audios'),
        ),
    ]