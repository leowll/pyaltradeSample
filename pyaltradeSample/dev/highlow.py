__author__ = 'leo'

from pyalgotrade import strategy
from pyalgotrade.technical.highlow import High
from pyalgotrade.technical.highlow import Low


class highlow(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, highPeriod, lowPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        self.__bars = feed[instrument]
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__highPeriod = highPeriod
        self.__lowPeriod = lowPeriod
        self.__high = High(self.__prices, highPeriod)
        self.__low = Low(self.__prices, lowPeriod)

        # We'll use adjusted close values instead of regular close values.

    def buySignal(self, bars):
        if len(self.__prices) < self.__lowPeriod: return
        print self.__low[-1]
        return self.__prices[-1] == self.__low[-1]

    def sellSignal(self, bars):
        if len(self.__prices) < self.__highPeriod: return
        print self.__high[-1]
        return self.__prices[-1] == self.__high[-1]

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__position is None:
            if self.buySignal(bars):
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares, True)
        elif not self.__position.exitActive() and self.sellSignal(bars):
            self.__position.exitMarket()
