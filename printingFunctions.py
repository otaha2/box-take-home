from Functions import *
import utils

def printBeginTurn(game, listToPrint):
    if game.prevMove != "":
        printPrevCommand(game)
        
    game.refreshStrBoard()
    strB = utils.stringifyBoard(game.strBoard)
    print(strB)

    print("Captures UPPER:", end="")
    for item in game.upperPlayer.captures:
        print(" " + str(item), end="")
    
    print("")
    print("Captures lower: ", end="")
    for item in game.lowerPlayer.captures:
        print(str(item) + " ", end="")

    print("")

    if game.playerInCheck == True:
        print(game.playerTurn + " player is in check!")
        print("Available moves:")
        printList(listToPrint)
        


def ListPossibleCheckMoves(game, possibleMoves):

        listOfMoves = []

        for move in possibleMoves:
            beginPos = move[0]
            endPos = move[1]
            alphaBeginPos = fromIndexToAlpha(beginPos)
            alphaEndPos = fromIndexToAlpha(endPos)
            listOfMoves.append("move " + alphaBeginPos + " " + alphaEndPos)

        listOfMoves.sort()
        # for move in listOfMoves:
        #     print(move)

        return listOfMoves

def printList(listToPrint):

    for item in listToPrint:
        print(item)

def printPrevCommand(game):
        # self.prevCommand = command
        commandString = game.prevMove
        
        print(game.playerTurn + " player action: " + commandString)