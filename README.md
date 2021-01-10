# TradeBot
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

EXAMPLE OUTPUT:
** Note: The current state of the projects only requires the two Python files to operate. But it expects and 'output' folder to be present to drop the output csv files.
Here is an example of what an output csv file currently looks like:

Summing up the allocation settings:
The Total Set Allocations sum to (Should be 1.0)1.0
""
TICKERS:['ZAR', 'BTC', 'ETH', 'LTC', 'COMP', 'THETA', 'LINK']
PAIRS:{'ZAR': '', 'BTC': 'BTCZAR', 'ETH': 'ETHBTC', 'LTC': 'LTCBTC', 'COMP': 'COMPBTC', 'THETA': 'THETABTC', 'LINK': 'LINKBTC'}
ALLOCATIONS:{'ZAR': 0.02, 'BTC': 0.26, 'ETH': 0.35, 'LTC': 0.25, 'COMP': 0.04, 'THETA': 0.03, 'LINK': 0.05}
Oh, and the PRIORITIES are:{'ZAR': 0, 'BTC': 1, 'ETH': 2, 'LTC': 2, 'COMP': 2, 'THETA': 2, 'LINK': 2}
NOW reading Asset Holdings for these tickers...
HOLDINGS:{'ZAR': 174.41870377, 'BTC': 0.00356238, 'ETH': 0.16176399, 'LTC': 0.8218515, 'COMP': 0.112887, 'THETA': 9.97, 'LINK': 1.68801}
""
NOW getting the prices (ZAR) for these assets in the last minute
Out of bounds error, retrying...
Out of bounds error, retrying...
Out of bounds error, retrying...
Out of bounds error, retrying...
Out of bounds error, retrying...
Out of bounds error, retrying...
Out of bounds error, retrying...
PRICES:{'ZAR': 1, 'BTC': 644682.0, 'ETH': 19448.766576, 'LTC': 2721.202722, 'COMP': 2835.956118, 'THETA': 32.06648268, 'LINK': 266.02158048}
""
NOW calculated the values (ZAR) of each asset
VALUES: {'ZAR': 174.41870377, 'BTC': 2296.60226316, 'ETH': 3146.1100819123985, 'LTC': 2236.424538879783, 'COMP': 320.14257829266603, 'THETA': 319.7028323196, 'LINK': 449.0470880660448}
TOTAL VALUE: 8942.448086400493
""
NOW calculating the percentages (%) of each asset of the portfolio and the difference to the allocations
PERCENTAGES: {'ZAR': 0.019504581081689776, 'BTC': 0.25682030703120656, 'ETH': 0.35181753939359667, 'LTC': 0.25009086072089093, 'COMP': 0.0358003284111353, 'THETA': 0.03575115328942173, 'LINK': 0.05021523007205904}
DEVIATIONS: {'ZAR': -0.0004954189183102239, 'BTC': -0.003179692968793446, 'ETH': 0.00181753939359669, 'LTC': 9.086072089092845e-05, 'COMP': -0.004199671588864702, 'THETA': 0.0057511532894217315, 'LINK': 0.0002152300720590361}
SUM OF DEVIATION (Should be 0): 1.3877787807814457e-17
""
NOW determining which symbols are significantly different to trade0.01
The symbols to trade are now: []
NOW we are going to check if we are at priority level 2 or 1 or neither
Max Priority present in sufficiently different assets is: 0
There are no trades to be done... But...
Yeah, no, nothing

# Update pip in cmd
python -m pip install --upgrade pip
# Install dependencies
pip install python-binance
pip install wscat
# links
https://python-binance.readthedocs.io/en/latest/
https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md


## PROJECT DIRECTORIES from zrfir
cd "OneDrive\__Projects\Financial Freedom\Trading\TradeBot\Coinview"

### Cmd that obtains a stream with the Binance API: BTCUSD --!>
# See: 
wscat -c wss://stream.binance.com:9443/ws/btcusdt@trade

## Example of a trade data
{"e":"trade","E":1609858662378,"s":"BTCUSDT","t":546883709,"p":"32146.78000000","q":"0.02893100","b":4163994208,"a":4163994165,"T":1609858662378,"m":false,"M":true}
Payload: {
  "e": "trade",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order ID
  "a": 50,          // Seller order ID
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore
}
See: https://www.unixtimestamp.com/index.php for Unix Time Stamp converter

wscat -c wss://stream.binance.com:9443/ws/btcusdt@trade // BTCUSDT Ticks
wscat -c wss://stream.binance.com:9443/ws/btcusdt@kline_1m // BTCUSDT Candlestick 1min

## To Pipe the data to a file, append the following to stream request
 | tee <filename>


