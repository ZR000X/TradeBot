# import websocket, numpy
import datetime, config, csv
from decimal import Decimal
from binance.enums import * 
from binance.client import Client
from binance.exceptions import BinanceAPIException
from python.speaker import Speaker

client = Client(config.API_KEY, config.API_SECRET)

## Helper method to format and perform trades
def trade(ticker,amount_of_it_to_change):
    try:
        stepSize = Decimal(client.get_symbol_info(config.PAIRS[ticker])['filters'][2]['stepSize'])
        amount_of_it_to_change_FORMATTED = Decimal(int(Decimal(abs(amount_of_it_to_change))/stepSize))*stepSize
        amount_of_it_to_change_FORMATTED = Decimal(amount_of_it_to_change_FORMATTED).normalize()
        
        if amount_of_it_to_change < 0:
            spkr.say("NOW Selling "+ticker+" by "+str(amount_of_it_to_change_FORMATTED))
            order = client.order_market_sell(
                symbol=config.PAIRS[symbol],
                quantity=amount_of_it_to_change_FORMATTED
            )
        else:
            spkr.say("NOW Buying "+ticker+" by "+str(amount_of_it_to_change_FORMATTED))
            order = client.order_market_buy(
                symbol=config.PAIRS[symbol],
                quantity=amount_of_it_to_change_FORMATTED
            )
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
    
    ## Load in the allocations and print priorities
    sum_of_allocations = 0
    for symbol,alloc in config.ALLOCATIONS.items():
        sum_of_allocations = sum_of_allocations + float(alloc)
    spkr.say("The Total Set Allocations sum to (Should be 1.0) is "+str(sum_of_allocations))
    spkr.say("TICKERS:"+str(config.TICKERS)); spkr.say("PAIRS:"+str(config.PAIRS)); spkr.say("ALLOCATIONS:"+str(config.ALLOCATIONS))
    spkr.say('Oh, and the PRIORITIES are:'); spkr.say(config.PRIORITIES); spkr.say('')
    
    ## Download New data from Binance and update
    download_successful = False
    while download_successful == False:
        try:
            for symbol in config.TICKERS:
                HOLDINGS[symbol] = float(client.get_asset_balance(asset=symbol)['free']) \
                    + float(client.get_asset_balance(asset=symbol)['locked'])
            spkr.say("HOLDINGS:"); spkr.say(HOLDINGS); spkr.say("\n")
            for symbol in config.TICKERS:
                if symbol=='ZAR':
                    PRICES['ZAR'] = 1
                elif symbol=='BTC':
                    PRICES['BTC'] = None
                    while PRICES['BTC'] is None:
                        try:
                            PRICES['BTC'] = float(client.get_historical_klines('BTCZAR', Client.KLINE_INTERVAL_1MINUTE, "1 minutes ago UTC")[0][4])
                        except:
                            spkr.say("Out of bounds error, retrying...")
                            pass
                else:
                    PRICES[symbol] = None
                    while PRICES[symbol] is None:
                        try:
                            PRICES[symbol] = PRICES['BTC']*float(client.get_historical_klines(config.PAIRS[symbol], Client.KLINE_INTERVAL_1MINUTE, "1 minutes ago UTC")[0][4])
                        except:
                            spkr.say("Out of bounds error, retrying...")
                            pass
            spkr.say("PRICES: "); spkr.say(PRICES); spkr.say('\n')
            download_successful = True
        except:
            spkr.say("Problem with downloading data... Retrying...")
            continue

    ## Calculate the values, percentages and deviations
    total_portfolio_value = 0
    for symbol in config.TICKERS:
        VALUES[symbol] = HOLDINGS[symbol]*PRICES[symbol]
        total_portfolio_value = total_portfolio_value + VALUES[symbol]
    spkr.say("VALUES: "); spkr.say(VALUES); spkr.say("TOTAL VALUE: "+str(total_portfolio_value)); spkr.say('')
    total_shares = 0
    total_differences = 0
    for symbol in config.TICKERS:
        PERCENTAGES[symbol] = VALUES[symbol]/total_portfolio_value
        total_shares = total_shares + PERCENTAGES[symbol]
        DEVIATIONS[symbol] = PERCENTAGES[symbol]-config.ALLOCATIONS[symbol]  
        total_differences = total_differences + DEVIATIONS[symbol]
    spkr.say("PERCENTAGES: "+str(PERCENTAGES)); spkr.say("DEVIATIONS: "+str(DEVIATIONS)); \
        spkr.say("SUM OF DEVIATION (Should be 0): "+str(total_differences)); spkr.say('\n')
    
    ## Determine what should be traded and perform the trades
    for symbol in config.TICKERS:
        if float(abs(DEVIATIONS[symbol])) >= float(config.SIGDIFF) and symbol != 'ZAR':
            TO_TRADE.append(symbol)
    spkr.say("The symbols to trade are now: "+str(TO_TRADE))
    max_priority = 0
    for symbol in TO_TRADE:
        if config.PRIORITIES[symbol] > max_priority:
            max_priority = int(config.PRIORITIES[symbol])
    spkr.say("Max Priority present in sufficiently different assets is: "+str(max_priority))
    if max_priority == 0:
        spkr.say("There are no trades to be done... But...")
        if float(DEVIATIONS['ZAR']) >= float(config.SIGDIFF) and DEVIATIONS['BTC']<0:
            spkr.say("We'll buy some BTC to balance ZAR")
            trade('BTC',float(DEVIATIONS['ZAR']*total_portfolio_value/PRICES['BTC']))
        else:
            spkr.say("Yeah, no, nothing")
    elif max_priority == 1:
        spkr.say("Only BTC needs to be traded, with a value "+str(DEVIATIONS['BTC']*total_portfolio_value))
        trade('BTC',float(-DEVIATIONS['BTC']*total_portfolio_value/PRICES['BTC']))
    else: 
        spkr.say("There are Altcoins to be traded...")
        if 'BTC' in TO_TRADE:
            TO_TRADE.remove('BTC')
        for symbol in TO_TRADE:
            spkr.say(symbol+" needs to be traded, with a value "+str(DEVIATIONS[symbol]*total_portfolio_value/PRICES['BTC'])+" BTC")
            trade(symbol,-float(DEVIATIONS[symbol]*total_portfolio_value/PRICES[symbol]))

    ## End off the loop    
    spkr.say("That is the end of the rebalancing at time "+now)