# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='update',
            new_name='updated',
        ),
    ]