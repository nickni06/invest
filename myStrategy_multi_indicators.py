from datetime import datetime
import backtrader as bt
import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
class MyStrategy(bt.Strategy):
    params = dict(
        pfast=30,  # period for the fast moving average
        pslow=100,   # period for the slow moving average
        rsi_per=14,
        rsi_upper=65.0,
        rsi_lower=35.0,
        rsi_out=50.0,
        warmup=35,
        printlog=False
    )

    def __init__(self):
        #指定价格序列
        self.data0=self.datas[0].close

        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None

        #添加指标
        sma1 = bt.ind.SMA(self.data0, period=self.p.pfast)
        sma2 = bt.ind.SMA(self.data0, period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

        rsi = bt.indicators.RSI(period=self.p.rsi_per,
                                upperband=self.p.rsi_upper,
                                lowerband=self.p.rsi_lower)

        self.crossdown = bt.ind.CrossDown(rsi, self.p.rsi_upper)
        self.crossup = bt.ind.CrossUp(rsi, self.p.rsi_lower)

        
    #策略核心，根据条件执行买卖交易指令（必选）
    def next(self):
        # 记录收盘价
        #self.log(f'收盘价, {data0[0]}')
        if self.order: # 检查是否有指令等待执行, 
            return
        # 检查是否持仓   
        if not self.position: # 没有持仓
            #执行买入条件判断：收盘价格上涨突破15日均线
            if self.crossover > 0 or self.crossup > 0:
                self.log('BUY CREATE, %.2f' % self.data0[0])
                #执行买入
                self.buy()         
        else:
            #执行卖出条件判断：收盘价格跌破15日均线
            if self.crossover <= 0 or self.crossdown < 0:
                self.log('SELL CREATE, %.2f' % self.data0[0])
                #执行卖出
                self.order = self.sell()

    #交易记录日志（可省略，默认不输出结果）
    def log(self, txt, dt=None,doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()},{txt}')

    #记录交易执行情况（可省略，默认不输出结果）
    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]: 
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}')
            self.bar_executed = len(self) 

        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None

    #记录交易收益情况（可省略，默认不输出结果）
    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')

    #回测结束后输出结果（可省略，默认输出结果）
    def stop(self):
        self.log('(MA均线： %2d日和%2d日) 期末总资金 %.2f' %
                 (self.p.pfast, self.p.pslow, self.broker.getvalue()), doprint=True)
