import backtrader as bt
import backtrader.indicators as btind

class SMA(bt.Strategy):
    """
    SMA(Simple Moving Average)
    计算公式: MA = (C1 + C2 + C3 + ... + Cn) / n, Cn是时刻 n 的收盘价。
    """
    params = (('period', 16),)

    def __init__(self):
        self.sma = btind.MovingAverageSimple(self.data, period=self.p.period)
        self.buy_sig = btind.CrossOver(self.data.close, self.sma)

    def next(self):
        if not self.position and self.buy_sig[0] == 1:
            self.order = self.buy()
        if self.position and self.buy_sig[0] == -1:
            self.order = self.close()
        # if self.position and self.buy_signal[0] == 1:
        #     self.order = self.close()  # 清仓
        #     self.order = self.buy()
        # if self.position and self.buy_signal[0] == -1:
        #     self.order = self.close()  # 清仓
        #     self.order = self.sell()