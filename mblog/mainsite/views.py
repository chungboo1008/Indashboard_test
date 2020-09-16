import sys
import subprocess
import psycopg2
import time
import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Profile,File
from  datetime import datetime
from  mainsite import form,models
from django.contrib import messages
# Another import
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import simplejson as json
from django.http import JsonResponse
from django.contrib.auth.models import User
from mainsite.serializers import ProfileSerializer #,DataSerializer
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from mainsite.models import fun_raw_sql_query,fun_sql_cursor_update,fun_sql_cursor_update_hw,sql_query
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.template import RequestContext
#from django.shortcuts import render_to_response just for django2
from rest_framework.views import APIView
from . import views
from rest_framework.parsers import MultiPartParser, FormParser ,FileUploadParser
import zipfile
import csv
## DB
from collections import namedtuple
from django.db import connection
from mainsite.models import namedtuplefetchall
import numpy as np
import xml.etree.ElementTree as ET
from collections import namedtuple
#opc
from opcua import Client
import time
import math
# threading
import threading
import time
import ipdb
# word2vec
from gensim.models import word2vec
from gensim import models
import logging
from pathlib import Path
import pandas as pd
# matlab
import http.client


@csrf_exempt
def save_data(request):
        if request.method == 'POST':
          json_data = json.loads(request.body)
          arr = json_data['arr']
          data={
              "arr": arr
          }
        return JsonResponse(data)

