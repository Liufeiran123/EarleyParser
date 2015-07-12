__author__ = 'lfr'
import os,sys
from Production import Production

class State:
    def __init__(self,nonTerminal,Production,backtraceState,inputStringProgress,productionProgress):
        self.__noTerminal = nonTerminal
        self.__Production = Production
        self.__backtraceState = backtraceState
        self.__inputStringProgress = inputStringProgress
        self.__productionProgress = productionProgress
        self.__printed = False

    def getBacktraceState(self):
        return self.__backtraceState
    def getNonTerminal(self):
        return self.__noTerminal
    def getProduction(self):
        return self.__Production
    def getProductionProgress(self):
        return self.__productionProgress
    def getInputStringProgress(self):
        return self.__inputStringProgress
    def isComplete(self):
        if self.getProductionProgress() == len(self.getProduction().getProductionContent()):
            return True
        else:
            return False

    def nextSymbolToProgress(self):
        tmp = self.getProduction().getProductionContent()
        return tmp[self.__productionProgress]
    def getPrinted(self):
        return self.__printed
    def setPrintedTrue(self):
        self.__printed = True




