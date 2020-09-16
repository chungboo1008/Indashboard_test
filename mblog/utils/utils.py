import pandas as pd
import numpy as np
import json

def readMliColumns(file):
    df=pd.read_csv(file,encoding='utf-8',header=None)
    df
    df.iloc[0:,0:1]=''
    df
    dfs = []
    count = 0
    for i in range(1,df.columns.size-104*8,115): #find column size      15以前115
            df_tmp=df.iloc[0:,i:i+115]
            preheader=df.iloc[0:1,i:i+115]
            header1=np.append('時間',preheader)
            preheader2=df.iloc[1:2,i:i+115]
            header2=np.append(None,preheader2)
            preheader3=df.iloc[2:3,i:i+115]
            header3=np.append('date_time',preheader3)
            header3 = [c.lower() for c in header3] 
            ndarray = np.vstack((header1,header2,header3))
            pdd = pd.DataFrame(ndarray)
            pdd = pdd.fillna("")
            dfs.append(pdd)
            count+=1
    for i in range(df.columns.size-104*8,df.columns.size,104):    # 15後104
            df_tmp=df.iloc[:,i:i+104]
            preheader=df.iloc[0:1,i:i+104] #
            header1=np.append('時間',preheader)
            preheader2=df.iloc[1:2,i:i+104]
            header2=np.append(None,preheader2)
            preheader3=df.iloc[2:3,i:i+104]
            header3=np.append('date_time',preheader3)
            header3 = [c.lower() for c in header3] 
            ndarray = np.vstack((header1,header2,header3))
            pdd = pd.DataFrame(ndarray)
            pdd = pdd.fillna("")
            dfs.append(pdd)
            count+=1

def get_dict(k):
    k = k-1
    dicts =[]
    for i in range(len(dfs[k].columns)):
        dic = {
            "alias_column_name":dfs[k][i][0],
            "column_name":dfs[k][i][2],
            "unit":dfs[k][i][1],

        }
        j = json.dumps(dic,ensure_ascii=False)
        dicts.append(dic)
    
    jsObj = json.dumps(dicts)

    fileObject = open('jsonFile.json', 'w')
    fileObject.write(jsObj)