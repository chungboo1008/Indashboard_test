# Generated by Django 2.0.7 on 2019-11-07 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0067_devices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(null=True)),
                ('jt_g01_cosphi', models.CharField(max_length=30, null=True)),
                ('jt_g01_dayava', models.CharField(max_length=30, null=True)),
                ('jt_g01_freq', models.CharField(max_length=30, null=True)),
                ('jt_g01_monthava', models.CharField(max_length=30, null=True)),
                ('jt_g01_nomp', models.CharField(max_length=30, null=True)),
                ('jt_g01_nrotor', models.CharField(max_length=30, null=True)),
                ('jt_g01_vane', models.CharField(max_length=30, null=True)),
                ('jt_g01_vwind', models.CharField(max_length=30, null=True)),
                ('jt_g01_gopos', models.CharField(max_length=30, null=True)),
                ('jt_g01_ambient_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_frontbearing_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_nacelleambient_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_nacellecb_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_nacelle_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_rearbearing_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_rotor_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_stator_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_tower_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_transformer_temp', models.CharField(max_length=30, null=True)),
                ('jt_g01_i_l1', models.CharField(max_length=30, null=True)),
                ('jt_g01_i_l2', models.CharField(max_length=30, null=True)),
                ('jt_g01_i_l3', models.CharField(max_length=30, null=True)),
                ('jt_g01_p', models.CharField(max_length=30, null=True)),
                ('jt_g01_u_l1', models.CharField(max_length=30, null=True)),
                ('jt_g01_u_l2', models.CharField(max_length=30, null=True)),
                ('jt_g01_u_l3', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
