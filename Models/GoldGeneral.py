from Models import Piece

class GoldGeneral(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "G"
        else:
            self.name = "g"

    def availableMoves(self, board):
        moves = []
        for x,y in self.goldGeneralList(self.posx, self.posy):
            if self.isValidMove(x, y, board):
                moves.append((x, y))
        return moves
    
    def doSomething(self):
        super().doSomething()
        print("Now GoldGeneral is doing something!")

    def goldGeneralList(self, x, y):
        if self.player == "UPPER":
            return [(x + 1, y), (x, y - 1), (x - 1, y), (x - 1, y -1), (x, y + 1), (x + 1, y -1)]
        elif self.player == "lower":
            return [(x + 1, y), (x, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

if __name__ == "__main__":
    newGoldGeneral = GoldGeneral("lower", 1, 1)
    newGoldGeneral.doSomething()