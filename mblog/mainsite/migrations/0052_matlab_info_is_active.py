# Generated by Django 2.0.7 on 2019-10-10 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0051_matlab_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='matlab_info',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]