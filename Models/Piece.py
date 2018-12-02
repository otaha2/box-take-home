from abc import ABC, abstractmethod

from SeperateFunctions import isSquareEmpty

BOARDWIDTH = 5
BOARDHEIGHT = 5

class Piece(ABC):

    promoted = False
    name = ""

    def __init__(self, player, posx, posy):
        self.player = player
        self.posx = posx
        self.posy = posy
    
    def promote(self):
        self.promoted = True
        self.name = "+" + self.name
    
    def printName(self):
        print(self.name)

    def __str__(self):
        return self.name

    @abstractmethod
    def availableMoves(self, board):
        return "No Available Moves for a Piece"

    @abstractmethod
    def doSomething(self):
        print("Piece is doing something!")

    def inBounds(self, x, y):
        if x >= 0 and x < 5 and y >= 0 and y < 5:
            return True
        else:
            return False
    
    def isSquareValid(self, x, y, board):
        if board[x][y] == 1:
            return True
        elif type(board[x][y]) != str and board[x][y].player != self.player:
            return True
        else:
            return False

    def isValidMove(self, x, y, board):
        if self.inBounds(x, y) and self.isSquareValid(x, y, board):
            return True
        else:
            return False

    def availableDrops(self, board):
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
