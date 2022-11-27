# Generated by Django 4.1.3 on 2022-11-16 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mqttData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobName', models.CharField(max_length=200)),
                ('createdTime', models.DateTimeField(auto_now_add=True)),
                ('startedTime', models.DateTimeField()),
                ('length', models.FloatField()),
            ],
        ),
    ]
