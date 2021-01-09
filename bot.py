# import websocket, numpy
import json, datetime, config, csv, pprint
from decimal import Decimal
from binance.enums import * 
from binance.client import Client
from binance.exceptions import BinanceAPIException

client = Client(config.API_KEY, config.API_SECRET)
pp = pprint.PrettyPrinter(indent=4)

def say(words, writer):
    pp.pprint(words)
    writer.writerow([words])

###QUANTITY REFERS TO HOW MUCH OF THE FIRST CURRENCY IS BEING BOUGHT/SOLD FOR THE SECOND
def trade(ticker,amount_of_it_to_change):
    try:
        stepSize = Decimal(client.get_symbol_info(config.PAIRS[ticker])['filters'][2]['stepSize'])
        amount_of_it_to_change_FORMATTED = Decimal(int(Decimal(abs(amount_of_it_to_change))/stepSize))*stepSize
        amount_of_it_to_change_FORMATTED = Decimal(amount_of_it_to_change_FORMATTED).normalize()
        
        if amount_of_it_to_change < 0:
            say("NOW Selling "+ticker+" by "+str(amount_of_it_to_change_FORMATTED),csvWriter)
            order = client.order_market_sell(
                symbol=config.PAIRS[symbol],
                quantity=amount_of_it_to_change_FORMATTED
            )
        else:
            say("NOW Buying "+ticker+" by "+str(amount_of_it_to_change_FORMATTED),csvWriter)
            order = client.order_market_buy(
                symbol=config.PAIRS[symbol],
                quantity=amount_of_it_to_change_FORMATTED
            )
    except BinanceAPIException as e:
        say(e.status_code,csvWriter)
        say(e.message,csvWriter)
    
while True:
    try:
        ## create new file for this exact time
        now = str(datetime.datetime.now()).replace('.','_').replace(' ','_').replace(':','_')
        csvfile = open("output\\"+str(now)+".csv", 'w', newline='')
        csvWriter = csv.writer(csvfile, delimiter='_')

        say("Summing up the allocation settings:", csvWriter)
        sum_of_allocations = 0
        for symbol,alloc in config.ALLOCATIONS.items():
            sum_of_allocations = sum_of_allocations + float(alloc)
        say("The Total Set Allocations sum to (Should be 1.0)"+str(sum_of_allocations),csvWriter)
        say('',csvWriter); say("TICKERS:"+str(config.TICKERS),csvWriter); say("PAIRS:"+str(config.PAIRS),csvWriter); say("ALLOCATIONS:"+str(config.ALLOCATIONS),csvWriter)
        say('Oh, and the PRIORITIES are:'+str(config.PRIORITIES),csvWriter)
        
        #OTHER DATA DECLARED HERE
        HOLDINGS = {}
        PRICES = {}
        VALUES = {}
        PERCENTAGES = {}
        DEVIATIONS = {}
        TO_TRADE = []

        say("NOW reading Asset Holdings for these tickers...",csvWriter)
        for symbol in config.TICKERS:
            HOLDINGS[symbol] = float(client.get_asset_balance(asset=symbol)['free']) \
                + float(client.get_asset_balance(asset=symbol)['locked'])
        say("HOLDINGS:"+str(HOLDINGS),csvWriter); say('',csvWriter)

        say("NOW getting the prices (ZAR) for these assets in the last minute",csvWriter)
        for symbol in config.TICKERS:
            if symbol=='ZAR':
                PRICES['ZAR'] = 1
            elif symbol=='BTC':
                PRICES['BTC'] = None
                while PRICES['BTC'] is None:
                    try:
                        PRICES['BTC'] = float(client.get_historical_klines('BTCZAR', Client.KLINE_INTERVAL_1MINUTE, "1 minutes ago UTC")[0][4])
                    except:
                        say("Out of bounds error, retrying...",csvWriter)
                        pass
            else:
                PRICES[symbol] = None
                while PRICES[symbol] is None:
                    try:
                        PRICES[symbol] = PRICES['BTC']*float(client.get_historical_klines(config.PAIRS[symbol], Client.KLINE_INTERVAL_1MINUTE, "1 minutes ago UTC")[0][4])
                    except:
                        say("Out of bounds error, retrying...",csvWriter)
                        pass
        say("PRICES:"+str(PRICES),csvWriter); say('',csvWriter)

        say("NOW calculated the values (ZAR) of each asset",csvWriter)
        total_portfolio_value = 0
        for symbol in config.TICKERS:
            VALUES[symbol] = HOLDINGS[symbol]*PRICES[symbol]
            total_portfolio_value = total_portfolio_value + VALUES[symbol]
        say("VALUES: "+str(VALUES),csvWriter); say("TOTAL VALUE: "+str(total_portfolio_value),csvWriter); say('',csvWriter)

        say("NOW calculating the percentages (%) of each asset of the portfolio and the difference to the allocations",csvWriter)
        total_shares = 0
        total_differences = 0
        for symbol in config.TICKERS:
            PERCENTAGES[symbol] = VALUES[symbol]/total_portfolio_value
            total_shares = total_shares + PERCENTAGES[symbol]
            DEVIATIONS[symbol] = PERCENTAGES[symbol]-config.ALLOCATIONS[symbol]  
            total_differences = total_differences + DEVIATIONS[symbol]
        say("PERCENTAGES: "+str(PERCENTAGES),csvWriter); say("DEVIATIONS: "+str(DEVIATIONS),csvWriter); \
            say("SUM OF DEVIATION (Should be 0): "+str(total_differences),csvWriter); say('',csvWriter)

        say("NOW determining which symbols are significantly different to trade"+str(config.SIGDIFF),csvWriter)
        for symbol in config.TICKERS:
            if float(abs(DEVIATIONS[symbol])) >= float(config.SIGDIFF) and symbol != 'ZAR':
                TO_TRADE.append(symbol)
        say("The symbols to trade are now: "+str(TO_TRADE),csvWriter)

        say("NOW we are going to check if we are at priority level 2 or 1 or neither",csvWriter)
        max_priority = 0
        for symbol in TO_TRADE:
            if config.PRIORITIES[symbol] > max_priority:
                max_priority = int(config.PRIORITIES[symbol])
        say("Max Priority present in sufficiently different assets is: "+str(max_priority),csvWriter)

        if max_priority == 0:
            say("There are no trades to be done... But...",csvWriter)
            if float(DEVIATIONS['ZAR']) >= float(config.SIGDIFF) and DEVIATIONS['BTC']<0:
                say("We'll buy some BTC to balance ZAR",csvWriter)
                trade('BTC',float(DEVIATIONS['ZAR']*total_portfolio_value/PRICES['BTC']))
            else:
                say("Yeah, no, nothing",csvWriter)
        elif max_priority == 1:
            say("Only BTC needs to be traded, with a value "+str(DEVIATIONS['BTC']*total_portfolio_value),csvWriter)
            trade('BTC',float(-DEVIATIONS['BTC']*total_portfolio_value/PRICES['BTC']))
        else: 
            say("There are Altcoins to be traded...",csvWriter)
            if 'BTC' in TO_TRADE:
                TO_TRADE.remove('BTC')
            for symbol in TO_TRADE:
                say(symbol+" needs to be traded, with a value "+str(DEVIATIONS[symbol]*total_portfolio_value/PRICES['BTC'])+" BTC",csvWriter)
                trade(symbol,-float(DEVIATIONS[symbol]*total_portfolio_value/PRICES[symbol]))
        # while current trades are not empty, get trades, then clear trades pending and trades approved
    except:
        continue