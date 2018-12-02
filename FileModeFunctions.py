from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook

from Functions import *
from printingFunctions import *

def addPieceToBoard(line, board):
    """
    Add a piece defined from file to board
    """
    
    startIndex = 0
    pieceReached = False
    for i in line:
        if i != " ":
            pieceReached = True
        if i == " " and not pieceReached:
            startIndex += 1
    # print(line)
    # print(line[startIndex + 2:startIndex + 4])
    #Get the index on board of the piece
    if "+" in line:
        piecePos = fromAlphaToIndex(line[startIndex + 3:startIndex + 5])
    else:
        piecePos = fromAlphaToIndex(line[startIndex + 2:startIndex + 4])

    #Initialize piece
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

    #Set the board square to contain piece
    board[piecePos[0]][piecePos[1]] = piece

def initCaptures(game, line, player):
    """
    Initialize Player Captures from File
    0 for UPPER player Captures
    1 for lower player Captures
    """
    #This was put in place because promotedPawnIllegalMoves had a space in front of all lines for some reason
    if line[0] == " ":
        line = line[1:len(line)]

    stringList = line[1:len(line) - 2]
    stringPiecesCaptured = stringList.split(" ")
    #Uppler Player
    if player == 0:
        for item in stringPiecesCaptured:
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
    elif player == 1:
        for item in stringPiecesCaptured:
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
    """
    commandList = line.split(" ")
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
    possibleMoves = getPossibleMovesOutCheck(game.playerTurn, game.board)
    if not possibleMoves:
        game.Checkmate = True
        if game.playerTurn == "lower":
            game.gameWinner = "UPPER"
        else:
            game.gameWinner = "lower"
        game.returnMessage = " Checkmate."
        game.endGame()
        return -1
    else:
        alphaPossibleMoves = ListPossibleCheckMoves(game, possibleMoves)
    
    return alphaPossibleMoves