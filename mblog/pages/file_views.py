import subprocess
import os
from  mainsite import form,models
from django.contrib import messages
# Another import

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import simplejson as json
from django.http import JsonResponse
from mainsite.serializers import ProfileSerializer#,DataSerializer
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from mainsite.models import fun_raw_sql_query,fun_sql_cursor_update,fun_sql_cursor_update_hw,sql_query
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.template import RequestContext
from rest_framework.views import APIView
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
from mainsite.models import Profile, User, User_Plan, Plan, Plan_Table, File, Matlab_Info
import datetime
from rest_framework.views import APIView
import scholarly



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class GETTABLEPERMISSION(APIView):

    @csrf_exempt
    def post(self, request):
        table_list = []
        alias_table_list = []
        tables = []
        json_data = json.loads(request.body)
        username = json_data['username']
        plan_id  = json_data['plan_id']
        try:
            db_user = User.objects.get(username = username)  # if username=admin then get admin row
            a_plan_table = Plan_Table.objects.filter(plan_id = plan_id).order_by("created_at")
            for item in a_plan_table:
                dic = {"table_name":item.table_name , "alias_table_name":item.alias_table_name ,"columns":item.columns}
                table_list.append(item.table_name)
                alias_table_list.append(item.alias_table_name)
                tables.append(dic)
            logging.info("Suceess")

            plan = Plan.objects.get(id=plan_id)
            user_id = db_user.id
            plan_name = plan.plan_name
            data = {
                "plan_id": plan_id,
                "plan_name": plan_name,
                "user_id": user_id,
                "tables": table_list,
                "alias_tables":alias_table_list,
                "tables_name":tables
            }
            logging.info("Get table success!")
        except Exception as err:
            logging.info("Error: {}".format(err))
        return Response(data, status = status.HTTP_200_OK)

class FileUploadViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    @list_route(methods=['post'])
    def get_plans(self, request):
        data = []
        json_data = json.loads(request.body)
        username = json_data['username'] # get a user name
        user = User.objects.get(username=username)  # if username = admin then get admin row
        profile = Profile.objects.get(user_id=user.id)
        user_id = profile.user_id
        plan_id = profile.plan_id
        user_plans = User_Plan.objects.filter(user_id_id=user.id)
        for user_plan in user_plans:
            plan_id_id = user_plan.plan_id_id
            plan = Plan.objects.get(id = plan_id_id)
            plan_name = plan.plan_name
            data.append({"plan_id":"plan" + str(plan_id_id),"plan_name":plan_name[:4]})

        return Response(data, status = status.HTTP_200_OK)

    @list_route(methods=['post'])
    def upload_exe_file(self, request):
        exeFile = request.FILES['exe']
        fname = exeFile.name
        try:
            if fname[-4:] == '.exe' or fname[-4:] == '.EXE':
                if not os.path.isdir('./media/exe_files/' + fname[:-4]):
                    os.mkdir('./media/exe_files/' + fname[:-4])
                exedest = os.path.join('./media/exe_files/'+ fname[:-4], fname)
                exestorage = open(exedest,'wb')
                for c in exeFile.chunks():
                    exestorage.write(c)
                exestorage.close()
                data = {
                    "status" :  "ok",
                    "file_name": fname,
                    "file_path": exedest,
                    "description":"File save success"
                }
            else:
                data = {
                    "status" :  "error",
                    "description":"Not a EXE File"
                }
        except Exception as err:
            data = {
                    "status":"error",
                    "description":err
            }
        if len(request.FILES) == 2:
            inputFile = request.FILES['input']
            iname = inputFile.name
            try:
                if iname[-4:] == '.txt' or iname[-4:] == '.TXT':
                    inputdest = os.path.join('./media/exe_files/'+ fname[:-4], iname)
                    inputstorage = open(inputdest,'wb')
                    for c in inputFile.chunks():
                        inputstorage.write(c)
                    inputstorage.close()
                    data = {
                        "status" :  "ok",
                        "file_name": fname,
                        "file_path": exedest,
                        "doc_name": iname,
                        "doc_path":inputdest,
                        "description":"File save success"
                    }
                    
                else:
                        data = {
                            "status" :  "error",
                            "description" : "Not a TXT File"
                        }
            except Exception as err:
                    data = {
                        "status":"error",
                        "description":err
                    }
            print(data)
        return Response(data, status = status.HTTP_200_OK)

    
    
    @list_route(methods=['post'])
    def get_file_permission(self, request):
        files_list = []
        doc_path = []
        output1 = []
        output2 = []
        json_data = json.loads(request.body)
        username = json_data['username'] # get a user name
        db_user = User.objects.get(username = username)  # if username=admin then get admin row
        user_plans = User_Plan.objects.filter(user_id = db_user.id)
        for user_plan in user_plans:
            user_plan = user_plan
        a_plan = user_plan.plan_id  # get is a object (a plan)
        a_file = File.objects.filter(plan_id = a_plan)
        for item in a_file:
            files_list.append(item.file_name)
            doc_path.append(item.doc_path)
            output1.append(item.outputfile1)
            output2.append(item.outputfile2)
        user_id = db_user.id
        plan_id = a_plan.id
        plan_name = a_plan.plan_name
        data = {
            "plan_id": plan_id,
            "plan_name": plan_name,
            "user_id": user_id,
            "files": files_list,
            "docs":doc_path,
            "output1":output1,
            "output2":output2
        }
        return Response(data, status = status.HTTP_200_OK)

    @list_route(methods=['post'])
    def get_matlab_permission(self, request):
        matlab_list = []
        json_data = json.loads(request.body)
        username = json_data['username'] # get a user name
        db_user = User.objects.get(username = username)  # if username=admin then get admin row
        user_plans = User_Plan.objects.filter(user_id = db_user.id)
        for user_plan in user_plans:
            user_plan =user_plan
        a_plan = user_plan.plan_id  # get is a object (a plan)
        a_matlab = Matlab_Info.objects.filter(plan_id = a_plan)

        for item in a_matlab:
            url = item.url + ":" + item.port + "/" + item.deployable_archive + "/" + item.function_name
            matlab_list.append(url)

        user_id = db_user.id
        plan_id = a_plan.id
        plan_name = a_plan.plan_name
        data = {
            "plan_id": plan_id,
            "plan_name": plan_name,
            "user_id": user_id,
            "url": matlab_list
        }
        return Response(data, status = status.HTTP_200_OK)

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
        try:
            if fname[-4:]=='.xml' or fname[-4:]=='.XML':
                dest = os.path.join('./media/xml/', fname)
                storage = open(dest, 'wb')
                for c in f2.chunks():
                    storage.write(c)
                storage.close()
                
                data = {
                    "status": "ok",
                    "file_name": fname,
                    "file_path": dest,
                    "description": "Success"
                }
                logging.info(data)
            else:
                data = {
                    "status": "error",
                    "file_name": "no_file_name",
                    "file_path": "no_file_path",
                    "description": "Not XML file"
                }
                logging.info(data)
        except Exception as err:
            print(err)
        return Response(data, status=status.HTTP_200_OK)
    
    @list_route(methods=['post'])
    def insert_matlab_info(self, request):
        json_data = json.loads(request.body)
        username = json_data['username'] 
        url = json_data['url']
        port = json_data['port']
        deployable_archive = json_data['deployable_archive']
        function_name = json_data['function_name']
        permission_name = json_data['permission_name']
        description = json_data['description']
        table_name = json_data['table_name']
        is_active = json_data['is_active']
        try:
            db_user = User.objects.get(username=username)
            user_id =  db_user.id
            user_plans = User_Plan.objects.filter(user_id = user_id)
            for user_plan in user_plans:
                user_plan = user_plan
            plan_id = user_plan.plan_id  # get is a object (a plan)sc
            now = datetime.datetime.now()
            
            with connection.cursor() as cursor:
                    query = "INSERT INTO %s ( user_id_id , plan_id_id, url, port ,deployable_archive, function_name, permission_name , created_at, last_time, is_active) \
                            VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%r');" \
                            % (table_name, user_id, plan_id.id, url, port , deployable_archive, function_name, permission_name, now, now, is_active)
                    cursor.execute(query)
                    data = {
                        "status":"Success",
                        "description":"Insert matlab information success!"
                    }
        except Exception as err:
            data = {
                "status":"Error",
                "description":err
            }
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def insert_file_info(self, request):
        json_data = json.loads(request.body)
        username = json_data['username'] # get a user name
        file_name = json_data['file_name']
        file_path = json_data['file_path']
        doc_name = json_data['doc_name']
       
        doc_path =json_data['doc_path']
        table_name = json_data['table_name']
        description = json_data['description']
        permission_name = json_data['permission_name']
        plan_id = json_data['plan_id']
        db_user = User.objects.get(username=username)
        user_id =  db_user.id
        # user_plan = User_Plan.objects.get(user_id = user_id)
        # plan_id = user_plan.plan_id  # get is a object (a plan)
        # a_file = File.objects.filter(plan_id = plan_id)
        
        
        now = datetime.datetime.now()
        
        with connection.cursor() as cursor:
            
            try:
                query = "INSERT INTO %s ( user_id_id , plan_id_id, file_path, file_name ,file_description, permission_name, created_at, last_time) \
                        VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s');" \
                        % (table_name, user_id, plan_id, file_path, file_name , description, permission_name, now, now)
                cursor.execute(query)
                data = {
                    "status":"ok",
                    "description":"Insert file information success!"
                }
            except Exception as err:
                data = {
                    "status":"error",
                    "description":err
                }
        return Response(data, status=status.HTTP_200_OK)



    @list_route(methods=['post'])
    def create_table(self,request):
        json_data = json.loads(request.body)
        fname = json_data['filename']
        plan_id = json_data['plan_id']
        description = json_data['description']
        permission_name = ""
        now = datetime.datetime.now()
        tree=ET.parse('./media/xml/'+fname)
        root = tree.getroot()
        sql_string = []
        columns =[]
        arr = []
        for name in root.findall('tablename'):
            tablename = name.find('name').text
        for name in root.findall('aliasTableName'):
            aliasTableName = name.find('name').text
        for column in root.findall('column'):
            columns.append(column.find('attribute').text)
            sql_string.append(column.find('attribute').text + ' ' + column.find('type').text)
        for pkey in root.findall('primarykey'):
            primary_key = pkey.find('key').text
        

        col = ",".join(i for i in sql_string)
        for item in columns:
            dict = {"alias_colum_name":'',"unit":'',"column_name":item}
            arr.append(dict)
        column_data = json.dumps(arr)
 
        try:
            with connection.cursor() as cursor:
                create_query = "CREATE TABLE %s (%s , PRIMARY KEY (%s));" % (tablename, col, primary_key)
                cursor.execute(create_query)
                # logging.info("create table success")
                insert_query = "INSERT INTO %s ( table_name , plan_id_id , permission_name, created_at, alias_table_name, columns) \
                        VALUES ('%s', %s, '%s', '%s','%s','%s');" % ('public.plan_table',tablename, plan_id, permission_name, now, aliasTableName,column_data)
                cursor.execute(insert_query)
                logging.info("insert  table  info success")
            data = {
                "status":"ok",
                "description":"create table success!"
            }
        except Exception as err:
            data = {
                "status":"error",
                "description":"create table failed!"
            }
            logging.info("Error message is :{}".format(err))
            
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def list_all_table(self, request):
        json_data = json.loads(request.body)
        table_name = json_data['table_name']
        table_name = table_name + '%'
        with connection.cursor() as cursor:
            query = "SELECT   tablename   FROM   pg_tables WHERE   tablename    LIKE   '%s'  ORDER   BY   tablename;" % (table_name)
            cursor.execute(query)
            big_array = cursor.fetchall()
            data = {
                "status":"ok",
                "data":big_array
            }
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def upload_to_db(self,request):
        json_data = json.loads(request.body)
        fname = json_data['filename']
        table = json_data['table']
       

        try:
            with open("./media/csv/"+fname, 'r') as f:
                logging.info("read f")
                
                with connection.cursor() as cursor:
                    cursor.copy_from(f,table,sep=',')
                    connection.commit()
                    data = {
                        "status":"ok"
                    }
                    logging.info("save")
        except Exception as err:
            data = {
                "status":"error"
            }
            logging.info("Error message is {}".format(err))

       


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
    def read_csv_with_no_header(self,request):
        csv_rows = []
        json_data = json.loads(request.body)
        filename = json_data['filename']
        with open('media/'+filename) as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                # print(row)
                csv_rows.append([row[i] for i in range(len(row))])
        
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
        json_data = json.loads(request.body)
        table = json_data['table']
        columns = json_data['columns']
        start_time = json_data['start_time']
        end_time = json_data['end_time']
        
        print(table)
        if 'date_time' in columns:
            columns.remove('date_time')
            sql_columns = ",".join(column for column in columns) #let it become col1,col2,..
            sql_columns = sql_columns.lower() #convert to lower capital
            sql_columns = 'to_char( date_time, \'YYYY-MM-DD HH24:MI:SS\') date_time ,' + sql_columns
        else:
            sql_columns = ",".join(column for column in columns) #let it become col1,col2,..
            sql_columns = sql_columns.lower() #convert to lower capital
        
        

        
        with connection.cursor() as cursor:
            #query = "SELECT array_to_json(array_agg(row_to_json(t))) FROM (SELECT * FROM %s WHERE date_time BETWEEN '%s' AND '%s' ORDER BY date_time ASC)t" % (table,start_time,end_time)
            query="SELECT array_to_json(array_agg(row_to_json(t))) FROM (SELECT %s FROM %s WHERE date_time BETWEEN '%s' AND '%s' ORDER BY date_time ASC)t" % (sql_columns, table, start_time, end_time)
            # query = "SELECT %s FROM %s" % (sql_columns, table)
            cursor.execute(query)
            big_array = cursor.fetchall()
            print(big_array)
            
        return Response(big_array, status=status.HTTP_200_OK)

    @list_route(methods=['post'])    
    def header_to_json(self,request):
        json_data=json.loads(request.body)
        table = json_data['table']


        with connection.cursor() as cursor:
            query = "SELECT column_name FROM information_schema.columns WHERE table_name='%s'" % (table)
            cursor.execute(query)
            big_array = cursor.fetchall()
            d = {}
            for col,i in zip(big_array,range(len(big_array))):
                d[str(i)] = col
            result = json.dumps(d,sort_keys=True) # CONVERT TO OBJ
           

        return Response(result, status=status.HTTP_200_OK)

    @list_route(methods=['post'])    
    def get_columns(self, request):
        json_data=json.loads(request.body)
        table = json_data['table']

        with connection.cursor() as cursor:
            query = "SELECT column_name FROM information_schema.columns WHERE table_name='%s'" % (table)
            cursor.execute(query)
            row = [item[0] for item in cursor.fetchall()]
 
        return Response(row, status=status.HTTP_200_OK)
            

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
                query = "SELECT %s,%s FROM public.mainsite_data WHERE date_time BETWEEN '%s' AND '%s'" % (x,col, start_time, end_time)
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
        with connection.cursor() as cursor:
            query = "SELECT * FROM public.papers WHERE chinese_title LIKE '%s'"  % (keyword)
            cursor.execute(query)
            papers = namedtuplefetchall(cursor)

        return Response(papers, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def google_search(self, request):   
        json_data = json.loads(request.body)
        keyword = json_data['keyword']
        result = []
        search_query = scholarly.search_pubs_query(keyword)
        for i in range(10):
            paper = next(search_query)
            result.append(paper.bib)
        return Response(result, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def google_search_graph(self, request):   
        json_data = json.loads(request.body)
        keywords = json_data['keyword']
        
        all_paper={}
        
        for keyword in keywords:
                search_query = scholarly.search_pubs_query(keyword)
                papers = []
                for i in range(5):
                    paper = next(search_query)
                    papers.append(paper.bib)
                all_paper[keyword]=papers
        return Response(all_paper, status=status.HTTP_200_OK)



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
        url="opc.tcp://192.168.3.101:4840"
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

