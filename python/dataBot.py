from binance.enums import * 
from binance.client import Client
from binance.exceptions import BinanceAPIException
from python.speaker import Speaker
from decimal import Decimal

## A Bot to fetch data from Binance API
class DataBot:

    ## Initiate the bot without the reporting
    # def __init__(self, api_key, api_sec):
    #     self.api_key = api_key
    #     self.api_sec = api_sec
    #     self.client = Client(api_key, api_sec)
    #     self.speaking = False
    #     self.spkr = None
    
    ## Initialise the bot with the reporting
    # def __init__(self, api_key: str, api_sec: str, file: FileIO):
    #     self.api_key = api_key
    #     self.api_sec = api_sec
    #     self.client = Client(api_key, api_sec)
    #     self.speaking = True
    #     self.spkr = Speaker(file)

    ## Initialise the bot with the reporting
    def __init__(self, api_key: str, api_sec: str, spkr: Speaker):
        self.api_key = api_key
        self.api_sec = api_sec
        self.client = Client(api_key, api_sec)
        self.speaking = True
        self.spkr = spkr

    ## fetch the current amount I hold from Binance
    def getTotalAssetBalance(self, symbol: str) -> float: 
        self.speak("Getting Total Asset Balance for "+symbol)
        toReturn = None    
        success = False        
        while success == False:
            try:
                toReturn = float(self.client.get_asset_balance(asset=symbol)['free']) \
            + float(self.client.get_asset_balance(asset=symbol)['locked'])
                success = True
            except:
                self.speak("Problem downloading Holding data for "+symbol+"... Retrying")
                continue                
        return toReturn 
    
    ## fetch the latest price for the supplied symbol from Binance API
    def getQuote(self, symbol: str) -> float: 
        self.speak("Getting Recent Quote for "+symbol)
        toReturn = None 
        success = False        
        while success == False:
            try:
                toReturn = float(self.client.get_historical_klines \
            (symbol, Client.KLINE_INTERVAL_1MINUTE, "1 minutes ago UTC")[0][4])
                success = True
            except:
                self.speak("Problem downloading Price data for "+symbol+"... Retrying")
                continue                
        return toReturn

    def formatTrade(self, symbol: str, tradeAmount: float) ->float:
        stepSize = Decimal(self.client.get_symbol_info(symbol)['filters'][2]['stepSize'])
        toReturn = Decimal(int(Decimal(abs(tradeAmount))/stepSize))*stepSize
        toReturn = Decimal(toReturn).normalize()
        return float(toReturn)

    def marketSell(self, symbol, formattedTrade):
        self.speak("NOW Selling "+symbol+" by "+str(formattedTrade))
        # order = self.client.order_market_sell(
        #         symbol=symbol,
        #         quantity=formattedTrade
        #     )

    def marketBuy(self, symbol, formattedTrade):
        self.speak("NOW Buying "+symbol+" by "+str(formattedTrade))
        # order = self.client.order_market_buy(
        #         symbol=symbol,
        #         quantity=formattedTrade
        #     )

    ## Report what the bot is doing using the Speaker class
    def speak(self, words):
        if self.speaking == True:
            self.spkr.say(words)