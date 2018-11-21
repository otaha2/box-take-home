import Models

from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook

class Game():

    chess_map_from_alpha_to_index = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4}
    chess_map_from_index_to_alpha = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}


    def __init__(self):
        self.playerTurn = "lower"
        self.initBoard()

    def initBoard(self):
        #Board is stored in Row-Column Order
        self.board = [[1] * 5 for i in range(5)]
        self.board[1][0] = Pawn.Pawn("lower", 0, 1)
        self.board[3][4] = Pawn.Pawn("UPPER", 4, 3)
        pieceOnBoard = ["k", "g", "s", "b", "r"]
        for i in range(5):
            if pieceOnBoard[i] == "k":
                self.board[0][i] = King.King("lower", i, 0)
                self.board[4][4-i] = King.King("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "g":
                self.board[0][i] = GoldGeneral.GoldGeneral("lower", i, 0)
                self.board[4][4-i] = GoldGeneral.GoldGeneral("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "s":
                self.board[0][i] = SilverGeneral.SilverGeneral("lower", i, 0)
                self.board[4][4-i] = SilverGeneral.SilverGeneral("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "b":
                self.board[0][i] = Bishop.Bishop("lower", i, 0)
                self.board[4][4-i] = Bishop.Bishop("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "r":
                self.board[0][i] = Rook.Rook("lower", i, 0)
                self.board[4][4-i] = Rook.Rook("UPPER", 4-i, 4)
        

    def printBoard(self):
        for i in range(5):
            row = self.board[4-i]
            for item in row:
                if(item == 1):
                    print("_", end=" ")
                else:
                    print(item, end=" ")
            print("")

if __name__ == "__main__":
    newGame = Game()
    newGame.printBoard()