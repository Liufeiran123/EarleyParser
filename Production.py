__author__ = 'lfr'
class Production(object):
    def __init__(self,productionLength,productionContent):
        self.__productionLength = productionLength
        self.__productionContent = productionContent

    def getProductionLength(self):
        return self.__productionLength

    def getProductionContent(self):
        return self.__productionContent