def query(request):
        if request.method == 'POST':
             json_data = json.loads(request.body)
             user = json_data['user']
             plan_id=json_data['plan_id']
             dashboard=json_data['dashboard']
             try:
                db_user=User.objects.get(username=user)
                db_profile=Profile.objects.get(user_id=db_user.id)
                db_profile.dashboard=dashboard
                data = {
                    "status":"ok",
                    "name": db_user.username,
                    "id": db_user.id,
                    "plan_id":db_profile.plan_id,
                    "dashboard": db_profile.dashboard
                }
             except:
                data={
                    "status":"error",
                    "description":"can not get the json"
                }

        return JsonResponse(data)



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (JSONParser,)

    @list_route(methods=['get'])
    def query(self, request):
            plan_id = request.query_params.get('plan_id', None)
            profile = fun_raw_sql_query(plan_id=plan_id)
            serializer = ProfileSerializer(profile, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def query_hw(self, request):
        plan_id = request.query_params.get('plan_id', None)
        profile = sql_query(plan_id=plan_id)

        return Response(profile, status=status.HTTP_200_OK)


    @detail_route(methods=['post'])
    def save(self,request,pk=None):
        json_data = json.loads(request.body)
        plan_id=json_data['plan_id']
        dashboard=json_data['dashboard']  # output dict
        dashboard=json.dumps(dashboard)   # convert json
        dashboard=str(dashboard)          # convert string
        plan_id=str(plan_id)              # convert string
        if plan_id and dashboard:
            profile = fun_sql_cursor_update(plan_id=plan_id,dashboard=dashboard,pk=pk)
        return Response(profile, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def saveHW(self,request,pk=None):
        json_data=json.loads(request.body)
        plan_id = json_data['plan_id']
        dashboard = json_data['dashboard']  # output dict
        dashboard = json.dumps(dashboard)  # convert json
        dashboard = str(dashboard)  # convert string
        plan_id = str(plan_id)

        h=json_data['h']
        w=json_data['w']
        h=str(h)
        w=str(w)


        profile = fun_sql_cursor_update_hw(plan_id=plan_id,dashboard=dashboard,width=w,hight=h,pk=pk)


        return Response(profile, status=status.HTTP_200_OK)


    # queryset = File.objects.all()
    # serializer_class = ProfileSerializer
    # parser_classes = (MultiPartParser, FormParser)

    @list_route(methods=['post'])
    def upload_file(self,request):
        inputFile = request.FILES['excel']
        fname = inputFile.name
        if fname[-4:] == '.csv' or fname[-4:] == '.CSV':
            dest = os.path.join('./media/csv/', fname)
            storage = open(dest,'wb')
            for c in inputFile.chunks():
                storage.write(c)
            storage.close()
            data = {
                "status" :  "ok",
                "file_name" : fname,
                "description" : "Success"
            }
        elif fname[-4:] == '.txt' or fname[-4:] == '.TXT':
            dest = os.path.join('./', fname)
            storage = open(dest,'wb')
            for c in inputFile.chunks():
                storage.write(c)
            storage.close()
            data = {
                "status" :  "ok",
                "file_name" : fname,
                "description" : "Success"
            }
        else:
            data = {
                "status":"error",
                "description":"Not a correct file"
            }
        return Response(data, status = status.HTTP_200_OK)
    @list_route(methods=['post'])
    def upload_xml_file(self,request):
        f2=request.FILES['xml']
        fname=f2.name
        if fname[-4:]=='.xml' or fname[-4:]=='.XML':
            dest = os.path.join('/home/ntu/myDjango/mblog/media/xml/', fname)
            storage = open(dest, 'wb')
            for c in f2.chunks():
                storage.write(c)
            storage.close()
            data = {
                "status": "ok",
                "file_name": fname,
                "description": "Success"
            }
        else:
            data = {
                "status": "error",
                "description": "Not CSV file"
            }
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def create_table(self,request):
        json_data = json.loads(request.body)
        fname = json_data['filename']
        tree=ET.parse('/home/ntu/myDjango/mblog/media/'+fname)
        root = tree.getroot()
        sql_string = []
        for name in root.findall('tablename'):
            tablename = name.find('name').text
        for column in root.findall('column'):
            sql_string.append(column.find('attribute').text + ' ' + column.find('type').text)

        col = ",".join(i for i in sql_string)

        with connection.cursor() as cursor:
            query="CREATE TABLE %s (%s)" % (tablename,col)
            cursor.execute(query)
            data={
                "col":col,
                "status":"ok",
                "description":"create table success!"
            }
        return Response(data, status=status.HTTP_200_OK)


    @list_route(methods=['post'])
    def upload_to_db(self,request):
        json_data = json.loads(request.body)
        fname = json_data['filename']

        if Data.objects.from_csv("./media/" + fname):
            # SQL syntax
            data={
                "status": "ok",
            }
        else:
            data = {
                "status": "error",
            }

        return Response(data, status=status.HTTP_200_OK)



    @list_route(methods=['post'])
    def upload_image(self,request):
            image=request.FILES['image']
            image_name=image.name
            if image_name[-4:]=='.jpg' or image_name[-4:]=='.png' or image_name[-5:]=='.jpeg':
                dest = os.path.join('/home/ntu/myDjango/mblog/media/image/', image_name)
                storage = open(dest, 'wb')
                for c in image.chunks():
                    storage.write(c)
                storage.close()
                data={
                    "status":"ok",
                    "description":"Success",
                    "url":"http://140.112.26.237:8002/media/image/"+image_name
                }
            else:
                data={
                    "status":"error",
                    "description":"Not a picture"

                }
            return Response(data,status=status.HTTP_200_OK)



    @list_route(methods=['post'])
    def download_file(self,request):
        json_data = json.loads(request.body)
        filename=json_data['filename']
        start_time=json_data['start_time']
        end_time=json_data['end_time']
        checkvalue=json_data['checkValue']
        col=",".join(i for i in checkvalue) #let it become col1,col2,..
        col=col.lower() #convert to lower capital


        with connection.cursor() as cursor:
            query="SELECT %s FROM mainsite_data WHERE date_time BETWEEN '%s' AND '%s'" % (col,start_time,end_time)
            cursor.execute(query)
            #cursor.execute("SELECT %s FROM mainsite_data WHERE date_time BETWEEN %s AND %s;", [filename,start_time, end_time])
            with open('media/export_output.csv',"w",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
            with zipfile.ZipFile('media/export_' + filename.rstrip('.csv') + '.zip', 'w') as zf:
             zf.write('/home/ntu/myDjango/mblog/media/'+'export_'+filename,'export_'+filename)

        data={
            "url":"http://140.112.26.237:8002"+"/media/"+"export_"+filename.rstrip('.csv')+".zip",

        }


        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def read_csv(self,request):
        csv_rows=[]
        json_data=json.loads(request.body)
        filename=json_data['filename']
        with open('media/'+filename) as csvfile:
            rows=csv.DictReader(csvfile)
            title = rows.fieldnames
            for row in rows:
                csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])

        return Response(csv_rows, status=status.HTTP_200_OK)



    @list_route(methods=['post'])
    def jt_to_json(self,request):
        json_data=json.loads(request.body)
        start_time = json_data['start_time']
        end_time = json_data['end_time']
        
        with connection.cursor() as cursor:
            query="SELECT array_to_json(array_agg(row_to_json(t))) FROM (SELECT * FROM mainsite_data WHERE date_time BETWEEN '2015-06-09T02:00:00' AND '2015-06-10T03:00:00')t"
            cursor.execute(query)
            big_array=cursor.fetchone()
        return Response(big_array, status=status.HTTP_200_OK)
    
    @list_route(methods=['post'])    
    def mli_to_json(self,request):
        json_data=json.loads(request.body)
        table=json_data['table']
        start_time = json_data['start_time']
        end_time = json_data['end_time']
        with connection.cursor() as cursor:
            query="SELECT array_to_json(array_agg(row_to_json(t))) FROM (SELECT * FROM %s WHERE date_time BETWEEN '%s' AND '%s')t" % (table,start_time,end_time)
            cursor.execute(query)
            big_array=cursor.fetchone()
        return Response(big_array, status=status.HTTP_200_OK)

    @list_route(methods=['post'])    
    def header_to_json(self,request):
        json_data=json.loads(request.body)
        table = json_data['table']


        with connection.cursor() as cursor:
            query="SELECT column_name FROM information_schema.columns WHERE table_name='%s'" % (table)
            cursor.execute(query)
            big_array=cursor.fetchall()
            d={}
            for col,i in zip(big_array,range(len(big_array))):
                d[str(i)]=col
            result=json.dumps(d,sort_keys=True) # CONVERT TO OBJ
            # result= [{'col'+str(i): v} for v,i in zip(big_array,range(len(big_array)))]
            # for col,i in zip(big_array,range(len(big_array))):  # after modify
            # result={
            #    "col1":big_array[1],
            #    "col2":big_array[2],
            #    "col3":big_array[3],
            #    "col4":big_array[4],
            #    "col5":big_array[5],
            #    "col6":big_array[6],
            #    "col7":big_array[7],
            #    "col8":big_array[8],
            #    "col9":big_array[9],
            #    "col10":big_array[10],
            # }

        return Response(result, status=status.HTTP_200_OK)
            

    @list_route(methods=['post'])
    def read_data(self,request):
        data_row1 = []
        data_row2 = []
        data_row3 = []
        data=[]
        json_data = json.loads(request.body)
        start_time = json_data['start_time']
        end_time = json_data['end_time']
        checkvalue = json_data['checkValue']
        x=json_data['x']
        x=x.lower()
        col = ",".join(i for i in checkvalue)  # let it become col1,col2,..
        col = col.lower()  # convert to lower capital


        with connection.cursor() as cursor:

            if x=='date_time':
                query = "SELECT date_time,%s FROM mainsite_data WHERE date_time BETWEEN '%s' AND '%s'" % (
                col, start_time, end_time)
                cursor.execute(query)
                result = namedtuplefetchall(cursor)
                data_row1=[[[int(time.mktime(r[0].timetuple()))*1000+8*3600*1000,float(r[i])] for r in result] for i in range(1,len(checkvalue)+1)]
            else:
                query = "SELECT %s,%s FROM mainsite_data WHERE date_time BETWEEN '%s' AND '%s'" % (x,col, start_time, end_time)
                cursor.execute(query)
                result = namedtuplefetchall(cursor)
                data_row1 = [
                    [[ float(r[0]),float(r[i])] for r in result]
                    for i in range(1, len(checkvalue) + 1)]

                for i in range(0, len(checkvalue)):
                    data_row1[i].sort(key=lambda x:x[0])

        return Response(data_row1, status=status.HTTP_200_OK)
    
    @list_route(methods=['post'])
    def read_paper(self,request):
        
        json_data = json.loads(request.body)
        keyword = json_data['keyword']
        keyword ="%"+keyword+"%"
        result=[]
        with connection.cursor() as cursor:
            query = "SELECT * FROM public.papers WHERE chinese_title LIKE '%s'"  % (keyword)
            cursor.execute(query)
            papers = namedtuplefetchall(cursor)
            # ipdb.set_trace()
            # for paper in papers:


        return Response(papers, status=status.HTTP_200_OK)
    
    # @list_route(methods=['post'])
    # def get_recommand_paper(self, request):
    #     json_data = json.loads(request.body)
    #     keyword = json_data['keyword']
    #     sentences = json_data['sentence']
    #     for sentence in sentences:
    #         if keyword in 




    #     return Response(papers, status=status.HTTP_200_OK)
    @list_route(methods=['post'])
    def read_papers(self,request):
        
        json_data = json.loads(request.body)
        keywords = json_data['keyword']
        all_paper={}
        
        for keyword in keywords:
            keyword ="%"+keyword+"%"
            result=[]
            with connection.cursor() as cursor:
                query = "SELECT * FROM public.papers WHERE chinese_title LIKE '%s'"  % (keyword)
                cursor.execute(query)
                papers = namedtuplefetchall(cursor)
                keyword=keyword.replace("%","")
                all_paper[keyword]=papers
        
        return Response(all_paper, status=status.HTTP_200_OK) 
    
    @list_route(methods=['post'])
    def get_device_info(self, request):
        json_data = json.loads(request.body)
        device_name = json_data['device']
        device_name = "%" + device_name + "%"
        with connection.cursor() as cursor:
                query = "SELECT * FROM devices WHERE device_name LIKE '%s'"  % (device_name)
                cursor.execute(query)
                papers = namedtuplefetchall(cursor)

        return Response(papers, status=status.HTTP_200_OK) 
    
    @list_route(methods=['post'])
    def read_opc(self,request):
        json_data = json.loads(request.body)
        value = json_data['value']
        url="opc.tcp://192.168.1.101:4840"
        client=Client(url,timeout=60*1)
        
        client.connect()
        
        Temp=client.get_node("ns=2;i=2")
        Temperature=Temp.get_value()
        print(Temperature)

        Press=client.get_node("ns=2;i=3")
        Pressure=Press.get_value()
        print(Pressure)

        TIME=client.get_node("ns=2;i=4")
        TIME_Value=TIME.get_value()
        print(TIME_Value)

        Freq=client.get_node("ns=2;i=5")
        Frequency=Freq.get_value()
        Cur=client.get_node("ns=2;i=6")
        Current=Cur.get_value()
        Hum=client.get_node("ns=2;i=7")
        Humidity=Hum.get_value()



        data={
                "Temperature":Temperature,
                "Pressure": Pressure,
                "TIME_Value":TIME_Value,
                "Freq":Frequency,
                "Current":Current,
                "Humidity": Humidity,
        }
        
         
        
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def get_keywords(self,request):
        json_data = json.loads(request.body)
        keyword = [json_data['keyword']]
        topn=json_data['topn']
        model_path = os.path.join('../mblog/models/', 'word2vec.model')
       
        result=[]
        model = models.Word2Vec.load(model_path)
        if len(keyword) == 1:
            res = model.most_similar(keyword[0],topn = topn)
            result=[item[0] for item in res]
            keywords={
                "keywords":result
            }
        else:
            keywords={
                "keywords":"No relative keyword(OOV)"
            }
        return Response(keywords, status=status.HTTP_200_OK) 


class BatchViewSet(viewsets.ModelViewSet):
    # revise
    queryset = File.objects.all()
    # serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    @list_route(methods=['post'])
    def execution(self,request):
        json_data=json.loads(request.body)
        parameter=json_data['parameter'] #maybe delete
        conn=psycopg2.connect(database="DB",user='root',password="lab125a",host='140.112.26.237',port="5432")
        # conn=psycopg2.connect(database="DB",user='root',password="lab125a",host='127.0.0.1',port="5432")
        
        cur=conn.cursor()
        cur.execute("SELECT * FROM Tasks")
        task_rows=cur.fetchall()
        # First Read the Task info
        for task_row in task_rows:
            task_id=task_row[0]
            if parameter==task_id:            
                task_name=task_row[1]
                task_functiontype=task_row[2]
                task_functionID=task_row[3]
                task_parameters=task_row[4]
                task_status=task_row[5]
                task_inputfile=task_row[8]
        # compare the task_functionID and function_id
        cur.execute("SELECT * FROM Functions")
        function_rows=cur.fetchall()
        for function_row in function_rows:
            function_id=function_row[0] 
            if task_functionID==function_id: 
            
                function_name=function_row[1]
                function_parameter=function_row[2]
                function_fileparameter=function_row[3]
                function_show=function_row[4]
                function_nextfunctionid=function_row[5]
                function_version=function_row[6]
                function_creator=function_row[7]
                function_createtime=function_row[8]
                function_commandpath=function_row[9]
            
        cur.execute("UPDATE Tasks SET Status=1") #doing
        result=subprocess.run([task_parameters,function_commandpath,function_parameter,function_fileparameter,task_inputfile],stdout=subprocess.PIPE)
        cur.execute("UPDATE Tasks SET Status=2") # done
        output=result.stdout.decode("utf-8") 
        f=open('output.txt','w')
        f.write(output)
        path=os.path.abspath('output.txt')
        print("Success Output File!!!!")
        
        
		# task_parameter='python'
		# function_commandpath='add.py'
		# function_parameter='abc'
		# function_fileparameter='-f'
		# task_inputfile='data.txt'
		# command_line=python add.py abc -f data.txt
        cur.execute("UPDATE Tasks SET Status=0") #reset
        cur.execute("UPDATE Tasks SET resultfile='%s'" % (str(path)))
        profile={
                    "result":task_parameters+" "+function_commandpath+" "+function_parameter+" "+function_fileparameter+" "+task_inputfile,
                    "parameter":parameter
        }
        conn.commit()
        conn.close()
        

        return JsonResponse(profile)
    
    @list_route(methods=['post'])
    def execute_wine(self, request):
        json_data = json.loads(request.body)
        exeFile = json_data['exeFile']
        inputFile = json_data['inputFile']
        outputFile1 = json_data['outputFile1']
        outputFile2 = json_data['outputFile2']
        # retcode = subprocess.call(cmd, shell=True)
        cmd = 'DISPLAY=:0 wine ./media/exe_files/'+ exeFile[:-4] + "/" + exeFile + " ./" + inputFile
        # problem HydroCRest read ./input.txt so can't change dir path
        retcode = subprocess.call(cmd, shell=True)
        # cmd = 'rm input.txt'
        # retcode = subprocess.call(cmd, shell=True)
        # print(retcode)
        # output waveloads.txt

        # fp = open('./' + outputFile1,"r")
        # line = fp.readline()
        # all_data_dict = {}
        # all_line = []
        # while line:
        #     one_line_data = line.split('\t')
        #     all_data_dict[one_line_data[0]] = np.array(one_line_data[1:-1]).astype(np.float)
        #     line = fp.readline()
        # all_line.append(all_data_dict)
        # all_data_dict = {}
        
        
        # cmd = 'mv waveloads.txt ./media/result/'
        # retcode = subprocess.call(cmd, shell=True)
        cmd = 'mv '+ outputFile1 + ' ./media/result/'
        retcode = subprocess.call(cmd, shell=True)
        if outputFile2 != None:
            cmd = 'mv '+ outputFile2 +' ./media/result/'
            retcode = subprocess.call(cmd, shell=True)
            if retcode == 0:
                result = {
                    "status": "ok",
                    "outputFile": "http://140.112.26.237:8002/media/result/"+ outputFile1,
                    "outputImage":"http://140.112.26.237:8002/media/result/"+ outputFile2,
                    "data": "No Data"

                }
            else:
                result = {
                    "status": "error",
                    "result_file": "No such file",
                    "data" : "No data"
                }

        else:
            if retcode == 0:
                result = {
                        "status": "ok",
                        "outputFile": "http://140.112.26.237:8002/media/result/"+ outputFile1,
                        "data": "No Data"

                    }
            else:
                result = {
                "status": "error",
                "result_file": "No such file",
                "data" : "No data"
                }
        return Response(result ,status=status.HTTP_200_OK)
    
    @list_route(methods=['post'])
    def get_similarity(self, request):
        json_data = json.loads(request.body)
        sentence = json_data['sentences']
        number = json_data['number']
        mode = json_data['mode']
        from recommand.main import Similarity
        # Similarity.preprocess()
        #Similarity.doc2bow()
        # Similarity.genTfIdf()
        if mode =='tableCreate':
            output = Similarity.genGoogleTopSimilarites(sentence, number)
        else:
            output = Similarity.genArticleTopSimilarities(sentence, number)
        return Response(output ,status=status.HTTP_200_OK)

    




    @list_route(methods=['post'])
    def execute_matlab(self, request):
        csv_rows = []
        json_data = json.loads(request.body)
        url = json_data['url']
        port = json_data['port']
        deployable_archive = json_data['deployable_archive']
        function_name = json_data['function_name']
        filename = json_data['filename']
        conn = http.client.HTTPConnection(url + ':' + port)
        headers = { "Content-Type": "application/json"}
        body = json.dumps({"nargout": 1, "rhs" : ['../../media/csv/'+filename]})
        conn.request("POST", "/" + deployable_archive + "/" + function_name , body, headers)
        response = conn.getresponse()
        if response.status == 200:
            result = json.loads(response.read())
            with open('media/matlab_files/dp.csv') as csvfile:
                rows = csv.reader(csvfile)
                for row in rows:
                    csv_rows.append([row[i] for i in range(len(row))])
            if "lhs" in result:
                output = {
                    "status": "success",
                    "data" : csv_rows,
                    "csv_file":"http://140.112.26.237:8002/media/matlab_files/dp.csv",
                    "image":"http://140.112.26.237:8002/media/matlab_files/plot_output.png"
                }
            elif "error" in result:
                output = {
                    "status": "error",
                    "data" : str(result["error"]["message"])
                }
        else:
            output = {
                    "status": "error",
                    "data" : "response error"
            }

        print(json_data)
       
            
        return Response(output ,status=status.HTTP_200_OK)




    @list_route(methods=['post'])
    def script_execution(self,request):

        json_data=json.loads(request.body)
        parameter=json_data['parameter'] #maybe delete
        conn=psycopg2.connect(database="DB",user='root',password="lab125a",host='140.112.26.237',port="5432")
        # conn=psycopg2.connect(database="DB",user='root',password="lab125a",host='127.0.0.1',port="5432")
        cur=conn.cursor()
        parameter=int(parameter)
        cur.execute("SELECT * FROM Tasks WHERE id=%d" % (parameter)) # find the task_id
        task_rows=cur.fetchall()  # fetch all column
        for task_row in task_rows:
            task_id=task_row[0] # if paramter==task_id
            if parameter==task_id:            
                task_name=task_row[1]
                task_functiontype=task_row[2]
                task_functionID=task_row[3]
                task_parameters=task_row[4]
                task_status=task_row[5]
                task_stepnumber=task_row[6]
                task_nowstep=task_row[7]
                task_inputfile=task_row[8]

        i=1
        while task_nowstep<=task_stepnumber and i<=task_stepnumber:# not yet done
            cur.execute("SELECT * FROM Functions WHERE id=%d" %(task_functionID)) # find the func you execute
            function_rows=cur.fetchall()

            for function_row in function_rows: #read parameter
                function_id=function_row[0]
                if task_functionID==function_id:

                    function_name=function_row[1]
                    function_parameter=function_row[2]
                    function_fileparameter=function_row[3]
                    function_show=function_row[4]
                    function_nextfunctionid=function_row[5]
                    function_version=function_row[6]
                    function_creator=function_row[7]
                    function_createtime=function_row[8]
                    function_commandpath=function_row[9]


            cur.execute("UPDATE Tasks SET Status=1")  # doing
            result = subprocess.run(
                [task_parameters, function_commandpath, function_parameter, function_fileparameter, task_inputfile],
                stdout=subprocess.PIPE)

            output1 = result.stdout.decode("utf-8")
            output = output1.strip('\n')
            function_parameter=output
            cur.execute("UPDATE Functions SET parameter	='%s'" % (function_parameter))
            f = open('output'+str(i)+'.txt', 'w')
            f.write(output)
            f.flush()
            path = os.path.abspath('output'+str(i)+'.txt')
            task_inputfile=str(path)
            i = i+1
            task_nowstep=task_nowstep+1
            task_functionID= function_nextfunctionid




        
        
		# task_parameter='python'
		# function_commandpath='add.py'
		# function_parameter='abc'
		# function_fileparameter='-f'
		# task_inputfile='data.txt'
		# command_line=python add.py abc -f data.txt
        cur.execute("UPDATE Tasks SET Status=0 WHERE id=2") #reset
        cur.execute("UPDATE Tasks SET resultfile='%s' WHERE id=2" % (str(path)))
        cur.execute("UPDATE Tasks SET inputfile='data.txt' WHERE id=2")
        profile={
                    "result":task_parameters+" "+function_commandpath+" "+function_parameter+" "+function_fileparameter+" "+task_inputfile,
                    "parameter":parameter
        }
        conn.commit()
        conn.close()
        

        return JsonResponse(profile)
    
    @list_route(methods=['post'])
    def exe_thread(self,request):
        json_data=json.loads(request.body)
        parameter=json_data['parameter'] #maybe delete
        t = threading.Thread(target =parameter)
        t.start()
        print("Start")
        t.join()
        print("End")








