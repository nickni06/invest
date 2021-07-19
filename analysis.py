# coding=utf-8
import sys
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
import tushare as ts
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from stock_basics_tables_structure import Base
import mysql_functions as mf
import matplotlib.pyplot as plt
# 创建数据库引擎
engine = create_engine('mysql://root:111111@127.0.0.1/invest')
conn = engine.connect()
sys.stdout.write('engine connected successfully\n')
# 创建mysql所有表结构
Base.metadata.create_all(engine)

# 连接 tushare
ts.set_token('14cdd17e72410feeb5f4f588c34774e85c6ab132c86a35ca4252f50b')
pro = ts.pro_api()

def get_reports_dates(code):
    query = "select f_ann_date from invest.income where ts_code = '" + str(code) + "' order by f_ann_date;"
    df = pd.read_sql(sql=query, con=engine)
    return list(df['f_ann_date'])

'''
单只股票的财报时期股票走势
'''
def get_neighbors_moving(code, reports_dates_list):

    before_price_change_ratio_list,  report_date_price_change_ratio_list, after_price_change_ratio_list = [], [], []

    query = "select * from invest.daily where ts_code = '" + str(code) + "' order by trade_date;"
    daily_df = pd.read_sql(sql=query, con=engine)
    daily_dates_list = list(daily_df['trade_date'])
    is_pre_IPO_reports = True # 是否是IPO之前的财报

    #print(reports_dates_list)
    for report_date in reports_dates_list:
        #print(report_date)
        if is_pre_IPO_reports:
            if report_date not in daily_dates_list:
                sys.stdout.write(str(report_date) + "'s report is assumed as report before IPO\n")
                before_price_change_ratio_list.append(0)
                report_date_price_change_ratio_list.append(0)
                after_price_change_ratio_list.append(0)
                continue
            else:
                is_pre_IPO_reports = False
        if report_date not in daily_dates_list:
            print(str(report_date) + ' not in report_date list')
            for _ in range(5):
                print(str(report_date) + ' report report_date on weekend')
                date_datetime = pd.to_datetime(report_date, format='%Y%m%d')
                date_datetime = date_datetime - BDay(1)
                report_date = date_datetime.strftime('%Y%m%d')
                print('changed report_date: ' + str(report_date))
                if report_date in daily_dates_list:
                    print(str(report_date) + ' in list now')
                    break

        report_date_index = daily_dates_list.index(report_date)
        if report_date_index != len(daily_dates_list) - 1:  # 报告通常在当天收盘后，因此将其往后调整一天
            report_date_index += 1

        before_start_date = daily_dates_list[report_date_index-10]
        after_end_date = daily_dates_list[report_date_index+10]
        report_date = daily_dates_list[report_date_index]

        before_start_price = float(daily_df[daily_df['trade_date']==before_start_date]['pre_close'])
        before_end_price = float(daily_df[daily_df['trade_date']==report_date]['pre_close'])
        before_price_change_ratio = 100 * before_end_price / before_start_price - 100
        before_price_change_ratio_list.append(before_price_change_ratio)

        report_date_price_change_ratio = \
            100 * float(daily_df[daily_df['trade_date'] == report_date]['close']) / float(daily_df[daily_df['trade_date'] == report_date]['pre_close']) \
            - 100
        report_date_price_change_ratio_list.append(report_date_price_change_ratio)

        after_start_price = float(daily_df[daily_df['trade_date']==report_date]['close'])
        after_end_price = float(daily_df[daily_df['trade_date']==after_end_date]['close'])
        after_price_change_ratio = 100 * after_end_price / after_start_price - 100
        after_price_change_ratio_list.append(after_price_change_ratio)
    # return before_price_change_ratio_list,  report_date_price_change_ratio_list, after_price_change_ratio_list
    return {'before_price_change_ratio_list': before_price_change_ratio_list,
            'report_date_price_change_ratio_list': report_date_price_change_ratio_list,
            'after_price_change_ratio_list': after_price_change_ratio_list}

