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
    Example: (0,0) --> "a1"
    """
    posx = pos[0]
    posy = pos[1]
    alphaX = map_from_index_to_alpha[posx]
    alphaY = str(posy + 1)

    return alphaX + alphaY

def fromAlphaToIndex(pos):
    """
    Helper function to convert from alpha string representation to index tuple position on board
    Example: "a1" --> (0,0)
    """
    posx = pos[0]
    posx = map_from_alpha_to_index[posx]
    posy = int(pos[1]) - 1

    return (posx, posy)

def parseInput(arg1, arg2):
        """
        Helper function to get the indicies on board of current position and end position
        Returns a list containing 2 tuples of X and Y position on board of current and end
        """
        #Call alpha to index helper functions
        return (fromAlphaToIndex(arg1), fromAlphaToIndex(arg2))

def checkForPawnInColumn(colNum, board, player):
    """
    Returns:    True if there is a Pawn in the column
                False if not
    """
    for i in range(5):
        item = board[colNum][i]
        if type(item) == Pawn.Pawn and item.player == player:
            return True
    return False

def checkForcedPawnPromote(board, positions):
    """
        If Pawn can be promoted it must be promoted as per the specs
        returns:    1 if pawn was promoted
                    0 if not
    """

    #Get current position of the pawn
    posX = positions[1][0]
    posY = positions[1][1]

    #Get prev position of the pawn
    prevX = positions[0][0]
    prevY = positions[0][1]

    #Get the pawn
    item = board[posX][posY]

    #Forced pawn promotion
    if type(item) == Pawn.Pawn and item.checkForPromotion((prevX, prevY)) and not item.promoted:
        item.promote()
        return 1
    
    else:
        return 0

def findKing(player, board):
    """
        Finds and returns the king of the player on the board
        returns:    King object if king exists on the board
                    False if king does not exist on the board
    """
    foundKing = False
    for col in board:
        for item in col:
            if type(item) == King.King and item.player == player:
                foundKing = True
                return item
    
    if foundKing == False:
        return False

def isInCheck(player, board):
    """
        Checks if a player is in check
        Returns:    True if player is in check
                    False otherwise
    """
    #Find the king
    king = findKing(player, board)
    if king == False:
        return True
    #Get king pos
    kingPos = (king.posx, king.posy)

    enemyAvailableEndPos = []
    #Get a list of all available end positions of enemy moves
    for col in board:
        for item in col:
            if type(item) != int and item.player != player:
                enemyPieceMoves = item.availableMoves(board)
                for move in enemyPieceMoves:
                    enemyAvailableEndPos.append(move)

    #If the king pos is in the list of possible enemy end Positions then the player is in check
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
                    #Check if the copied board is now in check...
                    #if not then it is a valid move to do to get out of check
                    if not isInCheck(player, copyBoard):
                        possibleMoves.append(((piecePosX,piecePosY), move))

    return possibleMoves

def getPossibleDropsOutCheck(player, board, playerCaptures):
    """
    Return all possible drops the player can make that would result in a board that the player is NOT in check
    Returns a list of tuples. Each tuple has piece to drop, and position to drop the piece
    """
    listDropOutCheck = []
    for piece in playerCaptures:
        #Get all available places to drop the piece
        listDropPiece = piece.availableDrops(board)
        if type(listDropPiece) == list:
            for item in listDropPiece:
                #Copy the board, piece and see if doing the drop would result in a board that is NOT in check
                copyBoard = copy.deepcopy(board)
                newPiece = copy.deepcopy(piece)
                newPiece.posx = item[0]
                newPiece.posy = item[1]
                copyBoard[item[0]][item[1]] = newPiece
                if not isInCheck(player, copyBoard):
                    listDropOutCheck.append((piece.name, item))
    
    return listDropOutCheck
    