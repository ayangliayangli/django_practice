# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-07 09:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guanyin', '0002_auto_20161107_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hosts',
            field=models.ManyToManyField(blank=True, null=True, to='guanyin.Host'),
        ),
    ]