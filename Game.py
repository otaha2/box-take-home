import Models
import utils as u
import argparse
import sys

from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook, Player
from Functions import *

#Dictionary to translate from alpha to index and Vice Versa
map_from_alpha_to_index = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4}
map_from_index_to_alpha = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}

class Game():

    #Command Line Options
    interactive_mode = False
    file_mode = False
    fname = ""

    def __init__(self):

        self.playerTurn = "lower"
        self.initBoard()
        self.lowerPlayer = Player.Player("lower")
        self.upperPlayer = Player.Player("UPPER")

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
        
    #Used for testing... use provided Utility Method instead of this
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

    def printBeginTurn(self):
        newGame.refreshStrBoard()
        strB = u.stringifyBoard(newGame.strBoard)
        print(strB)

        print("Captures UPPER:", end="")
        for item in self.upperPlayer.captures:
            print(" " + str(item), end="")
        
        print("")
        print("Captures lower:", end="")
        for item in self.lowerPlayer.captures:
            print(" " + str(item), end="")

        print("")

    
    def parseInput(self, arg1, arg2):
        """
        Helper function to get the indicies on board of current position and end position
        Returns a list containing 2 tuples of X and Y position on board of current and end
        """

        curX = arg1[0]
        curX = map_from_alpha_to_index[curX]
        curY = int(arg1[1]) - 1
        endX = arg2[0]
        endX = map_from_alpha_to_index[endX]
        endY = int(arg2[1]) - 1

        return [(curX, curY), (endX, endY)]

    def move(self, curPos, endPos):
        """Move the piece and update the board"""

        positions = self.parseInput(curPos, endPos)

        endX = positions[1][0]
        endY = positions[1][1]
        curX = positions[0][0]
        curY = positions[0][1]

        if (endX, endY) not in self.board[curX][curY].availableMoves(self.board):
            print("Illegal Move")
        else:
            #Empty end destination and make sure current is an object to dereference
            if type(self.board[curX][curY]) != int and self.board[curX][curY].player == self.playerTurn:
                if (self.board[endX][endY] != 1):
                    if self.playerTurn == "lower":
                        self.lowerPlayer.addCapture(self.board[endX][endY])
                    else:
                        self.upperPlayer.addCapture(self.board[endX][endY])
                item = self.board[curX][curY]
                item.posx = endX
                item.posy = endY
                self.board[endX][endY] = item
                self.board[curX][curY] = 1
            #End destination has another piece in that square
            elif type(self.board[curX][curY]) != int and self.board[curX][curY].player != self.playerTurn:
                print("Illegal Move... please move your own piece")
        

    def drop(self, piece, posDrop):
        # print("Piece to drop: " + piece)
        # print("Position to drop: " + str(posDrop))
        # print("Is piece in lower captures: " + str(piece. in self.lowerPlayer.captures))
        if self.playerTurn == "lower":
            for item in self.lowerPlayer.captures:
                if piece.upper() == str(item) and isSquareEmpty(posDrop, self.board):
                    pieceToDrop = item
                    pieceToDrop.name = pieceToDrop.name.lower()
                    pieceToDrop.posx = posDrop[0]
                    pieceToDrop.posy = posDrop[1]
                    pieceToDrop.player = "lower"
                    self.board[posDrop[0]][posDrop[1]] = pieceToDrop
                    self.lowerPlayer.captures.remove(item)
        if self.playerTurn == "UPPER":
            for item in self.upperPlayer.captures:
                if piece.lower() == str(item) and isSquareEmpty(posDrop, self.board):
                    pieceToDrop = item
                    pieceToDrop.name = pieceToDrop.name.upper()
                    pieceToDrop.posx = posDrop[0]
                    pieceToDrop.posy = posDrop[1]
                    pieceToDrop.player = "UPPER"
                    self.board[posDrop[0]][posDrop[1]] = pieceToDrop
                    self.upperPlayer.captures.remove(item)
        else:
            print("Invalid Drop")
    
    def getInput(self):
        turnInput = input(self.playerTurn + "> ")
        inputList = turnInput.split(" ")
        return inputList

    def updateTurn(self):
        if self.playerTurn == "lower":
            self.playerTurn = "UPPER"

        elif self.playerTurn == "UPPER":
            self.playerTurn = "lower"

    def promotePiece(self, endPos):
        """Called when user input promotes piece"""

        positions = self.parseInput("a1", endPos)
        posX = positions[1][0]
        posY = positions[1][1]

        if type(self.board[posX][posY]) != int:
            piece = self.board[posX][posY]
            canPromote = piece.checkForPromotion()
            if canPromote:
                piece.promote()
            else:
                print("Illegal Move... Cannot promote")
    
    def handleTurnCommand(self, command):

        if command[0] == "move":
            self.move(command[1], command[2])
            if len(command) > 3 and command[3] == "promote":
                self.promotePiece(command[2])
        if command[0] == "drop":
            #Get the piece value to drop, and index position from input command
            pieceToDrop = command[1]
            dropLocation = command[2]

            dropLocationX = dropLocation[0]
            dropLocationX = map_from_alpha_to_index[dropLocationX]
            dropLocationY = int(dropLocation[1]) - 1

            self.drop(pieceToDrop, (dropLocationX, dropLocationY))
        
                

    def gameLoop(self):
        while 1:
            #Print the beginning of the turn, wait for user input
            self.printBeginTurn()
            commandList = self.getInput()

            self.handleTurnCommand(commandList)
            self.updateTurn()

            



    
            


if __name__ == "__main__":
    newGame = Game()
    newGame.defineCLIOptions()

    # newGame.board[1][2] = Pawn.Pawn("lower", 1, 2)
    # newGame.board[2][3] = Bishop.Bishop("UPPER", 2, 3)

    newGame.gameLoop()

    # for col in newGame.board:
    #     for item in col:
    #         if type(item) == Models.Bishop.Bishop:
    #             print("My player is: " + item.player)
    #             print("My current Position is: " + str((item.posx, item.posy)))
    #             print(item.availableMoves(newGame.board))
    #             print("")




    # print("UPPER player captures: ")
    # for item in newGame.upperPlayer.captures:
    #     print(item)
    # print("")

    # positions = newGame.parseInput("d5", "c4")
    # newGame.move(positions[0], positions[1])
    # newGame.printBeginTurn()

    # positions = newGame.parseInput("e1", "e4")
    # newGame.move(positions[0], positions[1])
    # newGame.printBeginTurn()

    # positions = newGame.parseInput("a5", "a2")
    # newGame.move(positions[0], positions[1])
    # newGame.printBeginTurn()

    # newGame.board[1][4].promote()
    # print("Available moves for a Promoted Bishop: ")
    # print(newGame.board[1][4].availableMoves(newGame.board))
