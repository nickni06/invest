# coding=utf-8
import sys
import time
import pandas as pd
import get_ts_data as gtd

'''
------------ general functions ------------
'''


def get_ts_code(engine):
    """查询ts_code"""
    return pd.read_sql('select ts_code from stock_basic', engine)


'''
------------ stock basics ------------
'''


def truncate_update(engine, data, table_name):
    """删除mysql表所有数据，to_sql追加新数据"""
    conn = engine.connect()
    conn.execute('truncate ' + table_name)
    data.to_sql(table_name, engine, if_exists='append', index=False)


def update_stock_basic(engine, pro, retry_count, pause):
    """更新 股票信息 所有数据"""
    data = gtd.get_stock_basic(pro, retry_count, pause)
    print(data)
    truncate_update(engine, data, 'stock_basic')


'''
------------ daily ------------
'''

'''
删除所有日期区间内股票日线数据
'''


def delete_daily(engine, start_date, end_date):
    """删除 日线行情 数据"""
    conn = engine.connect()
    conn.execute('delete from daily where  trade_date between ' + str(start_date) + ' and ' + str(end_date))


def update_all_daily(engine, pro, codes, start_date, end_date, retry_count, pause):
    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = gtd.get_daily(pro, value, start_date, end_date, retry_count, pause)
        df.to_sql('daily', engine, if_exists='append', index=False)
        sys.stdout.write('------ ' + str(value) + ' updated to table successfully!\n')
        time.sleep(0.6)


def update_daily_date(engine, pro, date, retry_count, pause):
    """日期方式更新 日线行情"""
    df = gtd.get_daily_date(pro, date, retry_count, pause)
    df.to_sql('daily', engine, if_exists='append', index=False)


'''
------------ financial info ------------
'''

'''
获取财报三张表，业绩预告、快报，财务指标数据
'''


def update_all_income(engine, pro, codes, start_date, end_date, retry_count, pause):

    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = gtd.get_income(pro, value, start_date, end_date, retry_count, pause)
        df = df.drop_duplicates(subset=['ts_code', 'end_date', 'report_type'])
        df.to_sql('income', engine, if_exists='append', index=False)
        sys.stdout.write('------ ' + str(value) + ' updated to table income successfully!\n')
        time.sleep(1.0) # 接口每分钟规定最多50次访问


def update_all_balancesheet(engine, pro, codes, start_date, end_date, retry_count, pause):
    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = gtd.get_balancesheet(pro, value, start_date, end_date, retry_count, pause)
        try:
            df = df.drop_duplicates(subset=['ts_code', 'end_date', 'report_type'])
            df.to_sql('balancesheet', engine, if_exists='append', index=False)
            sys.stdout.write('------ ' + str(value) + ' updated to table balancesheet successfully!\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n')
        time.sleep(1.0)


def update_all_cashflow(engine, pro, codes, start_date, end_date, retry_count, pause):
    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = gtd.get_cashflow(pro, value, start_date, end_date, retry_count, pause)
        try:
            df = df.drop_duplicates(subset=['ts_code', 'end_date', 'report_type'])
            df.to_sql('cashflow', engine, if_exists='append', index=False)
            sys.stdout.write('------ ' + str(value) + ' updated to table cashflow successfully!\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n')
        time.sleep(1.0)


def update_all_forecast(engine, pro, codes, start_date, end_date, retry_count, pause):
    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = gtd.get_forecast(pro, value, start_date, end_date, retry_count, pause)
        try:
            df = df.drop_duplicates(subset=['ts_code', 'end_date'])
            df.to_sql('forecast', engine, if_exists='append', index=False)
            sys.stdout.write('------ ' + str(value) + ' updated to table forecast successfully!\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n')
        time.sleep(1.0)


def update_all_express(engine, pro, codes, start_date, end_date, retry_count, pause):
    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = gtd.get_express(pro, value, start_date, end_date, retry_count, pause)
        try:
            df = df.drop_duplicates(subset=['ts_code', 'end_date'])
            df.to_sql('express', engine, if_exists='append', index=False)
            sys.stdout.write('------ ' + str(value) + ' updated to table express successfully!\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n')
        time.sleep(1.0)


def update_all_fina_indicator(engine, pro, codes, start_date, end_date, retry_count, pause):
    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = gtd.get_fina_indicator(pro, value, start_date, end_date, retry_count, pause)
        try:
            df = df.drop_duplicates(subset=['ts_code', 'end_date'])
            df.to_sql('fina_indicator', engine, if_exists='append', index=False)
            sys.stdout.write('------ ' + str(value) + ' updated to table fina_indicator successfully!\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n')
        time.sleep(1.0)
