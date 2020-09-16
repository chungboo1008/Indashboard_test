from rest_framework import serializers
from mainsite.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ('user', 'plan_id', 'dashboard')

# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=File
#         fields = ('file_field','remark', 'timestamp')



# class DataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Data
#         fields =('date_time','JT_G01_COSPHI','JT_G01_DAYAVA','JT_G01_FREQ','JT_G01_MONTHAVA','JT_G01_NOMP', 'JT_G01_NROTOR','JT_G01_VANE','JT_G01_VWIND','JT_G01_GOPOS','JT_G01_Ambient_Temp','JT_G01_FrontBearing_Temp','JT_G01_NacelleAmbient_Temp','JT_G01_NacelleCB_Temp','JT_G01_Nacelle_Temp','JT_G01_RearBearing_Temp','JT_G01_Rotor_Temp', 'JT_G01_Stator_Temp', 'JT_G01_Tower_Temp', 'JT_G01_Transformer_Temp', 'JT_G01_I_L1','JT_G01_I_L2', 'JT_G01_I_L3', 'JT_G01_P', 'JT_G01_U_L1','JT_G01_U_L2','JT_G01_U_L3')
