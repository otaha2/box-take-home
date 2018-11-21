import Piece

class Pawn(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        self.name = "p"

    def availableMoves(self, posx, posy, board):
        print("Pawn implemented")
    
    def doSomething(self):
        super().doSomething()
        if(self.player == "UPPER"):
            print("My String representation is " + self.name.upper())
        else:
            print("My String representation is " + self.name)

if __name__ == "__main__":
    newPawn = Pawn("UPPER", 1, 1)
    newPawn.doSomething()