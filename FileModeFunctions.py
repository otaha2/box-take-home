from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook

from Functions import *
from printingFunctions import *

def addPieceToBoard(line, board):
    """
    Add a piece defined from file to board
    """
    #Get the index on board of the piece
    if "+" in line:
        piecePos = fromAlphaToIndex(line[3:5])
    else:
        piecePos = fromAlphaToIndex(line[2:4])

    #Initialize piece
    if "p" in line:
        piece = Pawn.Pawn("lower", piecePos[0], piecePos[1])
    elif "P" in line:
        piece = Pawn.Pawn("UPPER", piecePos[0], piecePos[1])
            
    if "k" in line:
        piece = King.King("lower", piecePos[0], piecePos[1])
    elif "K" in line:
        piece = King.King("UPPER", piecePos[0], piecePos[1])
            
    if "g" in line:
        piece = GoldGeneral.GoldGeneral("lower", piecePos[0], piecePos[1])
    elif "G" in line:
        piece = GoldGeneral.GoldGeneral("UPPER", piecePos[0], piecePos[1])
            
    if "s" in line:
        piece = SilverGeneral.SilverGeneral("lower", piecePos[0], piecePos[1])
    elif "S" in line:
        piece = SilverGeneral.SilverGeneral("UPPER", piecePos[0], piecePos[1])
            
    if "b" in line:
        piece = Bishop.Bishop("lower", piecePos[0], piecePos[1])
    elif "B" in line:
        piece = Bishop.Bishop("UPPER", piecePos[0], piecePos[1])
            
    if "r" in line:
        piece = Rook.Rook("lower", piecePos[0], piecePos[1])
    elif "R" in line:
            piece = Rook.Rook("UPPER", piecePos[0], piecePos[1])
        
    #Promoted piece, so promote the piece
    if "+" in line:
        piece.promote()

    # if type(piece) == Bishop.Bishop:
    #     print("Position to add: " + str((piecePos[0], piecePos[1])))

    #Set the board square to contain piece
    board[piecePos[0]][piecePos[1]] = piece

def getMoveCommand(line):
    """
    get the move defined in text file
    returns: move in space seperated list
    """
    commandList = line.split(" ")
    lastElement = commandList[len(commandList) - 1]
    lastElement = lastElement[:len(lastElement) - 1]
    commandList[len(commandList) - 1] = lastElement

    return commandList

def printIsInCheck(game):
    """
    Called only from file mode game
    Handles getting all moves out of check and printing them
    """
    possibleMoves = getPossibleMovesOutCheck(game.playerTurn, game.board)
    if len(possibleMoves) == 0:
        if game.playerTurn == "lower":
            game.gameWinner = "UPPER"
        else:
            game.gameWinner = "lower"
        game.returnMessage = "Checkmate."
        game.endGame()
        return
    else:
        alphaPossibleMoves = ListPossibleCheckMoves(game, possibleMoves)