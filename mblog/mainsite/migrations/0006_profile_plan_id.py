# Generated by Django 2.0.7 on 2018-08-08 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0005_auto_20180807_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plan_id',
            field=models.CharField(default='', max_length=20),
        ),
    ]
