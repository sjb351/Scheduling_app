# Generated by Django 4.1.3 on 2022-12-03 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleView', '0002_order_endtime_order_startedtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='data',
            field=models.JSONField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
