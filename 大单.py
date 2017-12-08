import tushare as ts

df = ts.get_sina_dd('300377', date='2017-12-08', vol=1000) #默认400手
#df = ts.get_sina_dd('600848', date='2015-12-24', vol=500)  #指定大于等于500手的数据

print(df)
