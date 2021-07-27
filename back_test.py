import pandas as pd  
import numpy as np
import tushare as ts 
import matplotlib.pyplot as plt
import myStrategy as ms
import backtrader as bt
import get_ts_data as gtd

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

ts.set_token('14cdd17e72410feeb5f4f588c34774e85c6ab132c86a35ca4252f50b')
pro = ts.pro_api()


def main(code, start_date, end_date='', startcash=10000, qts=500, com=0.001):
    #创建主控制器
    cerebro = bt.Cerebro()      
    #导入策略参数寻优
    cerebro.optstrategy(ms.MyStrategy,maperiod=range(3, 31))    
    #获取数据
    #df=ts.get_k_data(code,autype='qfq',start=start,end=end)
    df = gtd.get_daily(pro, code, start_date, end_date, retry_count=3, pause=2)
    df.index=pd.to_datetime(df.trade_date)
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
    main('600000','2010-01-01','',10000,1000)



