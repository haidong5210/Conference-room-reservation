# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boardroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='会议室名')),
            ],
        ),
        migrations.CreateModel(
            name='Boardroom2Time2user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_time', models.IntegerField(choices=[(1, '8:00'), (2, '9:00'), (3, '10:00'), (4, '11:00'), (5, '12:00'), (6, '14:00'), (7, '15:00'), (8, '16:00'), (9, '17:00'), (10, '18:00'), (11, '19:00')], verbose_name='会议当天时间')),
                ('time', models.DateField(verbose_name='会议日期')),
                ('boardroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Boardroom', verbose_name='会议室')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
            ],
        ),
        migrations.AddField(
            model_name='boardroom2time2user',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.User'),
        ),
    ]
