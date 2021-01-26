## TradeBot
Welcome to TradeBot!

Using the python-binance package (documentation: https://python-binance.readthedocs.io/en/latest/), we are developing an easy-to-use rebalancing bot.

The Bot will:
1.) Load the user-set system-parameters.
2.) Load the price and balance data from Binance.
3.) Calculate the value of each holding, and its percentage of the total value.
4.) Use the parameters to calculate discrepencies between current allocations of value per asset and user-set allocations.
5.) Build trades out of these discrepencies, should they meet certain user-set and Binance-set requirements.
6.) Perform the trades to rebalance the portfolio.
7.) Repeat continuously, so can be left running throughout the day.

# Install dependencies
python -m pip install --upgrade pip
pip install python-binance
pip install wscat
# Links
https://python-binance.readthedocs.io/en/latest/
https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
# How to Run
Simply run the mainBot python file in cmd. Be sure to tweak the config file!

## EXAMPLE OUTPUT:
** Note: The current state of the projects only requires the two Python files to operate. But it expects and 'output' folder to be present to drop the output csv files.
Here is an example of what an output csv file currently looks like:

"'Completed speaker setup'"
'\n'
''
"'The Total Set Allocations sum to (Should be 1.0) is 1.0'"
"""TICKERS:['ZAR', 'BTC', 'ETH', 'LTC', 'COMP', 'THETA', 'LINK', 'GRT']"""
"(""PAIRS:{'ZAR': '', 'BTC': 'BTCZAR', 'ETH': 'ETHBTC', 'LTC': 'LTCBTC', 'COMP': ""
 ""'COMPBTC', 'THETA': 'THETABTC', 'LINK': 'LINKBTC', 'GRT': 'GRTBTC'}"")"
"(""ALLOCATIONS:{'ZAR': 0.04, 'BTC': 0.3, 'ETH': 0.3, 'LTC': 0.2, 'COMP': 0.04, ""
 ""'THETA': 0.04, 'LINK': 0.04, 'GRT': 0.04}"")"
'PRIORITIES:'
"{   'BTC': 1,
    'COMP': 2,
    'ETH': 2,
    'GRT': 2,
    'LINK': 2,
    'LTC': 2,
    'THETA': 2,
    'ZAR': 0}"
''
"'Getting Total Asset Balance for ZAR'"
"'Getting Total Asset Balance for BTC'"
"'Getting Total Asset Balance for ETH'"
"'Getting Total Asset Balance for LTC'"
"'Getting Total Asset Balance for COMP'"
"'Getting Total Asset Balance for THETA'"
"'Getting Total Asset Balance for LINK'"
"'Getting Total Asset Balance for GRT'"
"'Getting Recent Quote for BTCZAR'"
"'Getting Recent Quote for ETHBTC'"
"'Getting Recent Quote for LTCBTC'"
"'Getting Recent Quote for COMPBTC'"
"'Getting Recent Quote for THETABTC'"
"'Getting Recent Quote for LINKBTC'"
"'Getting Recent Quote for GRTBTC'"
"'VALUES: '"
"{   'BTC': 2991.9185766399996,
    'COMP': 358.14906655248,
    'ETH': 3297.126144331589,
    'GRT': 571.3441369664,
    'LINK': 668.3879146228704,
    'LTC': 1932.1813918953146,
    'THETA': 337.9211005632,
    'ZAR': 357.79128617}"
"'TOTAL VALUE: 10514.819617741852'"
''
"(""PERCENTAGES: {'ZAR': 0.034027334674033974, 'BTC': 0.2845430245509566, 'ETH': ""
 ""0.3135694442887338, 'LTC': 0.18375792092858242, 'COMP': ""
 ""0.034061360971724935, 'THETA': 0.03213760319701723, 'LINK': ""
 ""0.06356627492639882, 'GRT': 0.05433703646255237}"")"
"(""DEVIATIONS: {'ZAR': -0.005972665325966027, 'BTC': -0.015456975449043397, ""
 ""'ETH': 0.0135694442887338, 'LTC': -0.016242079071417587, 'COMP': ""
 ""-0.005938639028275065, 'THETA': -0.007862396802982771, 'LINK': ""
 ""0.023566274926398824, 'GRT': 0.014337036462552369}"")"
"'SUM OF DEVIATION (Should be 0): 1.457167719820518e-16'"
'\n'
"""The symbols to trade are now: ['BTC', 'ETH', 'LTC', 'LINK', 'GRT']"""
"'Max Priority present in sufficiently different assets is: 2'"
"'There are Altcoins to be traded...'"
"'ETH needs to be traded, with a value 0.0002773031963450644 BTC'"
"'NOW Selling ETHBTC by 0.006'"
"'LTC needs to be traded, with a value -0.00033192077331662415 BTC'"

