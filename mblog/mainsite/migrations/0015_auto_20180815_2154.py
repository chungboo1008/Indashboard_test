# Generated by Django 2.0.7 on 2018-08-15 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0014_auto_20180812_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='person',
            name='className',
        ),
        migrations.RemoveField(
            model_name='person',
            name='identityCard',
        ),
        migrations.RemoveField(
            model_name='person',
            name='schoolClass',
        ),
        migrations.RemoveField(
            model_name='person',
            name='schoolClassChinese',
        ),
        migrations.RemoveField(
            model_name='person',
            name='seatNumber',
        ),
        migrations.RemoveField(
            model_name='person',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='person',
            name='studentID',
        ),
        migrations.AddField(
            model_name='person',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]