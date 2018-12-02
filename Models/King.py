from Models import Piece

class King(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "K"
        else:
            self.name = "k"
    
    def availableMoves(self, board):
        moves = []
        for x,y in kingList(self.posx, self.posy):
            if self.isValidMove(x, y, board):
                moves.append((x, y))
        return moves
    
    def doSomething(self):
        super().doSomething()
        print("Now King is doing something!")

    def checkForPromotion(self, prevPos):
        return False

def kingList(x, y):
    return [(x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

if __name__ == "__main__":
    newKing = King("lower", 1, 1)