# Generated by Django 2.0.7 on 2018-08-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0007_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolClass', models.CharField(max_length=20)),
                ('className', models.CharField(max_length=20)),
                ('schoolClassChinese', models.CharField(max_length=20)),
                ('seatNumber', models.CharField(max_length=20)),
                ('studentID', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('identityCard', models.CharField(max_length=30)),
                ('sex', models.CharField(max_length=2)),
                ('birth_date', models.CharField(max_length=20)),
            ],
        ),
    ]
