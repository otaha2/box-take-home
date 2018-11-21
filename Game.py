import Models
import utils as u
import argparse
import sys

from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook

class Game():

    #Command Line Options
    interactive_mode = False
    file_mode = False
    fname = ""

    #Dictionary to translate from alpha to index and Vice Versa
    chess_map_from_alpha_to_index = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4}
    chess_map_from_index_to_alpha = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}


    def __init__(self):

        self.playerTurn = "lower"
        self.initBoard()
        self.lowerPlayerMoveCount = 0
        self.upperPlayerMoveCount = 0

    #Set up the object represented board and string board
    def initBoard(self):

        #Board is stored in Row-Column Order
        self.board = [[1] * 5 for i in range(5)]
        self.strBoard = [[""] * 5 for i in range(5)]

        #Set the pawns for each player
        self.board[0][1] = Pawn.Pawn("lower", 0, 1)
        self.board[4][3] = Pawn.Pawn("UPPER", 4, 3)

        #Used to set the order of pieces on the board
        pieceOnBoard = ["k", "g", "s", "b", "r"]
        for i in range(5):
            if pieceOnBoard[i] == "k":
                self.board[i][0] = King.King("lower", i, 0)
                self.board[4-i][4] = King.King("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "g":
                self.board[i][0] = GoldGeneral.GoldGeneral("lower", i, 0)
                self.board[4-i][4] = GoldGeneral.GoldGeneral("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "s":
                self.board[i][0] = SilverGeneral.SilverGeneral("lower", i, 0)
                self.board[4-i][4] = SilverGeneral.SilverGeneral("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "b":
                self.board[i][0] = Bishop.Bishop("lower", i, 0)
                self.board[4-i][4] = Bishop.Bishop("UPPER", 4-i, 4)
            elif pieceOnBoard[i] == "r":
                self.board[i][0] = Rook.Rook("lower", i, 0)
                self.board[4-i][4] = Rook.Rook("UPPER", 4-i, 4)
    
    #Refresh the string representation of board from the object representation of board
    def refreshStrBoard(self):

        # i represents row
        for i in range(5):
            # j represents col
            for j in range(5):
                if(self.board[i][j] != 1):
                    self.strBoard[i][j] = str(self.board[i][j])
                else:
                    self.strBoard[i][j] = ""
        
    #Used for testing... used provided Utility Method
    def printBoard(self):

        for i in range(5):
            row = self.board[4-i]
            for item in row:
                if(item == 1):
                    print("_", end=" ")
                else:
                    print(item, end=" ")
            print("")


    def defineCLIOptions(self):
        if len(sys.argv) > 1:
            if sys.argv[1] == "-i":
                self.interactive_mode = True
                
            elif sys.argv[1] == "-f":
                self.file_mode = True
                self.fname = sys.argv[2]
            


if __name__ == "__main__":
    newGame = Game()
    newGame.defineCLIOptions()

    newGame.board[1][2] = Pawn.Pawn("lower", 1, 2)
    newGame.board[2][2] = Rook.Rook("UPPER", 2, 2)

    newGame.refreshStrBoard()
    strB = u.stringifyBoard(newGame.strBoard)
    print(strB)

    for col in newGame.board:
        for item in col:
            if type(item) == Models.Rook.Rook:
                print("My player is: " + item.player)
                print("My current Position is: " + str((item.posx, item.posy)))
                print(item.availableMoves(newGame.board))
                print("")
