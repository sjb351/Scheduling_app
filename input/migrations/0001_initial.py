# Generated by Django 4.1.3 on 2022-11-29 20:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='procces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.DurationField(default=datetime.timedelta(0))),
                ('automated', models.BooleanField(default=False)),
                ('WorkerSetUpTime', models.DurationField(blank=True, default=datetime.timedelta(0), null=True)),
                ('WorkerpostProcessTime', models.DurationField(blank=True, default=datetime.timedelta(0), null=True)),
                ('rankOrder', models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iDnumber', models.PositiveBigIntegerField(default=0)),
                ('useable', models.BooleanField(default=True)),
                ('numberParral', models.PositiveBigIntegerField(default=1)),
                ('proccessTrainedFor', models.ManyToManyField(blank=True, to='input.procces')),
            ],
        ),
        migrations.CreateModel(
            name='proccessesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='input.product')),
            ],
        ),
        migrations.AddField(
            model_name='procces',
            name='proccessesLis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='input.proccesseslist'),
        ),
        migrations.CreateModel(
            name='machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iDnumber', models.PositiveBigIntegerField(default=0)),
                ('useable', models.BooleanField(default=True)),
                ('degredation', models.PositiveIntegerField(default=0)),
                ('numberParral', models.PositiveBigIntegerField(default=1)),
                ('proccessFor', models.ManyToManyField(blank=True, to='input.procces')),
            ],
        ),
    ]
