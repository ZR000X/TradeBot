from python.asset import Asset

## A Class that will handle updating and storing all data of the portfolio
class Portfolio(Asset):
    pass

    ## Adds an asset class to the Portfolio's list of assets
    def addAsset(self, asset):
        self.assetList.add(asset)

    ## will use the getQuote method to update ever asset's price
    def updateQuotes(self):
        for asset in self.assetList:
            self.quotes[asset.name] = asset.getQuote()
    
    ## A useful method to say T/F if the portfolio has registered an asset, by name
    def hasAssetName(self, name):
        for asset in self.assetList:
            if asset.name == name:
                hasAssetName = True
        hasAssetName = False

    ## given a list of names, this method will ensure an asset with each name exists in the list
    def compileAssetNames(self, listOfNames):
        for name in listOfNames:
            if self.hasAssetName(name) == True:
                continue
            else:
                asset = Asset(self.api_key, self.api_sec)
                asset.setName(name)
                self.addAsset(asset)
    
    ## will place, for each of self's asset, the given symbol, according to the given dictionary 
    def compileAssetSymbols(self, dictionary):
        for asset in self.assetList:
            if asset.name in dictionary:
                asset.setSymbol(dictionary[asset.name])