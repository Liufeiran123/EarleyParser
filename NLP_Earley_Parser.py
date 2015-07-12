__author__ = 'lfr'

import sys,os
from State import State
from Production import Production
from Node import Node
from EarleyParser import EarleyParser



if __name__ == "__main__":
    if len(sys.argv) != 5:
        print  "Usage: ./NLP_Earley_Parser 'CFG File' 'Input Dictionary File' 'Input string file' 'main NonTerminal'"
        exit(1)
    earleyparser = EarleyParser()
    earleyparser.initialize(sys.argv[1])
    earleyparser.createDictionary(sys.argv[2])
    earleyparser.createInputStringVector(sys.argv[3])
    mainNonTerminal = sys.argv[4]

    checkOperation = earleyparser.createChart( mainNonTerminal )
    if checkOperation < 0 :
        exit(1)
    earleyparser.parse()
    earleyparser.printProductions( mainNonTerminal )
    vectorOfParsingTreeRoots = earleyparser.returnParsingTrees( mainNonTerminal )

    for trees in vectorOfParsingTreeRoots:
        trees.printf()
        print ""
        print "*****************************************************"





