from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from collections import namedtuple
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from postgres_copy import CopyManager
# Create your models here.



class Plan(models.Model):
    plan_name = models.CharField(max_length = 128,null = False, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "plan"

class User_Plan(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length = 128,default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_plan"

class Plan_Table(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    table_name = models.CharField(max_length = 128, default='')
    alias_table_name = models.CharField(max_length = 128, default='')
    permission_name = models.CharField(max_length = 128,default='',blank=True)
    columns = JSONField(null=True,default=[{}],blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        db_table = "plan_table"


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=20,null=True,default='')
    dashboard = JSONField(db_index=True,null=False,default=[{}])
    width = models.IntegerField(default=6)
    hight = models.IntegerField(default=3)

    class Meta:
        db_table = "profile"



def fun_raw_sql_query(**kwargs):
    plan_id = kwargs.get('plan_id')
    if plan_id:
        result = Profile.objects.raw('SELECT * FROM profile WHERE plan_id = %s', [plan_id])
    else:
        result = Profile.objects.raw('SELECT * FROM profile')
    return result

def sql_query(**kwargs):
    plan_id = kwargs.get('plan_id')
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM profile WHERE plan_id = %s', [plan_id])
        result = namedtuplefetchall(cursor)
    result = [
        {
            "dashboard": r.dashboard,
            "plan_id": r.plan_id,
            "hight": r.hight,
            "width": r.width,
        }
        for r in result
    ]

    return result




def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


@csrf_exempt
def fun_sql_cursor_update_hw(**kwargs):
    dashboard = kwargs.get('dashboard')
    plan_id=kwargs.get('plan_id')
    hight=kwargs.get('hight')
    width=kwargs.get('width')
    pk = kwargs.get('pk')
    #dashboard='[{"type": "text", "text": "第一行的文字", "size": "3em", "slotW": 1, "slotH": 1}]'
    '''
    Note that if you want to include literal percent signs in the query,
    you have to double them in the case you are passing parameters:
    '''

    with connection.cursor() as cursor:
            cursor.execute("UPDATE profile SET  dashboard=%s,hight=%s,width=%s WHERE plan_id = %s ", [dashboard,hight,width,plan_id])
            cursor.execute("SELECT * FROM profile WHERE id = %s", [pk])
            #result = cursor.fetchone()
            result = namedtuplefetchall(cursor)
    result = [
            {
                "dashboard":r.dashboard,
                "plan_id":r.plan_id,
                "hight":r.hight,
                "width":r.width,
            }
            for r in result
    ]

    return result


@csrf_exempt
def fun_sql_cursor_update(**kwargs):
    dashboard = kwargs.get('dashboard')
    plan_id=kwargs.get('plan_id')

    pk = kwargs.get('pk')
    #dashboard='[{"type": "text", "text": "第一行的文字", "size": "3em", "slotW": 1, "slotH": 1}]'
    '''
    Note that if you want to include literal percent signs in the query,
    you have to double them in the case you are passing parameters:
    '''

    with connection.cursor() as cursor:
            cursor.execute("UPDATE profile SET  dashboard=%s WHERE plan_id = %s ", [dashboard,plan_id])
            cursor.execute("SELECT * FROM profile WHERE id = %s", [pk])
            #result = cursor.fetchone()
            result = namedtuplefetchall(cursor)
    result = [
            {
                "dashboard":r.dashboard,
                "plan_id":r.plan_id,
            }
            for r in result
    ]

    return result


class File(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default="")
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE,default="")
    file_path = models.CharField(max_length=256,null=True)
    file_name = models.CharField(max_length=256, null=True)
    doc_path = models.CharField(max_length=256,null=True)
    doc_name = models.CharField(max_length=256,null=True)
    outputfile1 = models.CharField(max_length=256,null=True)
    outputfile2 = models.CharField(max_length=256,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=True)
    permission_name = models.CharField(max_length=512, null=True)
    file_description = models.TextField(blank=True,null=True)
    

    class Meta:
        db_table = "file"

class Matlab_Info(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default="")
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE,default="")
    url = models.CharField(max_length=256,null=True)
    port = models.CharField(max_length=256, null=True)
    deployable_archive = models.CharField(max_length=256, null=True)
    parameters = models.CharField(max_length=256, null=True)
    function_name = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=True)
    permission_name = models.CharField(max_length=512, null=True)
    program_description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "matlab_info"

class Papers(models.Model):
    chinese_title = models.CharField(max_length=512,null=True)
    english_title = models.CharField(max_length=512,null=True)
    chinese_keyword = models.CharField(max_length=512,null=True)
    english_keyword = models.CharField(max_length=512,null=True)
    paper_year = models.CharField(max_length=512,null=True)
    link = models.CharField(max_length=512,null=True)
    abstract = models.TextField(blank=True,null=True)

    class Meta:
        db_table = "papers"

class Devices(models.Model):
    chinese_title = models.CharField(max_length=512,null=True)
    device_name = models.CharField(max_length=512,null=True)
    problem = models.TextField(blank=True,null=True)
    methods = models.CharField(max_length=512,null=True)
    result = models.TextField(blank=True,null=True)
    paper_year = models.CharField(max_length=512,null=True)

    class Meta:
        db_table = "devices"
    


class Data(models.Model):
    date_time = models.DateTimeField(null=True)
    jt_g01_cosphi = models.CharField(max_length=30,null=True)
    jt_g01_dayava = models.CharField(max_length=30,null=True)
    jt_g01_freq = models.CharField(max_length=30,null=True)
    jt_g01_monthava = models.CharField(max_length=30,null=True)
    jt_g01_nomp = models.CharField(max_length=30,null=True)
    jt_g01_nrotor = models.CharField(max_length=30,null=True)
    jt_g01_vane = models.CharField(max_length=30,null=True)
    jt_g01_vwind = models.CharField(max_length=30,null=True)
    jt_g01_gopos = models.CharField(max_length=30,null=True)
    jt_g01_ambient_temp = models.CharField(max_length=30,null=True)
    jt_g01_frontbearing_temp = models.CharField(max_length=30,null=True)
    jt_g01_nacelleambient_temp = models.CharField(max_length=30,null=True)
    jt_g01_nacellecb_temp= models.CharField(max_length=30,null=True)
    jt_g01_nacelle_temp = models.CharField(max_length=30,null=True)
    jt_g01_rearbearing_temp= models.CharField(max_length=30,null=True)
    jt_g01_rotor_temp = models.CharField(max_length=30,null=True)
    jt_g01_stator_temp = models.CharField(max_length=30,null=True)
    jt_g01_tower_temp = models.CharField(max_length=30,null=True)
    jt_g01_transformer_temp =models.CharField(max_length=30,null=True)
    jt_g01_i_l1 = models.CharField(max_length=30,null=True)
    jt_g01_i_l2 = models.CharField(max_length=30,null=True)
    jt_g01_i_l3 = models.CharField(max_length=30,null=True)
    jt_g01_p = models.CharField(max_length=30,null=True)
    jt_g01_u_l1 = models.CharField(max_length=30,null=True)
    jt_g01_u_l2 = models.CharField(max_length=30,null=True)
    jt_g01_u_l3  = models.CharField(max_length=30,null=True)
    objects = CopyManager()
