from abc import ABC, abstractmethod

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

    def checkForPromotion(self):
        if self.player == "lower" and self.posy == BOARDHEIGHT - 1:
            self.promote()
        if self.player == "UPPER" and self.posy == 0:
            self.promote()
        return
