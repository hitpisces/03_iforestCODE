#-*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import IsolationForest
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
from warnings import simplefilter

simplefilter(action='ignore',category=FutureWarning)
simplefilter(action='ignore',category=DeprecationWarning)#关掉特性升级提升，如升级numpy>0.22要开起来！

pathDir=os.path.abspath('.')
indusCode="3982"
rng=np.random.RandomState(42)

df=pd.read_excel(pathDir+"//"+indusCode+".xlsx",'Sheet1')

f=open(pathDir+"//"+"columns.txt")
file=f.read()
col=file.split(',')
print("审核指标是：")
print(col)

groupdata=df.groupby(df["污染物名称"])
df_all=pd.DataFrame()
for (df["污染物名称"]),group in groupdata:
    df_new=pd.DataFrame(group)
    print(df_new)
    if(df_new.__len__()<5):
        continue
    X_Predict=df_new[col]
    clf = IsolationForest(n_estimators=100,
                          max_samples='auto',
                          contamination=0.01,
                          max_features=1.,
                          bootstrap=False,
                          n_jobs=1,
                          random_state=rng,
                          verbose=0)  # 孤立森林算法

    clf.fit(X_Predict)
    y_predict=clf.predict(X_Predict)

    # 将y = -1 的数据提取出来
    result_index = y_predict == -1
    a = X_Predict[result_index]

    # 将结果写入excel表格中
    df_new["异常值"]=y_predict
    df_all = df_all.append(df_new)
df_all.to_excel(pathDir+"//"+indusCode+"result.xlsx")
print("处理完成！")
