from binance.enums import * 
from binance.client import Client
from binance.exceptions import BinanceAPIException
from python.speaker import Speaker
from decimal import Decimal

## A Bot to fetch data from Binance API
class DataBot:
    ## Initialise the bot with the reporting
    def __init__(self, client:Client, spkr: Speaker):
        self.client = client
        self.speaking = True
        self.spkr = spkr

    ## fetch the current amount I hold from Binance
    def getTotalAssetBalance(self, symbol: str) -> float: 
        self.speak("Getting Total Asset Balance for "+symbol+"...")
        toReturn = None    
        success = False        
        while success == False:
            try:
                toReturn = float(self.client.get_asset_balance(asset=symbol)['free']) \
            + float(self.client.get_asset_balance(asset=symbol)['locked'])
                success = True           
            except BinanceAPIException as e:
                self.speak(e.status_code)
                self.speak(e.message)
                self.speak("Problem downloading Holding data for "+symbol+"... Retrying")
                continue
        self.speak("...which is "+str(toReturn))
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
        self.speak("...which is "+str(toReturn))
        return toReturn

    ## A method to format the trade amount
    def formatTrade(self, symbol: str, tradeAmount: float) -> float:
        stepSize = Decimal(self.client.get_symbol_info(symbol)['filters'][2]['stepSize'])
        toReturn = Decimal(int(Decimal(abs(tradeAmount))/stepSize))*stepSize
        toReturn = Decimal(toReturn).normalize()
        return toReturn

    ## Report what the bot is doing using the Speaker class
    def speak(self, words):
        if self.speaking == True:
            self.spkr.say(words)