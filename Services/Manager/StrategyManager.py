class StrategyManager:
    def __init__(self):
        self.strategies = {}
        self.PDArrays = {}  # Maps each strategy to its PDArray instances
    #  self.Level = {}  # Maps each strategy to its PDArray instances
    #  self.Confirmation = {}  # Maps each strategy to its PDArray instances

    def registerStrategy(self, strategy):
        self.strategies[strategy.name] = strategy
        print(f"Strategy '{strategy.name}' created and added to the Strategy Manager.")
        self.PDArrays[strategy.name] = []

    def addPDArray(self, strategyName, pdarray):
        """Add a PDArray to a specific strategy."""
        if strategyName in self.PDArrays:
            self.PDArrays[strategyName].append(pdarray)

    def analyzeCurrentData(self, assetName, strategyName, dataPoints):
        self.strategies[strategyName].analyzeCurrentData(dataPoints)

    def analyzePreviousData(self, assetName, strategyName, dataPoints):
        pass

    def returnAllIdsForPDArrayByStrategyAndAsset(self, assetName, strategyName, status):
        """Retrieve all IDs for a specific strategy and asset."""
        ids = []
        # Check if the strategy exists in the pdArraysByStrategy
        if strategyName in self.PDArrays:
            for pdarray in self.PDArrays[strategyName]:
                # Only add IDs if the assetName matches the requested asset_name
                if pdarray.assetName == assetName:
                    if pdarray.dataStatus == status:
                        ids.append(pdarray.Ids)
        return ids
