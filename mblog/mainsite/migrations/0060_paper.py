# Generated by Django 2.0.7 on 2019-11-07 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0059_delete_paper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chinese_title', models.CharField(max_length=256, null=True)),
                ('english_title', models.CharField(max_length=256, null=True)),
                ('chinese_keyword', models.CharField(max_length=256, null=True)),
                ('english_keyword', models.CharField(max_length=256, null=True)),
                ('paper_year', models.CharField(max_length=256, null=True)),
                ('link', models.CharField(max_length=256, null=True)),
                ('abstract', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'paper',
            },
        ),
    ]
