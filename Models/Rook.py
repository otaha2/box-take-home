from Models import Piece

class Rook(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "R"
        else:
            self.name = "r"

    def availableMoves(self, board):
        moves = []
        for i in range(1, 5):
            if self.isValidMove(self.posx + i, self.posy, board):
                moves.append((self.posx + i, self.posy))
            elif self.isValidMove(self.posx - i, self.posy, board):
                moves.append((self.posx - i, self.posy))
            elif self.isValidMove(self.posx, self.posy + i, board):
                moves.append((self.posx, self.posy + i))
            elif self.isValidMove(self.posx, self.posy - i, board):
                moves.append((self.posx, self.posy - i))
        return moves
            
        
    
    def doSomething(self):
        super().doSomething()
        print("Now Rook is doing something!")

if __name__ == "__main__":
    newRook = Rook("lower", 1, 1)
    newRook.doSomething()