from Models import Piece

class Bishop(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "B"
        else:
            self.name = "b"

    def availableMoves(self, posx, posy, board):
        print("Bishop implemented")
    
    def doSomething(self):
        super().doSomething()
        print("Now Bishop is doing something!")

if __name__ == "__main__":
    newBishop = Bishop("lower", 1, 1)
    newBishop.doSomething()