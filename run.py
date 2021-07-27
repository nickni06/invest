# coding=utf-8
import sys
import pandas as pd
import tushare as ts
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from stock_basics_tables_structure import Base
import mysql_functions as mf

# 创建数据库引擎
engine = create_engine('mysql://root:111111@127.0.0.1/invest')
conn = engine.connect()
sys.stdout.write('engine connected successfully\n')
# 创建mysql所有表结构
Base.metadata.create_all(engine)

# 连接 tushare
ts.set_token('14cdd17e72410feeb5f4f588c34774e85c6ab132c86a35ca4252f50b')
pro = ts.pro_api()

'''
----- stock_basics -----
'''
# 获取所有股票信息
def update_stock_basics():
    mf.update_stock_basic(engine, pro, 3, 2)

'''
----- daily -----
'''
# 根据需要增删 日线行情 数据  单次提取*4000*条
def update_daily(start_date, end_date):
    mf.delete_daily(engine, start_date, end_date)
    sys.stdout.write('--- daily price deleted successfully!\n')
    codes = mf.get_ts_code(engine)
    mf.update_all_daily(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- daily price updated successfully!\n')
    # mf.update_daily_date(engine, pro, '20190702', 3, 2)

'''
----- financial info -----
'''
# 根据需要增删 日线行情 数据  单次提取*4000*条
def update_income(start_date, end_date):
    codes = mf.get_ts_code(engine)
    mf.update_all_income(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- income table updated successfully!\n')

def update_balancesheet(start_date, end_date):
    codes = mf.get_ts_code(engine)
    mf.update_all_balancesheet(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- balancesheet table updated successfully!\n')

def update_cashflow(start_date, end_date):
    codes = mf.get_ts_code(engine)
    mf.update_all_cashflow(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- cashflow table updated successfully!\n')

def update_forecast(start_date, end_date):
    codes = mf.get_ts_code(engine)
    mf.update_all_forecast(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- forecast table updated successfully!\n')

def update_express(start_date, end_date):
    codes = mf.get_ts_code(engine)
    mf.update_all_express(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- express table updated successfully!\n')

def update_fina_indicator(start_date, end_date):
    codes = mf.get_ts_code(engine)
    mf.update_all_fina_indicator(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- fina_indicator table updated successfully!\n')

if __name__ == '__main__':
    start_date = 19900101
    end_date = 20210720
    
    # update_stock_basics()  # 更新股票代码信息

    # update_daily(start_date, end_date)  # 更新日线走势

    # update_income(start_date, end_date)

    # update_balancesheet(start_date, end_date)

    # update_cashflow(start_date, end_date)

    # update_forecast(start_date, end_date)

    # update_express(start_date, end_date)

    update_fina_indicator(start_date, end_date)
