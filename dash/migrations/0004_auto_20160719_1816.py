# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 18:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0003_auto_20160714_2022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='first_name',
            new_name='first',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='last_name',
            new_name='last',
        ),
    ]