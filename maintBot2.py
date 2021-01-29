import datetime, config, time, csv
from python.rebalanceBot import RebalanceBot
from decimal import Decimal
from binance.enums import * 
from binance.client import Client
from binance.exceptions import BinanceAPIException
from python.speaker import Speaker
from python.dataBot import DataBot

# client = Client(config.API_KEY, config.API_SECRET)
## set up a new speaker  
def setupNowSpeaker() -> Speaker:
    now = str(datetime.datetime.now()).replace('.','_') \
        .replace(' ','_').replace(':','-')[:19]
    output_filename = "output/"+now+".txt"    
    return Speaker(output_filename)

SIGDIFF = 0.01
NUM_SECS = 300
TICKERS = ['ZAR', 'BTC', 'ETH', 'LTC', 'COMP', 'THETA', 'LINK', 'GRT']

PAIRS = {  
    'ZAR': '',
    'BTC': 'BTCZAR',
    'ETH': 'ETHBTC',
    'LTC': 'LTCBTC',
    'COMP': 'COMPBTC',
    'THETA': 'THETABTC',
    'LINK': 'LINKBTC',
    'GRT': 'GRTBTC'
}
ALLOCATIONS = {
    'ZAR': 0.04,
    'BTC': 0.30,
    'ETH': 0.30,
    'LTC': 0.20,
    'COMP': 0.04,
    'THETA': 0.04,
    'LINK': 0.04,
    'GRT': 0.04
}
PRIORITIES = {
    'ZAR': 0,
    'BTC': 1,
    'ETH': 2,
    'LTC': 2,
    'COMP': 2,
    'THETA': 2,
    'LINK': 2,
    'GRT': 2
}

## CORE PROGRAM OPERATION LOOP
while True:
    ## Setup New Rebalance Bot
    client = Client(config.API_KEY, config.API_SECRET)
    spkr = setupNowSpeaker()
    rebalanceBot = RebalanceBot(client, SIGDIFF, NUM_SECS, spkr, True)

    for ticker in TICKERS:
        rebalanceBot.addTickerPlusData(ticker, PAIRS[ticker], ALLOCATIONS[ticker], PRIORITIES[ticker])

    rebalanceBot.balancePortfolio()