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
engine = create_engine('mysql://root:root@127.0.0.1/invest')
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
    # mf.delete_daily(engine, '19900101', '19991231')
    # sys.stdout.write('--- daily price deleted successfully!\n')
    codes = mf.get_ts_code(engine)
    mf.update_all_daily(engine, pro, codes, start_date, end_date, 3, 2)
    sys.stdout.write('--- daily price updated successfully!\n')
    # mf.update_daily_date(engine, pro, '20190702', 3, 2)



if __name__ == '__main__':
    start_date = 20200101
    end_date = 20201231
    update_stock_basics()
    update_daily(start_date, end_date)



