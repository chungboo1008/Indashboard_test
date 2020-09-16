# Generated by Django 2.0.7 on 2019-11-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0064_delete_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chinese_title', models.CharField(max_length=512, null=True)),
                ('device_name', models.CharField(max_length=512, null=True)),
                ('problem', models.TextField(blank=True, null=True)),
                ('methods', models.CharField(max_length=512, null=True)),
                ('result', models.TextField(blank=True, null=True)),
                ('paper_year', models.CharField(max_length=512, null=True)),
            ],
            options={
                'db_table': 'devices',
            },
        ),
    ]
