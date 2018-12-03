from abc import ABC, abstractmethod

from isSquareEmpty import isSquareEmpty

BOARDWIDTH = 5
BOARDHEIGHT = 5

class Piece(ABC):
    """
        Parent class of all other pieces (Pawn, King, Rook, etc)
    """

    promoted = False
    name = ""

    def __init__(self, player, posx, posy):
        self.player = player
        self.posx = posx
        self.posy = posy
    
    def promote(self):
        """
            Promote the piece
        """
        self.promoted = True
        self.name = "+" + self.name
    
    def printName(self):
        print(self.name)

    def __str__(self):
        return self.name

    @abstractmethod
    def availableMoves(self, board):
        return "No Available Moves for a Piece"

    def inBounds(self, x, y):
        """
            checks whether position is in bound
            return: True for yes
                    False for no ... Yes I know, pretty intuitive :)
        """
        if x >= 0 and x < 5 and y >= 0 and y < 5:
            return True
        else:
            return False
    
    def isSquareValid(self, x, y, board):
        """
            Check if square on board is valid
        """
        #Empty square ... is valid
        if board[x][y] == 1:
            return True
        #If piece in square belongs to other player ... also valid
        elif type(board[x][y]) != str and board[x][y].player != self.player:
            return True
        else:
            return False

    def isValidMove(self, x, y, board):
        """
            Checks for validity of the move
        """
        #Move is valid if move is in bound, and square is valid to move to
        if self.inBounds(x, y) and self.isSquareValid(x, y, board):
            return True
        else:
            return False

    def availableDrops(self, board):
        """
            Positions piece can be dropped
            returns:    list of possible drop locations
            **Overriden by Pawn**
        """
        listPos = []
        for i in range(0, 5):
            for j in range(0, 5):
                if isSquareEmpty((i,j), board):
                    listPos.append((i,j))

        return listPos
            


    def checkForPromotion(self, prevPos):
        """
        Checks if piece can be promoted
        returns:    True if valid Promotion
                    False if not valid for promotion
        """
        if self.promoted == True:
            return False

        # prevX = prevPos[0]
        prevY = prevPos[1]

        #Entering or leaving promotion zone
        if self.player == "lower": 
            if self.posy == BOARDHEIGHT - 1 or prevY == BOARDHEIGHT - 1:
                return True
        elif self.player == "UPPER":
            if self.posy == 0 or prevY == 0:
                return True
        else:
            return False
