# Generated by Django 2.0.7 on 2018-08-12 07:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0008_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dashboard',
            field=django.contrib.postgres.fields.jsonb.JSONField(db_index=True, null=True),
        ),
    ]
