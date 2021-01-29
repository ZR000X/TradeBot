from decimal import Decimal
from binance.client import Client
from binance.exceptions import BinanceAPIException
from python.speaker import Speaker

class TradeInstruction:
    def __init__(self, symbol:str, tradeAmount:float, client:Client, spkr:Speaker):
        self.symbol = symbol
        self.tradeAmount = tradeAmount # amount to increase asset by, if neg, then sell
        self.client = client
        self.spkr = spkr
        self.spkr.say("Initialising a tradebot to trade "+symbol+"...")
    
    def formatTradeAmount(self, symbol:str, tradeAmount:float) -> Decimal:
        self.spkr.say("Formatting the trade for symbol "+symbol+" of amount "+str(tradeAmount)+"...")
        stepSize = Decimal(self.client.get_symbol_info(symbol)['filters'][2]['stepSize'])
        lotSize = Decimal(self.client.get_symbol_info(symbol)['filters'][2]['stepSize'])
        toReturn = Decimal(int(Decimal(abs(tradeAmount))/stepSize))*stepSize
        toReturn = Decimal(toReturn).normalize()
        return toReturn

    def sayMarketTrade(self):
        formattedTradeAmount = self.formatTradeAmount(self.symbol, self.tradeAmount)
        if formattedTradeAmount > 0:
            if self.tradeAmount < 0:
                self.spkr.say("Would now be SELLING "+self.symbol+" of amount "+ \
                    str(formattedTradeAmount))
            else:
                self.spkr.say("Would now be BUYING "+self.symbol+" of amount "+ \
                    str(formattedTradeAmount)) 
        else:
            self.spkr.say("The amount of "+self.symbol+", which is "+str(self.tradeAmount)+" requested to be traded is too low..")

    def executeMarketTrade(self): 
        formattedTradeAmount = self.formatTradeAmount(self.symbol, self.tradeAmount)
        if formattedTradeAmount > 0:
            if self.tradeAmount < 0:
                self.spkr.say("SELLING "+self.symbol+" of amount "+str(self.formatTradeAmount(self.tradeAmount)))
                order = self.client.order_market_sell(
                    symbol=self.symbol,
                    quantity=formattedTradeAmount
                )
            else:
                self.spkr.say("BUYING "+self.symbol+" of amount "+str(self.formatTradeAmount(self.tradeAmount)))
                order = self.client.order_market_buy(
                    symbol=self.symbol,
                    quantity=formattedTradeAmount
                )
        else:
            self.spkr.say("The amount of "+self.symbol+", which is "+str(self.tradeAmount)+" requested to be traded is too low..")

