
from pyalgotrade import strategy
from pyalgotrade.technical import rsi
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.technical.cross import cross_above


class RSI(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, RSIPeriod, entrySMA, exitSMA):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__rsi = rsi.RSI(self.__prices, RSIPeriod)
        self.__entrySMA = ma.SMA(self.__prices, entrySMA)
        self.__exitSMA = ma.SMA(self.__prices, exitSMA)
        self.__lastbuy = 1000000
        
    def getEntrySMA(self):
        return self.__entrySMA

    def getExitSMA(self):
        return self.__exitSMA
    
    def getRSI(self):
        return self.__rsi

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()



    def onBars(self, bars):
        
        
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__exitSMA[-1] is None or self.__entrySMA[-1] is None or self.__rsi[-1] is None:
            return
        
        if self.__position is None:
            if self.buySignal():
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
                self.__lastbuy = self.getResult()
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and self.sellSignal() : 
            print self.getResult() / self.__lastbuy
            self.__position.exitMarket()

    def sellSignal(self):
        #return cross.cross_below(self.getExitSMA(), self.getEntrySMA()) #\
            
        return (self.getResult() / self.__lastbuy > 1.25 or self.__rsi[-1] > 80 ) \
            or (self.getResult() / self.__lastbuy < 0.9)
      
    
    def buySignal(self):
        min_rsi = min(self.__rsi[-2:-1])
        return self.__rsi[-1] < 20  #and self.__rsi[-1] > self.__rsi[-2] # and min_rsi < 20
        #return cross.cross_above(self.getExitSMA(), self.getEntrySMA())
       
