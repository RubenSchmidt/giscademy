# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-16 13:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_course_lessons_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='lessons_completed',
        ),
    ]
