# Generated by Django 2.0.7 on 2019-11-07 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0068_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Data',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='plan_id',
            new_name='plan_tmp_id',
        ),
    ]