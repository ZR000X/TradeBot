# TradeBot
Welcome to TradeBot! \\

Using the python-binance package (documentation: https://python-binance.readthedocs.io/en/latest/), we are developing an easy-to-use rebalancing bot. \\

The Bot will:
1.) Load the user-set system-parameters. \\
2.) Load the price and balance data from Binance. \\
3.) Calculate the value of each holding, and its percentage of the total value. \\
4.) Use the parameters to calculate discrepencies between current allocations of value per asset and user-set allocations. \\
5.) Build trades out of these discrepencies, should they meet certain user-set and Binance-set requirements. \\
6.) Perform the trades to rebalance the portfolio. \\
7.) Repeat continuously, so can be left running throughout the day. \\

# Update pip in cmd
python -m pip install --upgrade pip
# Install dependencies
pip install python-binance
# links
https://python-binance.readthedocs.io/en/latest/
https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md

## Usage Guide
Ensure that the requirements are installed and that your system variables are correct. \\
Simply run the mainBot2.py script in command prompt \\
Be sure to edit the config.py and mainBot2.py python files properly before use!