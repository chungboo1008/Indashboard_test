# Generated by Django 2.0.7 on 2018-08-12 10:12

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0012_auto_20180812_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dashboard',
            field=django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default='', null=True),
        ),
    ]
