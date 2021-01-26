from python.dataBot import DataBot

## class to handle, building from DataBot, the info for an asset
class Asset(DataBot):
    pass

    def setName(self, name):
        self.name = name

    def setSymbol(self, symbol):
        self.symbol = symbol

    def getQuote(self):
        self.getQuote(self.symbol)

    def getTotalAssetBalance(self):
        self.getTotalAssetBalance(self.symbol)

    def getTotalAssetValue(self):
        getTotalAssetValue = self.getQuote() * self.getTotalAssetBalance()