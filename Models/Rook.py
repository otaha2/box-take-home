from Models import Piece, King

class Rook(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "R"
        else:
            self.name = "r"

    def availableMoves(self, board):
        """
            Rook Implementation of availableMoves
            returns:    list of possible endPositions the Rook can go to
        """
        moves = []
        for i in range(1, 5):
            if self.isValidMove(self.posx + i, self.posy, board) and self.isPathOpen(self.posx + i, self.posy, board):
                moves.append((self.posx + i, self.posy))

            if self.isValidMove(self.posx - i, self.posy, board) and self.isPathOpen(self.posx - i, self.posy, board):
                moves.append((self.posx - i, self.posy))

            if self.isValidMove(self.posx, self.posy + i, board) and self.isPathOpen(self.posx, self.posy + i, board):
                moves.append((self.posx, self.posy + i))

            if self.isValidMove(self.posx, self.posy - i, board) and self.isPathOpen(self.posx, self.posy - i, board):
                moves.append((self.posx, self.posy - i))

        #Promoted Rooks move like a Rook OR a King.
        if self.promoted == True:
            #Get all available moves for a king in the same position of the Bishop
            kingMoves = King.King(self.player, self.posx, self.posy).availableMoves(board)
            for item in kingMoves:
                #If the move is not already included in the Rook moves, add it to the list of moves
                if item not in moves:
                    moves.append(item)

        return moves

    def isPathOpen(self, x, y, board):
        """
            Check if path to end Pos is clear of any other pieces
            returns:    True if path is clear
                        False if path is not clear
        """
        if self.posy > y and self.posx == x:
            #Check if path Down is open (from the view of the lower player)
            for i in range(y + 1, self.posy):
                if board[self.posx][i] != 1:
                    return False

        if self.posy < y and self.posx == x:
            #Check if path Up is open (from the view of the lower player)
            for i in range(self.posy + 1, y):
                if board[self.posx][i] != 1:
                    return False

        if self.posx > x and self.posy == y:
            #Check if path Left is open
            for i in range(x + 1, self.posx):
                if board[i][self.posy] != 1:
                    return False

        if self.posx < x and self.posy == y:
            #Check if path Right is open
            for i in range(self.posx + 1, x):
                if board[i][self.posy] != 1:
                    return False
        return True
            