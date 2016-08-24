import random
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma

"""
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 1000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.last_10_diffs = []
    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

"""

class MyStrat2(strategy.BacktestingStrategy):

    def __init__(self,feed,instrument,news):
        super(MyStrat2, self).__init__(feed, 1000)
        self.__position = None
        self.__instrument = instrument
        self.news = news

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None
    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        news = self.news.next()
        bar = bars[self.__instrument]
        instrument = self.__instrument
        if news is None:
            return
        if self.__position is None:
            if command_from_news(instrument,news)[0] == 'buy':
                self.__position = self.enterLong(self.__instrument, command_from_news(instrument,news)[1], True)

        elif command_from_news(instrument,news)[0] == 'sell' and not self.__position.exitActive():
            self.__position.exitMarket()


def command_from_news(instrument,news):
    if news[instrument] == 'g':
        return ('buy',10)
    if news[instrument] == 'vg':
        return ('buy', 10)
    if news[instrument] in ('b','vb') :
        return ('sell', None)



def run_strategy2(news):
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("msft", "C:\Users\Yoav\PycharmProjects\TLDR\Data\data_msft_2010_2012.csv")

    # Evaluate the strategy with the feed.
    myStrategy = MyStrat2(feed, "msft", news)
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()
"""
def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("msft", "C:\Users\Yoav\PycharmProjects\TLDR\Data\data_msft_2010_2012.csv")

    # Evaluate the strategy with the feed.
    myStrategy = MyStrat2(feed, "msft", smaPeriod)
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()
"""
def news_gen():
    while True:
        n = random.choice(['g','vg','b','vb'])
        yield {'msft':n}


run_strategy2(news_gen())
