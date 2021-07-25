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
import tree_tools as tt
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit

import pydotplus

from sklearn.impute import SimpleImputer
import os

# 创建数据库引擎
engine = create_engine('mysql://root:111111@127.0.0.1/invest')
conn = engine.connect()
sys.stdout.write('engine connected successfully\n')
# 创建mysql所有表结构
Base.metadata.create_all(engine)

# 连接 tushare
ts.set_token('14cdd17e72410feeb5f4f588c34774e85c6ab132c86a35ca4252f50b')
pro = ts.pro_api()

Saving_PATH = r'C:\Users\haora\Desktop\invest\byd_tree_clf_fina_indicator_'
Lib_PATH = r'C:\Users\haora\PycharmProjects\pythonProject\venv\Lib'


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
    # fina_indicator_df.to_csv(r'C:\Users\haora\Desktop\byd_fina_indicator.csv')
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


def get_important_revelant(element_name, fina_indicators_series_list, price_change_list_dict, axis_lim=[-50, 50, -20, 20]):
    element_value_list = get_element(fina_indicators_series_list, element_name)
    l_e = pd.Series(element_value_list)
    l_b = pd.Series(price_change_list_dict['before_price_change_ratio_list'])
    l_rd = pd.Series(price_change_list_dict['report_date_price_change_ratio_list'])
    l_a = pd.Series(price_change_list_dict['after_price_change_ratio_list'])

    R_before = l_e.corr(l_b)
    R_report_date = l_e.corr(l_rd)
    R_after = l_e.corr(l_a)
    if abs(R_before) > 0.08 or abs(R_before) > 0.08 or abs(R_before) > 0.08:
        sys.stdout.write('important element: %s\n' % str(element_name))
    else:
        return
    sys.stdout.write('before: ' + str(R_before) + '\nreport_date: ' + str(R_report_date) + '\nafter: ' + str(R_after) + '\n')
    axis_lim = [l_e.min(), l_e.max(), -20, 20]
    print(axis_lim)
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


# 获得股票走势分类：decrease/increase
def get_change_category(price_change_list_dict):
    price_category_list_dict = {}
    before_cat_list, reportDate_cat_list, after_cat_list = [], [], []
    for price in price_change_list_dict['before_price_change_ratio_list']:
        price = float(price)
        if price > 0:
            before_cat_list.append('increase')
        else:
            before_cat_list.append('decrease')
    for price in price_change_list_dict['report_date_price_change_ratio_list']:
        price = float(price)
        if price > 0:
            reportDate_cat_list.append('increase')
        else:
            reportDate_cat_list.append('decrease')
    for price in price_change_list_dict['after_price_change_ratio_list']:
        price = float(price)
        if price > 0:
            after_cat_list.append('increase')
        else:
            after_cat_list.append('decrease')
    return {'before_category_list': before_cat_list, \
            'reportDate_category_list': reportDate_cat_list,
            'after_category_list': after_cat_list}

def tree_clf(X, Y_dict, price_period):
    Y = Y_dict[price_period]
    # tt.decison_tree_clf(X, Y, price_period)
    tt.cv_grid_search(X, Y, price_period)


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
    element_list = get_table_element_names(table_name)
    # for element in element_list[3: -1]:
    #     get_important_revelant(element, fina_indicators_series_list, price_change_list_dict)
    fina_indicator_df = pd.DataFrame(data=fina_indicators_series_list)
    price_category_list_dict = get_change_category(price_change_list_dict)
    # print(price_category_list_dict['before_category_list'])
    # print(fina_indicator_df['valuechange_income'])
    # print(len(price_category_list_dict['before_category_list']), len(fina_indicator_df['valuechange_income']))

    tree_clf(fina_indicator_df.iloc[:, 3:-1], price_category_list_dict, 'before_category_list')  # 3:-1 数字列
    tree_clf(fina_indicator_df.iloc[:, 3:-1], price_category_list_dict, 'reportDate_category_list')
    tree_clf(fina_indicator_df.iloc[:, 3:-1], price_category_list_dict, 'after_category_list')


if __name__ == '__main__':
    code = '002594.SZ' # 比亚迪
    main(code)


