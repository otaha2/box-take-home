from Models import Piece, GoldGeneral

class SilverGeneral(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "S"
        else:
            self.name = "s"

    def availableMoves(self, board):
        """
            SilverGeneral Implementation of availableMoves
            returns:    list of possible endPositions the SilverGeneral can go to
        """

        moves = []

        #If promoted, SilverGeneral can only move like a Gold General
        if self.promoted == True:
            moves = GoldGeneral.GoldGeneral(self.player, self.posx, self.posy).availableMoves(board)
            return moves
        
        for x,y in self.silverGeneralList(self.posx, self.posy):
            if self.isValidMove(x, y, board):
                moves.append((x, y))
        
        return moves

    def silverGeneralList(self, x, y):
        """
            Called in availableMoves
            Defines the move patterns for a SilverGeneral
            returns:    a list of possible endPos relative to current pos of the SilverGeneral
        """
        if self.player == "UPPER":
            return [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
        elif self.player == "lower":
            return [(x + 1, y - 1), (x - 1, y - 1), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
