from Models import Piece, King

class Bishop(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "B"
        else:
            self.name = "b"

    def availableMoves(self, board):
        moves = []
        # print("Bishop Position: " + str((self.posx, self.posy)))
        for i in range(1, 5):
            # print("Position " + str((self.posx - i, self.posy - i)) + " : " + str(self.isValidMove(self.posx - i, self.posy - i, board)))
            if self.isValidMove(self.posx + i, self.posy + i, board) and self.isPathOpen(self.posx + i, self.posy + i, board):
                moves.append((self.posx + i, self.posy + i))

            if self.isValidMove(self.posx + i, self.posy - i, board) and self.isPathOpen(self.posx + i, self.posy - i, board):
                moves.append((self.posx + i, self.posy - i))

            if self.isValidMove(self.posx - i, self.posy + i, board) and self.isPathOpen(self.posx - i, self.posy + i, board):
                moves.append((self.posx - i, self.posy + i))

            if self.isValidMove(self.posx - i, self.posy - i, board) and self.isPathOpen(self.posx - i, self.posy - i, board):
                moves.append((self.posx - i, self.posy - i))

        #Promoted Bishops move like a Bishop OR a King.
        if self.promoted == True:
            #Get all available moves for a king in the same position of the Bishop
            kingMoves = King.King(self.player, self.posx, self.posy).availableMoves(board)
            for item in kingMoves:
                #If the move is not already included in the Bishop moves, add it to the list of moves
                if item not in moves:
                    moves.append(item)

        return moves

    def isPathOpen(self, x, y, board):
        if self.posy > y and self.posx > x:
            #Check if path DownLeft is open (from the view of the lower player)
            for i, j in zip(range(self.posx - 1, x, -1), range(self.posy - 1, y, -1)):
                # print("Position " + str((i, j)) + " : " + str(board[i][j]))
                if board[i][j] != 1:
                    return False

        if self.posy > y and self.posx < x:
            #Check if path DownnRight is open (from the view of the lower player)
            for i, j in zip(range(self.posx + 1, x, 1), range(self.posy - 1, y, -1)):
                if board[i][j] != 1:
                    return False

        if self.posy < y and self.posx > x:
            #Check if path UpLeft is open
            for i, j in zip(range(self.posx - 1, x, -1), range(self.posy + 1, y, 1)):
                if board[i][j] != 1:
                    return False

        if self.posy < y and self.posx < x:
            #Check if path UpRight is open
            for i, j in zip(range(self.posx + 1, x, 1), range(self.posy + 1, y, 1)):
                if board[i][j] != 1:
                    return False
        return True
    
    def doSomething(self):
        super().doSomething()
        print("Now Bishop is doing something!")

if __name__ == "__main__":
    newBishop = Bishop("lower", 1, 1)
    newBishop.doSomething()