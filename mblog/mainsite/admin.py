from django.contrib import admin
from .models import User,Profile,File,Plan
from mainsite import models


# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display=('name','email')

# admin.site.register(User,UserAdmin)



class ProfileAdmin(admin.ModelAdmin):
    list_display=('id','user_id','plan_id','dashboard','width','hight')
admin.site.register(models.Profile,ProfileAdmin)

class PlanAdmin(admin.ModelAdmin):
    list_display=('id','plan_name','is_active','created_at','last_time')
admin.site.register(models.Plan,PlanAdmin)

class Plan_TableAdmin(admin.ModelAdmin):
    list_display=('id','plan_id','table_name','permission_name','created_at')
admin.site.register(models.Plan_Table,Plan_TableAdmin)

class User_PlanAdmin(admin.ModelAdmin):
     list_display=('id','user_id','plan_id','permission_name','created_at')
admin.site.register(models.User_Plan,User_PlanAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display=('id','file_name','created_at','last_time')
admin.site.register(File, FileAdmin)

class Matlab_InfoAdmin(admin.ModelAdmin):
    list_display=('id','user_id','plan_id','function_name','created_at','last_time')
admin.site.register(models.Matlab_Info, Matlab_InfoAdmin)

class Paper_InfoAdmin(admin.ModelAdmin):
    list_display=('id','chinese_title','english_title','english_keyword')
admin.site.register(models.Papers, Paper_InfoAdmin)

# class DataAdmin(admin.ModelAdmin):
#     # list_display=('date_time','jt_g01_cosphi','jt_g01_dayava','jt_g01_freq','jt_g01_monthava','jt_g01_nomp','JT_G01_NROTOR','JT_G01_VANE','JT_G01_VWIND','JT_G01_GOPOS','JT_G01_Ambient_Temp','JT_G01_FrontBearing_Temp','JT_G01_NacelleAmbient_Temp','JT_G01_NacelleCB_Temp','JT_G01_Nacelle_Temp','JT_G01_RearBearing_Temp','JT_G01_Rotor_Temp','JT_G01_Stator_Temp','JT_G01_Tower_Temp','JT_G01_Transformer_Temp','jt_g01_i_l1','JT_G01_I_L2','JT_G01_I_L3','JT_G01_P','JT_G01_U_L1','JT_G01_U_L2','JT_G01_U_L3')
#     list_display = ('date_time', 'jt_g01_cosphi', 'jt_g01_dayava')
# admin.site.register(Data, DataAdmin)

# admin.site.register(models.Data)

# from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
# from .models import Person
#
# @admin.register(Person)
# class PersonAdmin(ImportExportModelAdmin):
#     list_display = ('name','number','date')