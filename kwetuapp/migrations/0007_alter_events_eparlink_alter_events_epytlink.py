# Generated by Django 4.1.5 on 2023-02-09 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuapp', '0006_events_eparlink_events_epytlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='eparlink',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='events',
            name='epytlink',
            field=models.CharField(max_length=255),
        ),
    ]
