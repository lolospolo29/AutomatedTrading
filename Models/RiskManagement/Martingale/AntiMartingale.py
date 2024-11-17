from Interfaces.RiskManagement.IMartingale import IMartingale


class AntiMartingale(IMartingale):
    def __init__(self,orderAmount):
        self.orderAmount: int = orderAmount

    def getOrderAmount(self):
        return self.orderAmount

    def getMartingaleModel(self):
        return "Anti"
