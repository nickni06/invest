import sys
import pandas as pd  
import numpy as np
import tushare as ts 
import matplotlib.pyplot as plt
import myStrategy as ms
import myStrategy_multi_indicators as msmi
import backtrader as bt
import get_ts_data as gtd
from datetime import datetime


#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

ts.set_token('14cdd17e72410feeb5f4f588c34774e85c6ab132c86a35ca4252f50b')
pro = ts.pro_api()


def search_param(code, start_date, end_date='', startcash=10000, qts=500, com=0.001):
    #创建主控制器
    cerebro = bt.Cerebro()      
    #导入策略参数寻优
    cerebro.optstrategy(msmi.MyStrategy,maperiod=range(3, 51))    
    #获取数据
    df = gtd.get_daily_qfq(pro, code, start_date, end_date, retry_count=3, pause=2)
    df.index=pd.to_datetime(df.trade_date)
    df = df.sort_index()
    df=df[['open','high','low','close','vol']]
    #将数据加载至回测系统
    data = bt.feeds.PandasData(dataname=df)    
    cerebro.adddata(data)
    #broker设置资金、手续费
    cerebro.broker.setcash(startcash)           
    cerebro.broker.setcommission(commission=com)    
    #设置买入设置，策略，数量
    cerebro.addsizer(bt.sizers.FixedSize, stake=qts)   
    print('期初总资金: %.2f' %                    
    cerebro.broker.getvalue())    
    cerebro.run(maxcpus=1)    
    print('期末总资金: %.2f' % cerebro.broker.getvalue())


#使用最优参数
def run_fixed(code, start_date, end_date='', startcash=10000, qts=500, com=0.001):
    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()
    #获取数据
    df = gtd.get_daily_qfq(pro, code, start_date, end_date, retry_count=3, pause=2)
    df.index=pd.to_datetime(df.trade_date)
    df=df[['ts_code', 'open','high','low','close','vol']]
    df = df.sort_index()
    data = bt.feeds.PandasData(dataname=df,
                                fromdate=datetime(2010, 1, 1),
                                todate=datetime(2020, 3, 30) )
    data=bt.feeds.PandasData(dataname=df,
                                fromdate=datetime.strptime(start_date, "%Y%m%d"),
                                todate=datetime.strptime(end_date, "%Y%m%d"))
    # 加载数据
    cerebro.adddata(data)
    # 将交易策略加载到回测系统中
    #设置printlog=True，表示打印交易日志log
    cerebro.addstrategy(msmi.MyStrategy, printlog=True)
    # 设置初始资本为10,000
    cerebro.broker.setcash(startcash)
    # 设置交易手续费为 0.1%
    cerebro.broker.setcommission(commission=com)
    #设置买入设置，策略，数量
    cerebro.addsizer(bt.sizers.FixedSize, stake=qts)

    #回测结果
    cerebro.run()
    #获取最后总资金
    portvalue = cerebro.broker.getvalue()
    #Print out the final result
    print(f'总资金: {portvalue:.2f}')


def plot_stock(code,title,start,end):
    dd=ts.get_k_data(code,autype='qfq',start=start,end=end)
    dd.index=pd.to_datetime(dd.date)
    dd.close.plot(figsize=(14,6),color='r')
    plt.title(title+'价格走势\n'+start+':'+end,size=15)
    plt.annotate(f'期间累计涨幅:{(dd.close[-1]/dd.close[0]-1)*100:.2f}%', xy=(dd.index[-150],dd.close.mean()),
             xytext=(dd.index[-500],dd.close.min()), bbox = dict(boxstyle = 'round,pad=0.5',
            fc = 'yellow', alpha = 0.5),
             arrowprops=dict(facecolor='green', shrink=0.05),fontsize=12)
    plt.show()


if __name__ == '__main__':
    code = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    start_asset = int(sys.argv[4])
    shares_per_action = int(sys.argv[5])
    run_fixed(code, start_date, end_date, start_asset, shares_per_action)



