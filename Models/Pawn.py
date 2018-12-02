from Models import Piece, GoldGeneral
from Functions import isInCheck, checkForPawnInColumn
from SeperateFunctions import isSquareEmpty
import copy

BOARDWIDTH = 5
BOARDHEIGHT = 5

class Pawn(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "P"
        else:
            self.name = "p"

    def availableMoves(self, board):
        moves = []

        #If promoted, moves like a Gold General
        if self.promoted == True:
            moves = GoldGeneral.GoldGeneral(self.player, self.posx, self.posy).availableMoves(board)
            return moves

        if self.player == "lower" and self.isValidMove(self.posx, self.posy + 1, board):
            moves.append((self.posx, self.posy + 1))
        elif self.player == "UPPER" and self.isValidMove(self.posx, self.posy - 1, board):
            moves.append((self.posx, self.posy - 1))
        return moves

    def pawnDropInCheck(self, board):
        copyBoard = copy.deepcopy(board)
        copyBoard[self.posx][self.posy] = self

        if self.player == "lower":
            otherPlayer = "UPPER"
        elif self.player == "UPPER":
            otherPlayer = "lower"

        if isInCheck(otherPlayer, copyBoard):
            return True

        if self.player == "lower" and self.posy == BOARDHEIGHT - 1:
            return True
        elif self.player == "UPPER" and self.posy == 0:
            return True

    def availableDrops(self, board):
        listPos = []
        for i in range(0, 5):
            for j in range(0, 5):
                if isSquareEmpty((i,j), board):
                    if not checkForPawnInColumn(j, board, self.player):
                        if not Pawn(self.player, i, j).pawnDropInCheck(board):
                            listPos.append((i,j))

        return listPos
    
    def doSomething(self):
        super().doSomething()
        if(self.player == "UPPER"):
            print("My String representation is " + self.name.upper())
        else:
            print("My String representation is " + self.name)

if __name__ == "__main__":
    newPawn = Pawn("UPPER", 1, 1)
    newPawn.doSomething()