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
    
    print("Captures lower:", end="")
    for item in game.lowerPlayer.captures:
        print(" " + str(item) , end="")

    print("")

    if game.playerInCheck == True:
        print(game.playerTurn + " player is in check!")
        print("Available moves:")
        printList(listToPrint)


def ListPossibleCheckMoves(game, possibleMoves):
    """
        Given a game object, and tuple-integer representation ex: ((0, 0), (0, 1)) of moves to get out of check
        return a list of string representation "move a1 a2" of possible moves to get player out of check
    """

    listOfMoves = []

    for move in possibleMoves:
        beginPos = move[0]
        endPos = move[1]
        alphaBeginPos = fromIndexToAlpha(beginPos)
        alphaEndPos = fromIndexToAlpha(endPos)
        listOfMoves.append("move " + alphaBeginPos + " " + alphaEndPos)

    return listOfMoves

def ListPossibleCheckDrops(game, possibleDrops):
    """
        Given a game object, and tuple-integer representation ex: (B, (0,0)) of drops to get out of check
        return a list of string representation "drop b a1" of possible drops to get player out of check
    """
    listOfDrops = []

    for drop in possibleDrops:
        pieceStr = drop[0]
        pieceStr = pieceStr.lower()
        pos = drop[1]
        alphaPos = fromIndexToAlpha(pos)
        listOfDrops.append("drop " + pieceStr + " " + alphaPos)

    return listOfDrops


def printList(listToPrint):

    for item in listToPrint:
        print(item)

def printPrevCommand(game):

        if game.playerTurn == "lower":
            prevPlayer = "UPPER"
        else:
            prevPlayer = "lower"
        
        print(prevPlayer + " player action: " + game.prevMove)