# -*- coding: utf-8 -*-
__author__ = 'leo'

from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.technical import rsi
from pyalgotrade.technical import highlow


class smarsi(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod, rsiPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        self.__bars = feed[instrument]
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__last_buy = 1000000
        self.__sma = ma.SMA(self.__prices, smaPeriod)
        self.__sma30 = ma.SMA(self.__prices, 30)
        self.__sma20 = ma.SMA(self.__prices, 20)
        self.__rsi = rsi.RSI(self.__prices, rsiPeriod)
        self.__buy_pos = None
        self.__sell_pos = None

    def getSMA(self, smaPeriod):
        return ma.SMA(self.__prices,smaPeriod)

    def getRSI(self):
        return self.__rsi

    def bigger_than_sma(self):
        if len(self.__prices) < 3: return
        return (self.__prices[-1] > self.__sma) and (self.__prices[-2] > self.__sma) \
               and (self.__prices[-3] > self.__sma)

    def buySignal(self, bars):
        # a> (价格上穿30日均线) && (价格>SMA价格的3% ||连续三日价格>SMA)
        return cross.cross_above(self.__prices, self.__sma30) and \
               (self.__prices[-1] > (self.__sma[-1] * 1.03) or self.bigger_than_sma())

    def sellSignal(self, bars):
        #         a> 价格下穿20日均线 并且 价格<SMA价格的97%
        #         b> 亏损超10%
        #         c> RSI>80
        #         c> 价格小于买入后最高价的90%
        if self.__buy_pos is None or self.__sell_pos is None:
            high_period = 0
        else:
            high_period = self.__buy_pos - self.__sell_pos
        return (cross.cross_below(self.__prices, self.__sma20) and self.__prices[-1] < self.__sma[-1] * 0.97) \
               or (self.__last_buy * 0.9 > self.getResult()) \
               or (self.__rsi > 80) \
               or (self.__prices < highlow.High(self.__prices, high_period) * 0.9)

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__position is None:
            if self.buySignal(bars):
                print self.__buy_pos
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares, True)
                self.__last_buy = self.getResult()
                self.__buy_pos = len(self.__prices)
                print 'ris', self.__rsi[-1], 'last buy', self.__last_buy, 'result:', self.getResult(), \
                'sma:', self.__sma[-1]
        elif not self.__position.exitActive() and self.sellSignal(bars):
            self.__sell_pos = len(self.__prices)
            self.__position.exitMarket()
