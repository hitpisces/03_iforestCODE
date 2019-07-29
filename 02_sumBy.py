#-*- coding: utf-8 -*-

import os

import pandas as pd
import pymysql


industryCode = "3982"
pathDir=os.path.abspath('.')
db=pymysql.connect("localhost","root","******","szwp_20190625")
cursor = db.cursor()
str_sql ="""Select `行政区`,`统一社会信用代码`,`单位详细名称`,replace(replace(`污染物排放量`,'吨',''),'千克','') as 污染物排放量,replace(replace(`污染物产生量`,'吨',''),'千克','') as 污染物产生量,`污染物名称` from `g106-1_产排污系数核算明细` where `行业代码`='3982'"""
cursor.execute(str_sql)
sqlResults=cursor.fetchall()
db.close()

columnDes = cursor.description
columnNames = [columnDes[i][0] for i in range(len(columnDes))]
df = pd.DataFrame([list(i) for i in sqlResults],columns=columnNames)

df[['污染物排放量']] = df[['污染物排放量']].apply(pd.to_numeric)
df[['污染物产生量']] = df[["污染物产生量"]].apply(pd.to_numeric)
grouped = df.groupby(['单位详细名称','行政区','统一社会信用代码','污染物名称'])['污染物排放量','污染物产生量'].apply(lambda x : x.sum()).reset_index()
print("完成分组，开始写入文件……")

fileName = industryCode+'.'+'xlsx'
f = open(pathDir + "//"+fileName,'w')
f.truncate()
grouped.to_excel(industryCode+".xlsx",index=True)
f.close()
print("文件写入完成！")
