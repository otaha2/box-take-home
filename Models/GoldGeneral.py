from Models import Piece

class GoldGeneral(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "G"
        else:
            self.name = "g"

    def availableMoves(self, board):
        print("GoldGeneral implemented")
    
    def doSomething(self):
        super().doSomething()
        print("Now GoldGeneral is doing something!")

if __name__ == "__main__":
    newGoldGeneral = GoldGeneral("lower", 1, 1)
    newGoldGeneral.doSomething()