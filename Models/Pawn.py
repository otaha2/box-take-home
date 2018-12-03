from Models import Piece, GoldGeneral
from Functions import isInCheck, checkForPawnInColumn
from isSquareEmpty import isSquareEmpty
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
        """
            Pawn Implementation of avaialbleMoves
            returns:    list of possible endPos the Pawn can go to
        """
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
        """
            Unique to the pawn in that the pawn cannot be dropped into a position that would result in an immediate check
            Also cannot be dropped directly in the promotion zone
            returns:    True if pawn drop will result in check or is in promotion zone
                        False if not
        """
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
        """
            Defines all places the pawn can be dropped in
            returns:    list of possible positions paw can be dropped in
        """
        listPos = []
        for i in range(0, 5):
            for j in range(0, 5):
                #Empty Square
                if isSquareEmpty((i,j), board):
                    #There cannot be another pawn in the same column
                    if not checkForPawnInColumn(j, board, self.player):
                        #Pawn cannot be dropped in immediate checkmate or in promotion zone
                        if not Pawn(self.player, i, j).pawnDropInCheck(board):
                            listPos.append((i,j))

        return listPos