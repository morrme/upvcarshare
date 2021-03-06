# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 14:58
from __future__ import unicode_literals

from django.db import migrations, models
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('journeys', '0009_auto_20160622_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='journey',
            name='arrival',
            field=models.DateTimeField(blank=True, null=True, verbose_name='fecha y hora de llegada estimada'),
        ),
        migrations.AlterField(
            model_name='journey',
            name='recurrence',
            field=recurrence.fields.RecurrenceField(blank=True, null=True, verbose_name='¿Vas a realizar este trayecto más de una vez?'),
        ),
    ]
