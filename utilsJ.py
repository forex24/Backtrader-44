# 数据接口
import akshare as ak
import baostock as bs
import tushare as ts

# 基础模块
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

# 返回样式以Backtrader为准调整


def index_tushare(token, stock_code,
                  s_date=datetime.datetime.now()-datetime.timedelta(days=365),
                  e_date=datetime.datetime.now()):
    ts.set_token(token)
    pro = ts.pro_api()
    df = pro.index_daily(ts_code=stock_code,
                         fields='trade_date,open,high,low,close,vol',
                         start_date=s_date.strftime('%Y%m%d'),
                         end_date=e_date.strftime('%Y%m%d'))
    df.index = pd.to_datetime(df.trade_date)
    df.drop('trade_date', axis=1, inplace=True)
    df = df.astype('float')
    df.rename(columns={'vol': 'volume'}, inplace=True)
    df['openinterest'] = 0
    return df.iloc[::-1]


def stock_tushare(token, stock_code,
                  s_date=datetime.datetime.now()-datetime.timedelta(days=365),
                  e_date=datetime.datetime.now()):
    ts.set_token(token)
    pro = ts.pro_api()
    df = pro.daily(ts_code=stock_code,
                   fields='trade_date,open,high,low,close,vol',
                   start_date=s_date.strftime('%Y%m%d'),
                   end_date=e_date.strftime('%Y%m%d'))
    df.index = pd.to_datetime(df.trade_date)
    df.drop('trade_date', axis=1, inplace=True)
    df = df.astype('float')
    df.rename(columns={'vol': 'volume'}, inplace=True)
    df['openinterest'] = 0
    return df.iloc[::-1]


def index_to_csv_tushare(token, stock_index, time_sleep=0.5,
                         s_date=datetime.datetime.now()-datetime.timedelta(days=365),
                         e_date=datetime.datetime.now(), fpath='.\\Data\\'):
    pro = ts.pro_api(token)
    index_list = np.unique(pro.index_weight(index_code=stock_index,
                                            start_date=s_date.strftime('%Y%m%d'),
                                            end_date=e_date.strftime('%Y%m%d')).con_code).tolist()
    for s_code in index_list:
        df = stock_tushare(token, s_code, s_date, e_date)
        time.sleep(time_sleep)
        df.to_csv(fpath + s_code + '.csv')
    return
