import datetime

import backtrader as bt
import backtrader.analyzers as btan
import pandas as pd

from strategys import *

if __name__ == '__main__':

    # 初始化模型
    cerebro = bt.Cerebro()

    # 加载数据到模型中
    dataname = 'history_data/ETHUSDT_1H.csv'
    dataframe = pd.read_csv(dataname)
    dataframe['datetime'] = pd.to_datetime(dataframe['datetime'],
                                           unit="ms")  # 转换日期格式

    # print(dataframe)

    dataframe.set_index('datetime', inplace=True)
    data = bt.feeds.PandasData(dataname=dataframe,
                               fromdate=datetime.datetime(2021, 3, 1),
                               todate=datetime.datetime(2022, 6, 25))

    #    timeframe=bt.TimeFrame.Minutes)

    # 导入数据
    cerebro.adddata(data)
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Days)

    # 构建策略
    mystrategy = DEMA
    strats = cerebro.addstrategy(strategy=mystrategy)

    cerebro.addanalyzer(btan.SharpeRatio, _name="SharpeRatio")
    cerebro.addanalyzer(btan.DrawDown, _name='DrawDown')

    # 设定初始资金和佣金
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(0.0005)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=50)

    # cerebro.broker.set_filler(bt.broker.filler.FixedBarPerc(perc=0.1))
    # cerebro.broker.set_filler(bt.broker.filler.FixedSize(size=1))

    # 策略执行前的资金
    print('启动资金: %.2f' % cerebro.broker.getvalue())

    # 策略执行
    result = cerebro.run()
    print('执行策略后的资金: %.2f' % cerebro.broker.getvalue())
    print('夏普比率：{}'.format(
        result[0].analyzers.SharpeRatio.get_analysis()['sharperatio']))
    print('最大回撤：{}'.format(
        result[0].analyzers.DrawDown.get_analysis()['max']['drawdown']))
    # 绘图
    cerebro.plot(style="candle")
