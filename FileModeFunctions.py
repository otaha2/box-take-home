from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook

from Functions import *
from printingFunctions import *

def addPieceToBoard(alphaPiece, alphaPosition, board):
    """
    Add a piece defined from file to board
    Inputs:     alphaPiece      -- string representation of piece ex: "p" for lower player Pawn
                alphaPosition   -- string representation of board position ex: "a1" which is (0,0) on board
                board           -- board to add piece to
    """
    
    #Get the index on board of the piece
    piecePos = fromAlphaToIndex(alphaPosition)

    #Initialize piece based on line
    if "p" in alphaPiece:
        piece = Pawn.Pawn("lower", piecePos[0], piecePos[1])
    elif "P" in alphaPiece:
        piece = Pawn.Pawn("UPPER", piecePos[0], piecePos[1])
            
    elif "k" in alphaPiece:
        piece = King.King("lower", piecePos[0], piecePos[1])
    elif "K" in alphaPiece:
        piece = King.King("UPPER", piecePos[0], piecePos[1])
            
    elif "g" in alphaPiece:
        piece = GoldGeneral.GoldGeneral("lower", piecePos[0], piecePos[1])
    elif "G" in alphaPiece:
        piece = GoldGeneral.GoldGeneral("UPPER", piecePos[0], piecePos[1])
            
    elif "s" in alphaPiece:
        piece = SilverGeneral.SilverGeneral("lower", piecePos[0], piecePos[1])
    elif "S" in alphaPiece:
        piece = SilverGeneral.SilverGeneral("UPPER", piecePos[0], piecePos[1])
            
    elif "r" in alphaPiece:
        piece = Rook.Rook("lower", piecePos[0], piecePos[1])
    elif "R" in alphaPiece:
        piece = Rook.Rook("UPPER", piecePos[0], piecePos[1])

    elif "B" in alphaPiece:
        piece = Bishop.Bishop("UPPER", piecePos[0], piecePos[1])
    elif "b" in alphaPiece:
        piece = Bishop.Bishop("lower", piecePos[0], piecePos[1])
        
    #Promoted piece, so promote the piece
    if "+" in alphaPiece:
        piece.promote()

    #update board with the newly initialized piece
    board[piecePos[0]][piecePos[1]] = piece
    return


def initCaptures(game, capturesList, player):
    """
    Initialize Player Captures from File
    Input:          player          ---  0 for UPPER player Captures, 1 for lower player Captures
                    capturesList    --- list of captured pieces
                    game            --- game object
    
    """

    #Upper Player
    if player == 0:
        for item in capturesList:
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
        for item in capturesList:
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
    
    return

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