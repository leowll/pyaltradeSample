
from pyalgotrade import strategy
from pyalgotrade.technical.linebreak import LineBreak

class threelines(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        self.__bars = feed[instrument]
        self.__lines = LineBreak(self.__bars, 2)
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
    def buySignal(self, bars):
        if(len(self.__lines) < 3) : return
        line1 = self.__lines[-1]
        line2 = self.__lines[-2]
        line3 = self.__lines[-3] 
        return line1.isWhite() and line2.isWhite() and line3.isWhite()
        
    
    def sellSignal(self, bars):
        if(len(self.__lines) < 3) : return
        line1 = self.__lines[-1]
        line2 = self.__lines[-2]
        line3 = self.__lines[-3] 
        return line1.isBlack() and line2.isBlack() and line3.isBlack()
       
        
    def onBars(self, bars):
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__position is None:
            if self.buySignal(bars):
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares, True)
        elif not self.__position.exitActive() and self.sellSignal(bars):
            self.__position.exitMarket()
            
    
    
