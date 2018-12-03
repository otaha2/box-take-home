from Functions import *
import utils

def printBeginTurn(game, listToPrint):
    """
        Called at the beginning of every turn
        Prints the board, Captured pieces, and available moves if the player is in check
        Returns: Nothing
    """
        
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
        print("")
        print(game.playerTurn + " player is in check!")
        print("Available moves:")
        printList(listToPrint)
    else:
        print("")


def ListPossibleCheckMoves(game, possibleMoves):
    """
        Given a game object, and tuple-integer representation ex: ((0, 0), (0, 1)) of moves to get out of check
        return a list of string representation "move a1 a2" of possible moves to get player out of check
    """
    listOfMoves = []

    for move in possibleMoves:
        #Get the beginning position and end position
        beginPos = move[0]
        endPos = move[1]
        #Call index to alpha helper functions
        alphaBeginPos = fromIndexToAlpha(beginPos)
        alphaEndPos = fromIndexToAlpha(endPos)
        #Create and add the string move command
        listOfMoves.append("move " + alphaBeginPos + " " + alphaEndPos)

    return listOfMoves

def ListPossibleCheckDrops(game, possibleDrops):
    """
        Given a game object, and tuple-integer representation ex: (B, (0,0)) of drops to get out of check
        return a list of string representation "drop b a1" of possible drops to get player out of check
    """
    listOfDrops = []

    for drop in possibleDrops:
        #Get piece to drop and position to drop it in
        pieceStr = drop[0]
        pieceStr = pieceStr.lower()
        pos = drop[1]
        #Call index to alpha helper function
        alphaPos = fromIndexToAlpha(pos)
        #Create and add the string drop command
        listOfDrops.append("drop " + pieceStr + " " + alphaPos)

    return listOfDrops


def printList(listToPrint):
    """
        Helper function to print a list with each item in list on a line
    """

    for item in listToPrint:
        print(item)

def printPrevCommand(game):
    """
        Called from Print Begin Turn to print command made by the previous player
        Returns: Nothing
    """

    if game.playerTurn == "lower":
        prevPlayer = "UPPER"
    else:
        prevPlayer = "lower"
    
    print(prevPlayer + " player action: " + game.prevMove)