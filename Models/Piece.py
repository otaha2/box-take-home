from abc import ABC, abstractmethod

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
        if board[y][x] == 1:
            return True
        elif board[y][x] != 1 and type(board[y][x]) != str and board[y][x].player != self.player:
            return True
        else:
            return False

    def isValidMove(self, x, y, board):
        if self.inBounds(x, y) and self.isSquareValid(x, y, board):
            return True
        else:
            return False
