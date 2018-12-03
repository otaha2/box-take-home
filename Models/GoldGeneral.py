from Models import Piece

class GoldGeneral(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "G"
        else:
            self.name = "g"

    def availableMoves(self, board):
        """
            GoldGeneral Implementation of avaialbleMoves
            returns:    list of possible endPos the GoldGeneral can go to
        """
        moves = []
        for x,y in self.goldGeneralList(self.posx, self.posy):
            if self.isValidMove(x, y, board):
                moves.append((x, y))
        return moves
    
    def checkForPromotion(self, prevPos):
        #GoldGeneral cannot be promoted
        return False

    def goldGeneralList(self, x, y):
        """
            Called in availableMoves
            Defines the move patterns for a GoldGeneral
            returns:    a list of possible endPos relative to current pos of the GoldGeneral
        """
        if self.player == "UPPER":
            return [(x + 1, y), (x, y - 1), (x - 1, y), (x - 1, y -1), (x, y + 1), (x + 1, y -1)]
        elif self.player == "lower":
            return [(x + 1, y), (x, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]