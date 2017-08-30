
# coding: utf-8

# # 106年Q2 上市公司各產業EPS統計資訊分析

# **欲解決的問題：** 那一些產業/上市公司的獲利創況是值得關注的
# 
# *藉由產業別與個別的公司獲利狀況去篩選可行的投資標的*
# 
# * 資料來源: 政府資料開放平台 https://data.gov.tw
# 
# * 資料項目: 上市公司各產業EPS統計資訊
# 
# * 資料時間：106年Q2

# ****
# ## 1. 引入各項Pandas設定及導入資料

# In[120]:

#import library
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

get_ipython().magic('pylab inline')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('precision',3)
pd.options.display.float_format = '{:,.4f}'.format


# In[115]:

#import data
path = 'C:/Users/AdamChang/Documents/Python Scripts/data/PFD Data/上市公司各產業EPS統計資訊.csv'
df = pd.read_csv(path, encoding='big5hkscs', index_col=0, skiprows=1, 
                 names=['Code','Company','Industry','Eps','Denomination','OperationIncome',
                       'OperationProfit','OtherIncome','NetProfitAfterTax'])


# ****
# # **2.檢視Data Profile**

# In[123]:

import pandas_profiling


# In[125]:

pandas_profiling.ProfileReport(df)


# ***
# # **3.依照公司的Eps, 營業收益, 稅後淨利篩選各指標的前10大上市公司**

# In[127]:

#檢視前10大Eps的上市公司
#view top 10 eps companies
dfEps = df.sort_values(by='Eps', ascending=False)
dfEps.head(10)


# In[118]:

#檢視前10大營業收益的上市公司
#top 10 operation income company
dfOI = df.sort_values(by='OperationIncome', ascending=False)
dfOI.head(10)


# In[128]:

#檢視前10大稅後獲利率的上市公司
#top 10 Profit Rate company
df['Profit'] = df['NetProfitAfterTax']/df['OperationIncome']
dfProfit = df.sort_values(by='Profit', ascending=False)
dfProfit.head(10)


# In[129]:

#檢視基本統計資訊
#check summary of the data
df.describe()


# ****
# # 4.依照產業類別做篩選，篩選出高Eps與獲利的上市公司

# In[133]:

from bokeh.io import output_notebook, show
from bokeh.charts import Histogram

output_notebook()


# In[134]:

#檢視上市公司的獲利分布
#View the Eps distribution
EpsHist = Histogram(df, values='Eps')
show(EpsHist)


# In[104]:

#檢視上市公司營收狀況分布
#View the distribution of Operation Income
OperationIncomeHist = Histogram(df, values='OperationIncome')
show(OperationIncomeHist)


# In[51]:

#檢視ouliar的資料
#find the outliar
df[df.Eps>20]


# In[52]:

# 3008高獲利，但也高門檻，先將他從投資選項中剃除
# 3008 have high Eps, but also high stock price. Remove it from the data
dfDelOutl = df.drop(df[df.Eps>20].index)

#再度檢視Eps分布狀況
#View the distribution of Eps again.
EpsHist2 = Histogram(dfDelOutl, values='Eps')
show(EpsHist2)


# In[53]:

IndsGroup = dfDelOutl.groupby('Industry')
IndsGroup


# In[95]:

#將各行業的Eps, 營業收入, 稅後收入加總，檢視各行業的獲利狀況，評估賺錢的行業為何

IndsGroupEpsSum = IndsGroup.agg(np.sum)
IndsGroupEpsSum.sort_values(by='Eps',ascending=False).style.highlight_max(axis=0)


# In[66]:

#將各行業的Eps, 營業收入, 稅後收入取平均值，看各行業內企業的獲利狀況，評估哪個行業的平均概況較好
IndsGroupEpsMean = IndsGroup.agg(np.mean)
IndsGroupEpsMean.sort_values(by='Eps',ascending=False).style.highlight_max(axis=0)


# In[135]:

#將各行業Eps平均值與加總彙整比較
IndsEpsSum = IndsGroupEpsSum['Eps']
IndsEpsMean = IndsGroupEpsMean['Eps']
IndEps = pd.DataFrame({'EpsSum':IndsEpsSum,
                      'EpsMean':IndsEpsMean})
IndEps['Percent'] = IndEps['EpsMean']/IndEps['EpsSum']
IndEps.sort_values(by='EpsSum', ascending=False).style.highlight_max(axis=0)


# In[57]:

from bokeh.charts import Bar


# In[139]:

p = Bar(dfDelOutl,label='Industry',values='Eps', legend=None, agg='mean',title='各產業別Eps平均值')
show(p)


# In[140]:

p3 = Bar(dfDelOutl,label='Industry',values='Eps', legend=None, agg='sum',color='Green',title='各產業內企業Eps總和')
show(p3)


# In[72]:

from bokeh.charts import Scatter
from bokeh.models import HoverTool


# In[75]:

# Eps產業加總 對照 稅後淨利加總做比較
hover = HoverTool(tooltips=[
        ('Industry','@Industry')])

p2 = Scatter(IndsGroupEpsSum, x='Eps', y='NetProfitAfterTax', color='Industry', tools=['crosshair',hover,'save'], legend=None)
show(p2)


# In[101]:

#檢視前10大Eps加總的行業
IndsGroupEpsSum = IndsGroupEpsSum.sort_values(by='Eps', ascending=False)
IndsGroupEpsSum.head(10)


# In[76]:

#Eps 各產業平均 對照 稅後淨利平均做比較
hover = HoverTool(tooltips=[
        ('Industry','@Industry')])

p2 = Scatter(IndsGroupEpsMean, x='Eps', y='NetProfitAfterTax', color='Industry', tools=['crosshair',hover,'save'], legend=None)
show(p2)


# # 依照上述兩表，過濾出Eps門檻>1.4 或 稅後淨利>1500000的企業

# In[94]:

IndsGroupEpsMean.loc[(IndsGroupEpsMean.Eps>1.4) | (IndsGroupEpsMean.NetProfitAfterTax>1500000)]


# 交叉比較，挑出以下產業別做進一步篩選：
# - 其它
# - 其他電子業
# - 半導體業
# - 塑膠工業
# - 油電燃氣業

# In[102]:

ChooseIndustry = ['其他','其他電子業','半導體業','塑膠工業','油電燃氣業']


# In[142]:

#看上述5個產業Eps最高的企業為何, 與各自的Eps

for i in ChooseIndustry:
    dfChoose = df[df.Industry==i].sort_values(by='Eps',ascending=False)
    print('Industry:',i)
    print(dfChoose[['Company','Eps']].head(5))
    print('\n')

