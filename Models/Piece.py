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
    def availableMoves(self, posx, posy, board):
        return "No Available Moves for a Piece"

    @abstractmethod
    def doSomething(self):
        print("Piece is doing something!")
