import Piece

class GoldGeneral(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        self.name = "g"

    def availableMoves(self, posx, posy, board):
        print("GoldGeneral implemented")
    
    def doSomething(self):
        super().doSomething()
        print("Now GoldGeneral is doing something!")

if __name__ == "__main__":
    newGoldGeneral = GoldGeneral("lower", 1, 1)
    newGoldGeneral.doSomething()