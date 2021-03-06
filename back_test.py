import sys
import pandas as pd  
import numpy as np
import tushare as ts 
import matplotlib.pyplot as plt
import myStrategy as ms
import backtrader as bt
import get_ts_data as gtd
from datetime import datetime


#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

ts.set_token('14cdd17e72410feeb5f4f588c34774e85c6ab132c86a35ca4252f50b')
pro = ts.pro_api()


def search_param_BF(code, start_date, end_date='', startcash=10000, qts=500, com=0.001):
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

'''
Parameters optiization using PSO (Particle Swarm Optimization)
'''
def search_param_PSO(code, start_date, end_date='', startcash=10000, qts=500, com=0.001):
    import optunity
    import optunity.metrics

    def run(rsi_upper, rsi_lower, pfast, pslow):
        #创建主控制器
        cerebro = bt.Cerebro()
        #添加策略
        cerebro.addstrategy(ms.MyStrategy_MI_1, rsi_upper=rsi_upper, rsi_lower=rsi_lower, pfast=pfast, pslow=pslow)
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
        print('期初总资金: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        # cerebro.run(maxcpus=1)
        print('期末总资金: %.2f' % cerebro.broker.getvalue())
       
        print('Current Parameters:')
        print('rsi_lower = %.2f' % rsi_lower)
        print('rsi_upper = %.2f' % rsi_upper)
        print('pfast = %.2f' % pfast)
        print('pslow = %.2f' % pslow)
        print()      
        return cerebro.broker.getvalue()
    
    opt = optunity.maximize(run, num_evals=100, rsi_upper=[10,100], rsi_lower=[5,100], pfast=[5, 60], pslow=[10, 200])
    
    optimal_pars, details, _ = opt
    print('Optimal Parameters:')
    print('rsi_lower = %.2f' % optimal_pars['rsi_lower'])
    print('rsi_upper = %.2f' % optimal_pars['rsi_upper'])
    print('pfast = %.2f' % optimal_pars['pfast'])
    print('pslow = %.2f' % optimal_pars['pslow'])
    
    return optimal_pars

'''
test poss
'''
def search_param_PSO_test(code, strategy, start_date, end_date, startcash, qts, com, num_evals, **kwarg):
    import optunity
    import optunity.metrics

    '''
    CHANGE PARAM CONF HERE
    '''
    def run(pfast, pslow):
        #创建主控制器
        cerebro = bt.Cerebro()
        #添加策略
        '''
        CHANGE PARAM CONF HERE
        '''
        cerebro.addstrategy(strategy, pfast=pfast, pslow=pslow, printlog=False)

        #获取数据
        df = gtd.get_daily_qfq(pro, code, start_date, end_date, retry_count=3, pause=2)
        df.index=pd.to_datetime(df.trade_date)
        df = df.sort_index()
        df=df[['open','high','low','close','vol']]
        start_close_price = df['close'][0]
        end_close_price = df['close'][-1]
        print(f'股价期间变化: {(end_close_price/start_close_price-1)*100:.2f}%')
        
        #将数据加载至回测系统
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)
        #broker设置资金、手续费
        cerebro.broker.setcash(startcash)
        cerebro.broker.setcommission(commission=com)
        #设置买入设置，策略，数量
        cerebro.addsizer(bt.sizers.FixedSize, stake=qts)
        # print('期初总资金: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        # print('期末总资金: %.2f' % cerebro.broker.getvalue())
        
        
        print('Current Parameters:')
        # print('rsi_lower = %.2f' % rsi_lower)
        # print('rsi_upper = %.2f' % rsi_upper)
        print('pfast = %.2f' % pfast)
        print('pslow = %.2f' % pslow)
        print()
        return cerebro.broker.getvalue()
    
    opt = optunity.maximize(run, num_evals=num_evals, **kwarg)
    optimal_params, details, _ = opt
    print('-- Optimization Finished --')
    # print(details)
    print('time used: %.2fs' % float(details.stats['time']))
    print('best value: %.2f' % float(details.optimum))
    print('best rate: %.2f%s' % (float(details.optimum - startcash) / startcash * 100, '%')) 
    print()
    print('Optimal Parameters:')
    key_list = list(optimal_params.keys())
    key_list.sort()
    for key in key_list:
        print('%s = %.2f' % (str(key), optimal_params[key]))
    return optimal_params


