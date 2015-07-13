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
                if len(currentstateToExpand.getBacktraceStateVector()) > 1:
                    print ""
                    print "BACKTRACE VECTOR BIGGER THAN 1"
                    for btstates in currentstateToExpand.getBacktraceStateVector():
                        print ""
                        print "[DEBUG]: at 0 -" , btstates.getNonTerminal() , " size: " , len(btstates.getProduction().getProductionContent())
                        for productions in btstates.getProduction().getProductionContent():
                            print productions," "
                        print ""
                    for index,btstates in enumerate(currentstateToExpand.getBacktraceStateVector()):
                        if id(self.__father.getProduction()) == id(btstates.getProduction()):
                            currentstateToExpand = btstates
                            print "[DEBUG]: matching production pointer at position " ,index
                            break
                        if index == len(currentstateToExpand.getBacktraceStateVector()) - 1:
                            print"[ERROR]: no matching production pointer correspondent to production in this node!"
                            exit(1)
                else:
                    nextStateToExpand = currentstateToExpand.getBacktraceStateVector()[0]
                child = Node(self,nextStateToExpand.getNonTerminal(),nextStateToExpand.getProduction().getProductionContent(),\
                        nextStateToExpand.getProduction())
                self.__children.insert(0,child)
                currentstateToExpand = child.expandNode(nextStateToExpand,earleyProductions)
                print ""
                print "finished expanding - " , nextStateToExpand.getNonTerminal()
            else:
                child = Node(self,pro,[],None)
                self.__children.insert(0,child)
                if len(currentstateToExpand.getBacktraceStateVector()) > 1:
                    print ""
                    print "BACKTRACE VECTOR BIGGER THAN 1"
                    for btstates in currentstateToExpand.getBacktraceStateVector():
                        print ""
                        print "[DEBUG]: at 0 -" ,btstates.getNonTerminal() ," size: " ,len(btstates.getProduction().getProductionContent())
                        for productions in btstates.getProduction().getProductionContent():
                            print productions
                        print ""
                    for index,btstates in enumerate(currentstateToExpand.getBacktraceStateVector()):
                        if id(self.__father.getProduction()) == id(btstates.getProduction()):
                            currentstateToExpand = btstates
                            print "[DEBUG]: matching production pointer at position " , index
                            break;
                        if index == len(currentstateToExpand.getBacktraceStateVector())-1:
                            print "[ERROR]: no matching production pointer correspondent to production in this node!"
                            exit(1)
                else:
                    currentstateToExpand = currentstateToExpand.getBacktraceStateVector()[0]

                if len(currentstateToExpand.getBacktraceStateVector()) > 1:
                    print ""
                    print "BACKTRACE VECTOR BIGGER THAN 1"
                    for btstates in currentstateToExpand.getBacktraceStateVector():
                        print ""
                        print "[DEBUG]: at 0 -" ,btstates.getNonTerminal() ," size: " ,len(btstates.getProduction().getProductionContent())
                        for productions in btstates.getProduction().getProductionContent():
                            print productions
                        print ""
                    for index,btstates in enumerate(currentstateToExpand.getBacktraceStateVector()):
                        if id(self.__father.getProduction()) == id(btstates.getProduction()):
                            currentstateToExpand = btstates
                            print "[DEBUG]: matching production pointer at position " , index
                            break;
                        if index == len(currentstateToExpand.getBacktraceStateVector())-1:
                            print "[ERROR]: no matching production pointer correspondent to production in this node!"
                            exit(1)
                else:
                    currentstateToExpand = currentstateToExpand.getBacktraceStateVector()[0]
        return currentstateToExpand

    def printf(self):
        print  "Node [" , self.__grammarElement , "]{",
        for nodes in self.__children:
            nodes.printf()
        print "}",


    def getProduction(self):
        return self.__production