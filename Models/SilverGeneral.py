from Models import Piece

class SilverGeneral(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "S"
        else:
            self.name = "s"

    def availableMoves(self, board):
        print("SilverGeneral implemented")
    
    def doSomething(self):
        super().doSomething()
        print("Now SilverGeneral is doing something!")

if __name__ == "__main__":
    newSilverGeneral = SilverGeneral("lower", 1, 1)
    newSilverGeneral.doSomething()