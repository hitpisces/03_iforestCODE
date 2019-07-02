#-*- coding: utf-8 -*-

import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)

pathDir=os.path.abspath('.')
df=pd.read_excel(pathDir+"//"+"3982"+".xlsx",'Sheet2')
print(df.describe())
df.boxplot(['绝对值比'])
plt.show()