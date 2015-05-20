from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
import sma_crossover
import rsi
import threelines
import highlow

# Load the yahoo feed from the CSV file
feed = yahoofeed.Feed()
feed.addBarsFromCSV("orcl", "orcl-2000.csv")

# Evaluate the strategy with the feed's bars.
# myStrategy = sma_crossover.SMACrossOver(feed, "orcl", 20)

rsiPeriod = 5

entrySMA = 20
exitSMA = 5

# myStrategy = rsi.RSI(feed, "orcl", rsiPeriod,entrySMA,exitSMA)
#myStrategy = threelines.threelines(feed,"orcl")
myStrategy = highlow.highlow(feed, "orcl", 30, 30)
# Attach a returns analyzers to the strategy.
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy, True, True, True)
# plt.getInstrumentSubplot("orcl").addDataSeries("Entry SMA", myStrategy.getEntrySMA())
# plt.getInstrumentSubplot("orcl").addDataSeries("Exit SMA", myStrategy.getExitSMA())
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
# plt.getInstrumentSubplot("orcl").addDataSeries("SMA", myStrategy.getSMA())
# plt.getInstrumentSubplot("orcl").addDataSeries("RSI", myStrategy.getRSI())
# Plot the simple returns on each bar.
# plt.getOrCreateSubplot("rsi").addDataSeries("RSI", myStrategy.getRSI())


# plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())


# Run the strategy.
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

# Plot the strategy.
plt.plot()