#使用最优参数
def run_fixed(code, strategy, best_params, start_date, end_date='', startcash=10000, qts=500, com=0.001, **kwarg):
    print('--start date: %s, end_date: %s--' % (str(start_date), str(end_date)))
    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()
    #获取数据
    df = gtd.get_daily_qfq(pro, code, start_date, end_date, retry_count=3, pause=2)
    df.index=pd.to_datetime(df.trade_date)
    df=df[['ts_code', 'open','high','low','close','vol']]
    df = df.sort_index()
    data=bt.feeds.PandasData(dataname=df,
                                fromdate=datetime.strptime(start_date, "%Y%m%d"),
                                todate=datetime.strptime(end_date, "%Y%m%d"))
    # 加载数据
    cerebro.adddata(data)
    # 将交易策略加载到回测系统中
    #设置printlog=True，表示打印交易日志log
    """CHANGE HERE """
    cerebro.addstrategy(strategy, **kwarg)
    
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
    #获取期间股价
    start_close_price = df['close'][0]
    end_close_price = df['close'][-1]

    #Print out the final result
    print(best_params)
    print(f'总资金: {portvalue:.2f}')
    print(f'收益率: {(portvalue/startcash-1)*100:.2f}%')
    print(f'股价期间变化: {(end_close_price/start_close_price-1)*100:.2f}%')
    print()

def evaluate(code, strategy, best_params, eval1_start_date, eval2_start_date, eval3_start_date, end_date, startcash, qts, **kwarg):
    run_fixed(code, strategy, best_params, eval1_start_date, eval2_start_date, startcash, qts, **kwarg)
    run_fixed(code, strategy, best_params, eval1_start_date, eval3_start_date, startcash, qts, **kwarg)
    run_fixed(code, strategy, best_params, eval1_start_date, end_date, startcash, qts, **kwarg)



def plot_stock(code,title,start,end):
    dd=ts.get_k_data(code,autype='qfq',start=start,end=end)
    dd.index=pd.to_datetime(dd.date)
    dd.close.plot(igsize=(14,6),color='r')
    plt.title(title+'价格走势\n'+start+':'+end,size=15)
    plt.annotate(f'期间累计涨幅:{(dd.close[-1]/dd.close[0]-1)*100:.2f}%', xy=(dd.index[-150],dd.close.mean()),
             xytext=(dd.index[-500],dd.close.min()), bbox = dict(boxstyle = 'round,pad=0.5',
            fc = 'yellow', alpha = 0.5),
             arrowprops=dict(facecolor='green', shrink=0.05),fontsize=12)
    plt.show()


def ask_param():
    code = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    start_asset = int(sys.argv[4])
    shares_per_action = int(sys.argv[5])
    return code, start_date, end_date, start_asset, shares_per_action


if __name__ == '__main__':
    code = '002594.SZ'
    strategy = ms.MyStrategy_DMA
    train_start_date = str(20000101)
    eval1_start_date = str(20180101)
    eval2_start_date = str(20190101)
    eval3_start_date = str(20200101)
    end_date = str(20210101)
    
    start_asset = 1000000
    shares_per_action = 3000
    com=0.001
    num_evals = 10000
    # code, start_date, end_date, start_asset, shares_per_action = ask_param()
    
    '''
    CHANGE PARAM CONF HERE
    '''
    best_params = search_param_PSO_test(code, strategy, train_start_date, eval1_start_date, start_asset, shares_per_action, com, num_evals, pfast=[2, 60], pslow=[10, 200])
    
    '''
    best_params = {
            #'rsi_upper': 24.58984375, 
            #'rsi_lower': 37.470703125, 
            'pfast': 15.205078125, 
            'pslow': 117.24609375}
    '''
    print()
    print('-- Starting Final Backtest --')
    print(best_params)
    print('start date: %s, end_date: %s' % (str(eval1_start_date), str(end_date)))
    print('start_asset: %s, shares_per_action: %s' % (start_asset, shares_per_action))
    print()
    evaluate(code, strategy, best_params, eval1_start_date, eval2_start_date, eval3_start_date, end_date, startcash=start_asset, qts=shares_per_action, **best_params)
    



