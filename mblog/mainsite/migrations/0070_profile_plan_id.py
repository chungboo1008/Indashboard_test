# Generated by Django 2.0.7 on 2019-11-07 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0069_auto_20191107_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plan_id',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='mainsite.Plan'),
        ),
    ]
