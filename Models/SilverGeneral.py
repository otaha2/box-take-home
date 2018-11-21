from Models import Piece

class SilverGeneral(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "S"
        else:
            self.name = "s"

    def availableMoves(self, board):
        moves = []
        for x,y in self.silverGeneralList(self.posx, self.posy):
            if self.isValidMove(x, y, board):
                moves.append((x, y))
        return moves
    
    def doSomething(self):
        super().doSomething()
        print("Now SilverGeneral is doing something!")

    def silverGeneralList(self, x, y):
        if self.player == "UPPER":
            return [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
        elif self.player == "lower":
            return [(x + 1, y - 1), (x - 1, y - 1), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

if __name__ == "__main__":
    newSilverGeneral = SilverGeneral("lower", 1, 1)
    newSilverGeneral.doSomething()