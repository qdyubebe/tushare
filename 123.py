import tushare as ts

tf=ts.guba_sina()

df = ts.day_cinema() #取上一日全国影院票房排行数据
#df = ts.day_cinema('2015-12-24') #取指定日期的数据
df.head(10)


print ( tf )

print ( df )
