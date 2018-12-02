from Models import Pawn, King
import copy
import utils

#Dictionary to translate from alpha to index and Vice Versa
map_from_alpha_to_index = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4}
map_from_index_to_alpha = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}

def fromIndexToAlpha(pos):
    """
    Helper function to convert from tuple of index position on board,
    to alpha string representations
    """
    posx = pos[0]
    posy = pos[1]
    alphaX = map_from_index_to_alpha[posx]
    alphaY = str(posy + 1)

    return alphaX + alphaY

def fromAlphaToIndex(pos):
    """
    Helper function to convert from alpha string representation to index tuple position on board
    """
    posx = pos[0]
    posx = map_from_alpha_to_index[posx]
    posy = int(pos[1]) - 1

    return (posx, posy)

def isSquareEmpty(position, board):
    posX = position[0]
    posY = position[1]

    if board[posX][posY] == 1:
        return True
    else:
        return False

def checkForPawnInColumn(colNum, board, player):
    """
    Returns True if there is a Pawn in the column
    Else returns False
    """
    for i in range(5):
        item = board[colNum][i]
        if type(item) == Pawn.Pawn and item.player == player:
            return True
    return False

def findKing(player, board):
    foundKing = False
    for col in board:
        for item in col:
            if type(item) == King.King and item.player == player:
                foundKing = True
                return item
    
    if foundKing == False:
        return False

def isInCheck(player, board):
    king = findKing(player, board)
    if king == False:
        return True
    kingPos = (king.posx, king.posy)

    enemyAvailableEndPos = []
    #Get all available end positions of enemy moves
    for col in board:
        for item in col:
            if type(item) != int and item.player != player:
                enemyPieceMoves = item.availableMoves(board)
                # print("Piece: " + item.name)
                # print(enemyPieceMoves)
                # print("Enemy Piece: " + item.name)
                # print(enemyPieceMoves)
                for move in enemyPieceMoves:
                    enemyAvailableEndPos.append(move)
                    
    if kingPos in enemyAvailableEndPos:
        return True
    else:
        return False
                    
def getPossibleMovesOutCheck(player, board):
    """
    Return all possible moves the player can make that would result in a board that the player is NOT in check
    Returns a list of tuples. Each tuple has beginning location of piece to move and end location for that piece
    """
    possibleMoves = []
    for col in board:
        for piece in col:
            if type(piece) != int and piece.player == player:
                pieceMoves = piece.availableMoves(board)
                piecePosX = piece.posx
                piecePosY = piece.posy
                for move in pieceMoves:
                    copyBoard = copy.deepcopy(board)
                    #Do the move on the copied board
                    copyBoard[piecePosX][piecePosY] = 1
                    newPiece = copy.deepcopy(piece)
                    newPiece.posx = move[0]
                    newPiece.posy = move[1]
                    copyBoard[move[0]][move[1]] = newPiece
                    # if type(piece) == King.King:
                        # print("Current Position" + str((piecePosX, piecePosY)) + " End Pos: " + str(move))
                        # print("Copied Board:")
                        # print(copyBoard)
                    #Check if the copied board is now in check...
                    #if not then it is a valid move to do to get out of check
                    if not isInCheck(player, copyBoard):
                        possibleMoves.append(((piecePosX,piecePosY), move))
    # print("")
    return possibleMoves

def checkDetection(player, board):
    """
    Find where the players king is, and find all available moves of the opposite players pixeces
    If the players position is in one of those moves they are in check. Return True.
    """
    copyBoard = copy.deepcopy(board)

    #Find the postition of the king
    king = findKing(player, board)
    kingPos = (king.posx, king.posy)

    #Replace the position of the king in the copied board to empty
    copyBoard[kingPos[0]][kingPos[1]] = 1

    availableEndPosEnemy = []
    #Get all available end positions of enemy moves
    for col in board:
        for item in col:
            if type(item) != int and item.player != player:
                enemyPieceMoves = item.availableMoves(copyBoard)
                for move in enemyPieceMoves:
                    availableEndPosEnemy.append(move)
    
    #If the kings position is among the possible enemy positions, then the player is in check
    if kingPos in availableEndPosEnemy:
        possibleKingMoves = king.availableMoves(board)
        for move in possibleKingMoves:
            if move in availableEndPosEnemy:
                possibleKingMoves.remove(move)
    elif kingPos not in availableEndPosEnemy:
        return 0
    
    #King has no more legal moves to make... checkmate
    if len(possibleKingMoves) == 0:
        pass

    return possibleKingMoves

# def gameStrBoard(self):
#     strBoard = 
#         # i represents row
#         for i in range(5):
#             # j represents col
#             for j in range(5):
#                 if(self.board[i][j] != 1):
#                     strBoard[i][j] = str(self.board[i][j])
#                 else:
#                     self.strBoard[i][j] = ""

#     return 
        