from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook

from Functions import *
from printingFunctions import *

def addPieceToBoard(line, board):
    """
    Add a piece defined from file to board
    """
    
    #This check was made becuase promotedPawnIllegalMoves had a space in front of all lines for some reason
    startIndex = 0
    pieceReached = False
    for i in line:
        if i != " ":
            pieceReached = True
        if i == " " and not pieceReached:
            startIndex += 1

    #Get the index on board of the piece
    if "+" in line:
        piecePos = fromAlphaToIndex(line[startIndex + 3:startIndex + 5])
    else:
        piecePos = fromAlphaToIndex(line[startIndex + 2:startIndex + 4])

    #Initialize piece based on line
    if "p" in line:
        piece = Pawn.Pawn("lower", piecePos[0], piecePos[1])
    elif "P" in line:
        piece = Pawn.Pawn("UPPER", piecePos[0], piecePos[1])
            
    elif "k" in line:
        piece = King.King("lower", piecePos[0], piecePos[1])
    elif "K" in line:
        piece = King.King("UPPER", piecePos[0], piecePos[1])
            
    elif "g" in line:
        piece = GoldGeneral.GoldGeneral("lower", piecePos[0], piecePos[1])
    elif "G" in line:
        piece = GoldGeneral.GoldGeneral("UPPER", piecePos[0], piecePos[1])
            
    elif "s" in line:
        piece = SilverGeneral.SilverGeneral("lower", piecePos[0], piecePos[1])
    elif "S" in line:
        piece = SilverGeneral.SilverGeneral("UPPER", piecePos[0], piecePos[1])
            
    elif "r" in line:
        piece = Rook.Rook("lower", piecePos[0], piecePos[1])
    elif "R" in line:
        piece = Rook.Rook("UPPER", piecePos[0], piecePos[1])

    elif "B" in line:
        piece = Bishop.Bishop("UPPER", piecePos[0], piecePos[1])
    elif "b" in line:
        piece = Bishop.Bishop("lower", piecePos[0], piecePos[1])
        
    #Promoted piece, so promote the piece
    if "+" in line:
        piece.promote()

    #update board with the newly initialized piece
    board[piecePos[0]][piecePos[1]] = piece

def initCaptures(game, line, player):
    """
    Initialize Player Captures from File
    player input is:    0 for UPPER player Captures
                        1 for lower player Captures
    """
    #This was put in place because promotedPawnIllegalMoves had a space in front of all lines for some reason
    if line[0] == " ":
        line = line[1:len(line)]

    #get a list of pieces to add to captures
    stringList = line[1:len(line) - 2]
    stringPiecesCaptured = stringList.split(" ")

    #Upper Player
    if player == 0:
        for item in stringPiecesCaptured:
            #Piece position does not matter for now becuase that will get updated when the piece is dropped
            if item == "P":
                game.upperPlayer.addCapture(Pawn.Pawn("UPPER", 1, 1))
            elif item == "K":
                game.upperPlayer.addCapture(King.King("UPPER", 1, 1))
            elif item == "G":
                game.upperPlayer.addCapture(GoldGeneral.GoldGeneral("UPPER", 1, 1))
            elif item == "S":
                game.upperPlayer.addCapture(SilverGeneral.SilverGeneral("UPPER", 1, 1))
            elif item == "B":
                game.upperPlayer.addCapture(Bishop.Bishop("UPPER", 1, 1))
            elif item == "R":
                game.upperPlayer.addCapture(Rook.Rook("UPPER", 1, 1))
    #Lower player
    elif player == 1:
        for item in stringPiecesCaptured:
            #Piece position does not matter for now becuase that will get updated when the piece is dropped
            if item == "p":
                game.lowerPlayer.addCapture(Pawn.Pawn("lower", 1, 1))
            elif item == "k":
                game.lowerPlayer.addCapture(King.King("lower", 1, 1))
            elif item == "g":
                game.lowerPlayer.addCapture(GoldGeneral.GoldGeneral("lower", 1, 1))
            elif item == "s":
                game.lowerPlayer.addCapture(SilverGeneral.SilverGeneral("lower", 1, 1))
            elif item == "b":
                game.lowerPlayer.addCapture(Bishop.Bishop("lower", 1, 1))
            elif item == "r":
                game.lowerPlayer.addCapture(Rook.Rook("lower", 1, 1))

def getMoveCommand(line):
    """
    get the move defined in text file
    returns: move in space seperated list

    Example:    line = "move a1 a2"
                commandList = ["move", "a1", "a2"]
    """
    commandList = line.split(" ")
    #Get rid of the newline in the last element of the list
    if "\n" in line:
        lastElement = commandList[len(commandList) - 1]
        lastElement = lastElement[:len(lastElement) - 1]
        commandList[len(commandList) - 1] = lastElement
    
    return commandList

def printIsInCheck(game):
    """
    Called only from file mode game
    Handles getting all moves out of check and printing them
    returns:    list of possible moves
                -1 if checkmate and game ended
    """

    #Get possible MOVES to get out of check
    possibleMoves = getPossibleMovesOutCheck(game.playerTurn, game.board)

    #Get possible DROPS to get out of check
    if game.playerTurn == "lower":
        possibleDrops = getPossibleDropsOutCheck(game.playerTurn, game.board, game.lowerPlayer.captures)
    elif game.playerTurn == "UPPER":
        possibleDrops = getPossibleDropsOutCheck(game.playerTurn, game.board, game.upperPlayer.captures)

    #Exists no moves or drops to get out of check ---> Checkmate
    if not possibleMoves and not possibleDrops:
        game.Checkmate = True
        if game.playerTurn == "lower":
            game.gameWinner = "UPPER"
        else:
            game.gameWinner = "lower"
        game.returnMessage = " Checkmate."
        game.endGame()
        return -1
    #Otherwise get the string representation of the moves and drops
    else:
        alphaPossibleMoves = ListPossibleCheckMoves(game, possibleMoves)
        alphaPossibleDrops = ListPossibleCheckDrops(game, possibleDrops)

    #Combine moves and drops
    combinedList = alphaPossibleMoves + alphaPossibleDrops
    combinedList.sort()
    
    return combinedList