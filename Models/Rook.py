import Piece

class Rook(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        self.name = "r"

    def availableMoves(self, posx, posy, board):
        print("Rook implemented")
    
    def doSomething(self):
        super().doSomething()
        print("Now Rook is doing something!")

if __name__ == "__main__":
    newRook = Rook("lower", 1, 1)
    newRook.doSomething()