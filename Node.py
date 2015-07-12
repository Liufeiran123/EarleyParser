__author__ = 'lfr'
import os,sys
from State import State
from Production import Production

class Node:
    def __init__(self,father,grammarElement,Productionstr,Production):
        self.__father = father
        self.__grammarElement = grammarElement
        self.__productionstr = Productionstr
        self.__production = Production
        self.__children = []

    def expandNode(self,currentstateToExpand,earleyProductions):
        print ""
        print "currently in expansion of - ",currentstateToExpand.getNonTerminal(),
        for ab in currentstateToExpand.getProduction().getProductionContent():
            print  " ",  ab , " ",
        for pro in self.__productionstr[::-1]:
            if pro in earleyProductions:
                nextStateToExpand = currentstateToExpand.getBacktraceState()
                child = Node(self,nextStateToExpand.getNonTerminal(),nextStateToExpand.getProduction().getProductionContent(),\
                        nextStateToExpand.getProduction())
                self.__children.insert(0,child)
                currentstateToExpand = child.expandNode(nextStateToExpand,earleyProductions)
                print ""
                print "finished expanding - " , nextStateToExpand.getNonTerminal()
            else:
                child = Node(self,pro,[],None)
                self.__children.insert(0,child)
                currentstateToExpand = currentstateToExpand.getBacktraceState()
                currentstateToExpand = currentstateToExpand.getBacktraceState()
        return currentstateToExpand

    def printf(self):
        print  "Node [" , self.__grammarElement , "]{",
        for nodes in self.__children:
            nodes.printf()
        print "}",


    def getProduction(self):
        return self.__production