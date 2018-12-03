from Models import Piece

class King(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "K"
        else:
            self.name = "k"
    
    def availableMoves(self, board):
        """
            King Implementation of avaialbleMoves
            returns:    list of possible endPos the King can go to
        """
        moves = []
        for x,y in kingList(self.posx, self.posy):
            if self.isValidMove(x, y, board):
                moves.append((x, y))
        return moves

    def checkForPromotion(self, prevPos):
        #King cannot be promoted
        return False

def kingList(x, y):
    """
        Called in availableMoves
        Defines the move patterns for a King
        returns:    a list of possible endPos relative to current pos of the King
    """
    return [(x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
