__author__ = 'lfr'
import sys,os,codecs
from State import State
from Production import Production
from Node import Node


class EarleyParser:
    def __init__(self):
        self.__earleyProductions = {}
        self.__earleyDictionary = {}
        self.__earleyParserChart = []
        self.__inputVector = []
        self.__returnVector = []

    def initialize(self,filePath):
        inputdata = codecs.open(filePath,'r','utf-8')
        for line in inputdata.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            words = line.strip().split('->')
            for word in words:
                print '[DEBUG]:','line token:[',word,']'
            productions = words[1].split(' ')
            for production in productions:
                print "[DEBUG]:","production token:[",production,"]"
            if words[0] in self.__earleyProductions:
                print "[DEBUG]:found [",words[0],"] adding Production to existing list"
                tmp = self.__earleyProductions[words[0]]
                tmp.append(Production(len(productions),productions))
            else:
                tmp = []
                tmp.append(Production(len(productions),productions))
                self.__earleyProductions[words[0]] = tmp
                print "[DEBUG: created new list [",words[0],"] and inserted Production with success"
        inputdata.close()

    def createDictionary(self,filePath):
        inputdata = codecs.open(filePath,'r','utf-8')
        for line in inputdata.readlines():
            print "[DEBUG]:",line
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            words = line.strip().split('->')
            for word in words:
                print '[DEBUG]:','line token:[',word,']'
            if words[0] in self.__earleyDictionary:
                print "[DEBUG]: BAD INPUT DICTIONARY!"
                exit()
            else:
                self.__earleyDictionary[words[0]] = words[1]
                print "[DEBUG]: [" , words[0] , "][" , words[1], "] inserted with success"
        inputdata.close()

        for k,v in self.__earleyDictionary.items():
            print "[DEBUG]: element [" , k , "][" , v , "] in dictionary"


    def createInputStringVector(self,filePath):
        inputdata = codecs.open(filePath,'r','utf-8')
        tmp = []
        for line in inputdata.readlines():
            self.__inputVector = line.strip().split(' ')
            for words in self.__inputVector:
                if words in self.__earleyDictionary:
                    tmp.append(self.__earleyDictionary[words])
        self.__inputVector = tmp

        for words in self.__inputVector:
            print "[DEBUG]: " ,"input vector element: [" ,words, "]"
        inputdata.close()

    def getProduction(self,nonTerminal):
        if nonTerminal in self.__earleyProductions:
            return self.__earleyProductions[nonTerminal]
        else:
            return None

    def createChart(self,mainNonTerminal):
        mainProduction = self.getProduction(mainNonTerminal)
        if mainProduction == None:
            return -1

        for i in range(len(self.__inputVector)+1):
            self.__earleyParserChart.append([])

        print  "[DEBUG]: size of list (number of productions with " , mainNonTerminal , " as non terminal) = " , len(mainProduction)
        for production in mainProduction:
            for pro in production.getProductionContent():
                print "[DEBUG]: element of list " , pro
            self.__earleyParserChart[0].append(State(mainNonTerminal,production,None,0,0))
        return 1


    def parse(self):
        for i in range(len(self.__inputVector)+1):
            print i,"*************************************************************"
            for states in self.__earleyParserChart[i]:
                if states.isComplete() == False:
                    if self.getProduction(states.nextSymbolToProgress()) != None:
                        self.predictor(states,i)
                    else:
                        self.scanner(states,i)
                else:
                    self.completer(states,i)
        print "[DEBUG]: finished parsing input string!"

    def printProductions(self,mainNonTerminal):
        print  "[DEBUG]: All Productions in chart[" , len(self.__inputVector) , "]"
        print  "[DEBUG]: size of chart ",len(self.__earleyParserChart[len(self.__inputVector)])
        for states in self.__earleyParserChart[len(self.__inputVector)]:
            print  "[DEBUG]: size of production vector " , len(states.getProduction().getProductionContent())
            print  "[DEBUG]: - " , states.getNonTerminal() , " -> " ,
            for productioncontent in states.getProduction().getProductionContent():
                print productioncontent, " ",
            print ""
            print "****************************************************************** "

    def returnParsingTrees(self,mainNonTerminal):
        for states in self.__earleyParserChart[len(self.__inputVector) ]:
            if states.getNonTerminal() == mainNonTerminal and \
                    states.getProductionProgress() == len(states.getProduction().getProductionContent()):
                stateBookmark = states
                rootOfParsingTree = Node(None,stateBookmark.getNonTerminal(),stateBookmark.getProduction().getProductionContent(),\
                        stateBookmark.getProduction())
                test2 = rootOfParsingTree.expandNode(stateBookmark,self.__earleyProductions)
                print ""
                print  "finished expanding - " , test2.getNonTerminal()
                self.__returnVector.append( rootOfParsingTree )
        return self.__returnVector

    def predictor(self,stateToExpand,positionInputString):
        productionInStateToExpand = stateToExpand.getProduction()
        if stateToExpand.getProductionProgress() >= len(productionInStateToExpand.getProductionContent()):
            print  "[ERROR]: overflow in predictor!"
            exit()
        productioncontent = productionInStateToExpand.getProductionContent()
        nonTerminalToExpand = productioncontent[stateToExpand.getProductionProgress()]
        print  "[DEBUG]: predictor expanding [" , nonTerminalToExpand , "][" , stateToExpand.getProductionProgress() , "][" , stateToExpand.getInputStringProgress() , "]"
        productions = self.getProduction(nonTerminalToExpand)
        if productions != None:
            for pro in productions:
                print  "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!POSITION INPUT STRING: " , positionInputString , " " , len(self.__inputVector)
                stateToInsert = State(nonTerminalToExpand,pro,stateToExpand,positionInputString,0)
                positionOfState = self.stateExists(positionInputString,stateToInsert)
                if positionOfState < 0:
                    self.__earleyParserChart[ positionInputString ].append( stateToInsert )
                else:
                    del stateToInsert

    def scanner(self,stateToScan,positionInputString):
        productionInStateToScan = stateToScan.getProduction()
        if positionInputString >= len(self.__inputVector):
            print  "[DEBUG]: scanner fail, input string end reached"
            return
        if self.__inputVector[positionInputString] == productionInStateToScan.getProductionContent()[stateToScan.getProductionProgress()]:
            print  "[DEBUG]: scan [" , self.__inputVector[positionInputString], "][" , stateToScan.getProductionProgress() , "][" , stateToScan.getInputStringProgress(), "]"
            stateToInsert = State( stateToScan.getNonTerminal(), stateToScan.getProduction(), stateToScan, stateToScan.getInputStringProgress(), stateToScan.getProductionProgress() + 1 )
            print  "[DEBUG]: scanner is inserting state in chart position " , positionInputString + 1
            self.__earleyParserChart[ positionInputString + 1].append(stateToInsert)
        else:
            print  "[DEBUG]: scan mismatch - input[" , self.__inputVector[positionInputString] , "] production[" , productionInStateToScan.getProductionContent()[stateToScan.getProductionProgress()],"]"

    def completer(self,stateCompleted,positionInputString):
        print  "[DEBUG]: complete [" , stateCompleted.getNonTerminal() , "][" , stateCompleted.getProductionProgress() , "][" , stateCompleted.getInputStringProgress() , "]"
        if stateCompleted.getInputStringProgress() >= len(self.__earleyParserChart):
            print  "[ERROR]: COMPLETER OVERFLOW"
            exit(1)
        for states in self.__earleyParserChart[stateCompleted.getInputStringProgress()]:
            if len(states.getProduction().getProductionContent()) <= states.getProductionProgress():
                continue
            productioncontent = states.getProduction().getProductionContent()
            if stateCompleted.getNonTerminal() == productioncontent[states.getProductionProgress()]:
                stateToInsert = State( states.getNonTerminal(), states.getProduction(), stateCompleted, states.getInputStringProgress(), states.getProductionProgress() + 1)
                self.__earleyParserChart[ positionInputString ].append( stateToInsert )

    def stateExists(self,chartPosition,stateToCheck):
        for states in self.__earleyParserChart[chartPosition]:
            if states.getNonTerminal() == stateToCheck.getNonTerminal() and \
                states.getInputStringProgress() == stateToCheck.getInputStringProgress() and \
                id(states.getProduction()) == id(stateToCheck.getProduction()) and \
                states.getProductionProgress() == stateToCheck.getProductionProgress():
               # print  "[DEBUG]: found same state at position " , it - this->earleyParserChart[ chartPosition ].begin() << " of chart[" << chartPosition << "]" << endl;
                return 1
        return -1