'''
提取单只股票的历史财报重要财务指标
'''
def get_report_fina_indicator(code, reports_dates_list):
    query = "select * from invest.fina_indicator where ts_code = '" + str(code) + "';"
    fina_indicator_df = pd.read_sql(sql=query, con=engine)
    fina_indicator_dates_list = list(fina_indicator_df['ann_date'])
    fina_indicators_list_list = []
    fina_indicators_series_list = []
    for date in reports_dates_list:
        if date in fina_indicator_dates_list:
            fina_indicators_series = fina_indicator_df[fina_indicator_df['ann_date'] == date].iloc[0,:]
            fina_indicators_list_list.append(list(fina_indicators_series))
            fina_indicators_series_list.append(fina_indicators_series)

        else:
            fina_indicators_list_list.append([])
            sys.stderr.write('ERROR: cannot find acquired date' + str(date))
    return fina_indicators_series_list, fina_indicators_list_list

def scatterplot(list_1, list_2):
    fig, ax = plt.subplots()

    ax.scatter(list_1, list_2, alpha=0.5)
    ax.grid(True)

    plt.axis([-50, 50, -20, 20])
    plt.show()

def get_element(series_list, element):
    element_list = []
    for tuple_ in series_list:
        element_list.append(tuple_[element])
    return element_list

def show_revelant(element_name, fina_indicators_series_list, price_change_list_dict, axis_lim=[-50, 50, -20, 20]):
    element_value_list = get_element(fina_indicators_series_list, element_name)
    l_e = pd.Series(element_value_list)
    l_b = pd.Series(price_change_list_dict['before_price_change_ratio_list'])
    l_rd = pd.Series(price_change_list_dict['report_date_price_change_ratio_list'])
    l_a = pd.Series(price_change_list_dict['after_price_change_ratio_list'])
    R_before = l_e.corr(l_b)
    R_report_date = l_e.corr(l_rd)
    R_after = l_e.corr(l_a)
    sys.stdout.write('before: ' + str(R_before) + '\nreport_date: ' + str(R_report_date) + '\nafter: ' + str(R_after) + '\n')
    plt.suptitle(element_name)
    plt.subplot(221)
    plt.title('before_price_change')
    plt.scatter(l_e, l_b)
    plt.axis(axis_lim)
    plt.axhline(0, color='red', alpha=0.7)
    plt.axvline(0, color='red', alpha=0.7)
    plt.grid(True)
    plt.subplot(222)
    plt.title('report_date_price_change')
    plt.scatter(l_e, l_rd)
    plt.axis(axis_lim)
    plt.axhline(0, color='red', alpha=0.7)
    plt.axvline(0, color='red', alpha=0.7)
    plt.grid(True)
    plt.subplot(223)
    plt.title('after_price_change')
    plt.scatter(l_e, l_a)
    plt.axis(axis_lim)
    plt.axhline(0, color='red', alpha=0.7)
    plt.axvline(0, color='red', alpha=0.7)
    plt.grid(True)
    plt.show()

def get_table_element_names(table_name):
    table_element_names_query = 'show columns FROM invest.' + str(table_name) + ';'
    return list(pd.read_sql(sql=table_element_names_query, con=engine)['Field'])

def test(code='002594.SZ'):
    query = "select * from invest.daily where ts_code = '" + str(code) + "';"
    daily_df = pd.read_sql(sql=query, con=engine)
    daily_dates_list = list(daily_df['trade_date'])
    return daily_dates_list

def main(code):
    reports_dates_list = get_reports_dates(code)
    price_change_list_dict = get_neighbors_moving(code, reports_dates_list)
    fina_indicators_series_list, fina_indicators_list_list = get_report_fina_indicator(code, reports_dates_list)
    table_name = 'fina_indicator'
    print(get_table_element_names(table_name))

    #element_name = 'bps_yoy'
    #show_revelant(element_name, fina_indicators_series_list, price_change_list_dict)

if __name__ == '__main__':
    code = '002594.SZ' # 比亚迪
    main(code)

