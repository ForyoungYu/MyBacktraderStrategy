import backtrader as bt
import backtrader.indicators as btind

class Keltner(bt.Strategy):
    def log(self, text, dt=None):
        dt = dt or self.datas[0].datatime.data(0)
