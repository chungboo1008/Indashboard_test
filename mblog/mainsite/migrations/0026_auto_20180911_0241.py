# Generated by Django 2.0.7 on 2018-09-10 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0025_auto_20180828_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dashboard',
            field=models.TextField(default=''),
        ),
    ]