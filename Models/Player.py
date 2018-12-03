
class Player():

    def __init__(self, name):
        """
            Player object has a name, and keeps track of its captured pieces
        """

        self.name = name
        self.captures = []
    
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
    
        return