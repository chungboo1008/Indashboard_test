# Generated by Django 2.0.7 on 2018-09-10 19:21

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0028_auto_20180911_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dashboard',
            field=django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default=''),
        ),
    ]
