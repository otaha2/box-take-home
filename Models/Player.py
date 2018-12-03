#Is this needed?

class Player():

    def __init__(self, name):

        self.name = name
        self.captures = []
        self.numMoves = 0
    
    def addCapture(self, piece):
        """
            Add a piece to the list of captured pieces
        """

        #All captured pieces will start off unpromoted
        if piece.promoted == True:
            piece.promoted = False
            piece.name = piece.name[1]
            piece.player = self.name
        if self.name == "lower":
            piece.name = piece.name.lower()
        else:
            piece.name = piece.name.upper()
        self.captures.append(piece)