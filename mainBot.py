import datetime, config, time
from binance.enums import *
from binance.exceptions import BinanceAPIException
from python.speaker import Speaker
from python.dataBot import DataBot

# client = Client(config.API_KEY, config.API_SECRET)
spkr = Speaker("output/None")
dataBot = DataBot(config.API_KEY, config.API_SECRET, spkr)

def sgn(number):
    sgn = number / abs(number)

## Helper method to format and perform trades
def trade(ticker,tradeAmount):
    try:
        formattedTrade = dataBot.formatTrade(config.PAIRS[ticker], float(tradeAmount))        
        if tradeAmount < 0:            
            dataBot.marketSell(config.PAIRS[ticker], formattedTrade)
        else:
            dataBot.marketBuy(config.PAIRS[ticker], formattedTrade)
    except BinanceAPIException as e:
        spkr.say(e.status_code)
        spkr.say(e.message)

## CORE PROGRAM OPERATION LOOP
while True:
    ## Reset data
    HOLDINGS = {}
    PRICES = {}
    VALUES = {}
    PERCENTAGES = {}
    DEVIATIONS = {}
    TO_TRADE = []
    
    ## set up a new speaker  
    now = str(datetime.datetime.now()).replace('.','_') \
        .replace(' ','_').replace(':','-')[:19]
    output_filename = "output/"+now+".txt"    
    spkr = Speaker(output_filename)
    spkr.say("Completed speaker setup"); spkr.say("\n"); spkr.say('')

    dataBot = DataBot(config.API_KEY, config.API_SECRET, spkr)
    
    ## Load in the allocations and print priorities
    sum_of_allocations = 0
    for ticker,alloc in config.ALLOCATIONS.items():
        sum_of_allocations = sum_of_allocations + float(alloc)
    spkr.say("The Total Set Allocations sum to (Should be 1.0) is "+str(sum_of_allocations))
    spkr.say("TICKERS:"+str(config.TICKERS)); spkr.say("PAIRS:"+str(config.PAIRS)); spkr.say("ALLOCATIONS:"+str(config.ALLOCATIONS))
    spkr.say('PRIORITIES:'); spkr.say(config.PRIORITIES); spkr.say('')
    
    ## Download New data from Binance and update            
    for ticker in config.TICKERS:
        HOLDINGS[str(ticker)] = dataBot.getTotalAssetBalance(str(ticker))
    for ticker in config.TICKERS:
        if ticker=='ZAR':
            PRICES['ZAR'] = 1
        elif ticker=='BTC':
            PRICES['BTC'] = dataBot.getQuote("BTCZAR")                    
        else:
            PRICES[ticker] = PRICES['BTC']*dataBot.getQuote(config.PAIRS[ticker])       

    ## Calculate the values, percentages and deviations
    total_portfolio_value = 0
    for ticker in config.TICKERS:
        VALUES[ticker] = HOLDINGS[ticker]*PRICES[ticker]
        total_portfolio_value = total_portfolio_value + VALUES[ticker]
    spkr.say("VALUES: "); spkr.say(VALUES); spkr.say("TOTAL VALUE: "+str(total_portfolio_value)); spkr.say('')
    total_shares = 0
    total_differences = 0
    for ticker in config.TICKERS:
        PERCENTAGES[ticker] = VALUES[ticker]/total_portfolio_value
        total_shares = total_shares + PERCENTAGES[ticker]
        DEVIATIONS[ticker] = PERCENTAGES[ticker]-config.ALLOCATIONS[ticker]  
        total_differences = total_differences + DEVIATIONS[ticker]
    spkr.say("PERCENTAGES: "+str(PERCENTAGES)); spkr.say("DEVIATIONS: "+str(DEVIATIONS)); \
        spkr.say("SUM OF DEVIATION (Should be 0): "+str(total_differences)); spkr.say('\n')
    
    ## Determine what should be traded and perform the trades
    for ticker in config.TICKERS:
        if float(abs(DEVIATIONS[ticker])) >= float(config.SIGDIFF) and ticker != 'ZAR':
            TO_TRADE.append(ticker)
    spkr.say("The symbols to trade are now: "+str(TO_TRADE))
    max_priority = 0
    for ticker in TO_TRADE:
        if config.PRIORITIES[ticker] > max_priority:
            max_priority = int(config.PRIORITIES[ticker])
    spkr.say("Max Priority present in sufficiently different assets is: "+str(max_priority))
    if max_priority == 0:
        spkr.say("There are no trades to be done... But...")
        if float(DEVIATIONS['ZAR']) >= float(config.SIGDIFF) and DEVIATIONS['BTC']<0:
            spkr.say("We'll buy some BTC to balance ZAR")
            trade('BTC',sgn(float(DEVIATIONS['ZAR']))*float(config.SIGDIFF)*total_portfolio_value/PRICES['BTC'])
        else:
            spkr.say("Yeah, no, nothing")
    elif max_priority == 1:
        spkr.say("Only BTC needs to be traded, with a value "+str(DEVIATIONS['BTC']*total_portfolio_value))
        trade('BTC',float(-DEVIATIONS['BTC']*total_portfolio_value/PRICES['BTC']))
    else: 
        spkr.say("There are Altcoins to be traded...")
        if 'BTC' in TO_TRADE:
            TO_TRADE.remove('BTC')
        for ticker in TO_TRADE:
            spkr.say(ticker+" needs to be traded, with a value "+str(DEVIATIONS[ticker]*total_portfolio_value/PRICES['BTC'])+" BTC")
            trade(ticker,-float(DEVIATIONS[ticker]*total_portfolio_value/PRICES[ticker]))

    ## End off the loop    
    spkr.say("That is the end of the rebalancing at time "+now)
        
    for x in range (0,config.NUM_SECS):  
        b = "Waiting "+str(x)+"/"+str(config.NUM_SECS)+" secs before next check..."
        print (b, end="\r")
        time.sleep(1)