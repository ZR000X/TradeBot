from python.tradeInstruction import TradeInstruction
from python.dataBot import DataBot
from python.speaker import Speaker
from binance.client import Client

class RebalanceBot:

    def __init__(self, client:Client, sigdiff:float, numsecs:int, spkr:Speaker, test:bool):
        spkr.say("Initialising the Rebalance Bot...")
        
        self.client = client
        self.spkr = spkr
        self.dataBot = DataBot(client, spkr)
        self.test = test

        self.sigdiff = sigdiff
        self.numsecs = numsecs

        # These system variables must be added using the methods
        self.tickers = []
        self.symbols = {}
        self.allocations = {}
        self.priorities = {}
        self.tickersOutOfBalance = {}
        self.tradeInstructions = []

        # These variables are calculated
        self.holdings = {}
        self.quotes = {}
        self.values = {}
        self.totalPortfolioValue = 0

    ### THESE METHODS ARE MAINTENAINCE

    def addTickerPlusData(self, ticker:str, symbol:str, allocation:float, priority:int):
        self.spkr.say("Adding the ticker: "+ticker+"...")
        self.tickers.append(ticker)
        self.spkr.say("...which has symbol "+symbol)
        self.symbols[ticker] = symbol
        self.spkr.say("...and has allocation "+str(allocation))
        self.allocations[ticker] = allocation
        self.spkr.say("...and has priority "+str(priority))
        self.priorities[ticker] = priority
    
    def hasTicker(self, ticker:str) -> bool:
        if ticker in self.tickers:
            return True
        else:
            return False
    
    def checkAllocationsFit(self) -> bool:
        sumOfAllocations = 0
        for ticker in self.tickers:
            sumOfAllocations = sumOfAllocations + self.allocations[ticker]
        if abs(sumOfAllocations - 1) < 0.0001: #Only off by 0.01% maximum
            return True
        return False
    
    ## THESE METHODS WILL BE THE ACTION METHODS: UPDATING THE DATA
    
    def updateTotalAssetBalances(self):
        for ticker in self.tickers:
            self.holdings[ticker] = self.dataBot.getTotalAssetBalance(ticker)

    def updateQuotes(self):
        for ticker in self.tickers:
            if ticker=="ZAR":
                self.quotes["ZAR"] = 1
            elif ticker=="BTC":
                self.quotes["BTC"] = self.dataBot.getQuote("BTCZAR")                    
            else:
                self.quotes[ticker] = self.quotes["BTC"]*self.dataBot.getQuote(self.symbols[ticker])  
    
    def updateValues(self):
        for ticker in self.tickers:
            self.values[ticker] = self.holdings[ticker]*self.quotes[ticker]

    def updateTotalPortfolioValue(self):
        self.totalPortfolioValue = 0
        for ticker in self.tickers:
            self.totalPortfolioValue = self.totalPortfolioValue + self.values[ticker]
    
    def getTotalPortfolioValue(self) -> float:
        return self.totalPortfolioValue
    
    def getNewTotalPortfolioValue(self) -> float:
        self.updateTotalPortfolioValue()
        return self.totalPortfolioValue
   
    def updateTickersOutOfBalance(self):
        self.updateTotalPortfolioValue()
        for ticker in self.tickers:
            if abs(self.values[ticker]/self.totalPortfolioValue - self.allocations[ticker]) > self.sigdiff:
                self.tickersOutOfBalance[ticker] = self.values[ticker]/self.totalPortfolioValue - self.allocations[ticker]
    
    def getMaxPriorityOutOfBalance(self):
        toReturn = 0
        for ticker in self.tickers:
            if ticker in self.tickersOutOfBalance:
                if self.priorities[ticker] > toReturn:
                    toReturn = self.priorities[ticker]
        return toReturn
        
    def updateTradeInstructions(self):
        self.tradeInstructions = []
        maxPriority = self.getMaxPriorityOutOfBalance()
        for ticker in self.tickers:
            if ticker in self.tickersOutOfBalance:
                if self.priorities[ticker] == maxPriority:
                    self.tradeInstructions.append(TradeInstruction(self.symbols[ticker],  \
                        self.tickersOutOfBalance[ticker], self.client, self.spkr))

    def updateEntirePortfolio(self):
        self.updateTotalAssetBalances()
        self.updateQuotes()
        self.updateValues()
        self.updateTickersOutOfBalance()
        self.updateTradeInstructions()

    def balancePortfolio(self):
        self.updateEntirePortfolio()
        for tradeInstruction in self.tradeInstructions:
            if self.test:
                tradeInstruction.sayMarketTrade()
            else:
                tradeInstruction.executeMarketTrade()
