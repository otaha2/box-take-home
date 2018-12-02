import Models
import utils
import argparse
import sys
import copy

from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook, Player
from Functions import *
from printingFunctions import *
from FileModeFunctions import *



class Game():

    #Command Line Options
    interactive_mode = False
    file_mode = False
    fname = ""

    def __init__(self):

        self.playerTurn = "lower"
        self.lowerPlayer = Player.Player("lower")
        self.upperPlayer = Player.Player("UPPER")
        self.moveCount = 0
        self.playerInCheck= False
        self.prevMove = ""
        self.Checkmate = False
        self.endedGame = False

        if self.file_mode == False:
            self.initBoard()

    #Set up the object represented board and string board
    def initBoard(self):

        #Board is stored in [Column][Row] Order
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

    def completeFromFile(self):
        f = open(self.fname, "r")

        #Initialize board and player turn
        #Board is stored in [Column][Row] Order
        self.board = [[1] * 5 for i in range(5)]
        self.strBoard = [[""] * 5 for i in range(5)]
        self.playerTurn = "lower"

        #Flags for reading file
        piecesDone = False
        listOneDone = False
        listTwoDone = False

        listOfPossibleMoves = []

        for line in f:
            #New line, go to the next line
            if line == "\n":
                continue
            #2nd list was completed, Do all the moves given in the file
            if listTwoDone:
                if isInCheck(self.playerTurn, self.board):
                    listOfPossibleMoves = printIsInCheck(self)
                    if listOfPossibleMoves == -1:
                        return
                    self.playerInCheck = True
                commandList = getMoveCommand(line)

                #This was put in place because promotedPawnIllegalMoves had a space in front of all lines for some reason
                if "" in commandList:
                    commandList.remove("")

                self.prevMove = ' '.join(commandList)
                #Do the command (move, drop, etc.)
                returnVal = self.handleTurnCommand(commandList)
                #-1 means Illegal move was inputted
                if returnVal == -1:
                    self.returnMessage = " Illegal move."
                    if self.playerTurn == "lower":
                        self.gameWinner = "UPPER"
                    else:
                        self.gameWinner = "lower"
                    self.endedGame = True
                    self.updateTurn()                    
                    self.endGame()
                    return
                #Update whos turn it is before the next turn
                returnVal = self.updateTurn()
                # print("Move count: " + str(self.moveCount))

                if returnVal == -1:
                    return
                
            #Reached the first list means the initialization of pieces on the board are done
            #Initialize UPPER pieces captured
            if not listOneDone and "[" in line:
                piecesDone = True
                listOneDone = True
                initCaptures(self, line, 0)

            #Initialize lower pieces captured
            elif listOneDone == True and "[" in line:
                listTwoDone = True
                initCaptures(self, line, 1)

            #For each piece, initialize the board position with the Piece Object
            if not piecesDone:
                if line == "\n" or line == " \n":
                    piecesDone = True
                    continue
                addPieceToBoard(line, self.board) 

        if isInCheck(self.playerTurn, self.board):
            listOfPossibleMoves = printIsInCheck(self)
            self.playerInCheck = True
        else:
            self.playerInCheck = False

        if self.endedGame != True:
            printBeginTurn(self, listOfPossibleMoves)
            print("")
            print(self.playerTurn + "> ")

        # for col in self.board:
        #     for item in col:
        #         if type(item) == King.King and item.player == "lower":
        #             # print("Piece: " + item.name)
        #             print("Position: " + str((item.posx, item.posy)))
        #             print("Available Moves:")
        #             for move in item.availableMoves(self.board):
        #                 print(move)
                    
    
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

    def parseInput(self, arg1, arg2):
        """
        Helper function to get the indicies on board of current position and end position
        Returns a list containing 2 tuples of X and Y position on board of current and end
        """

        return (fromAlphaToIndex(arg1), fromAlphaToIndex(arg2))

    def move(self, curPos, endPos):
        """Move the piece and update the board"""

        positions = self.parseInput(curPos, endPos)

        # print("Parsed Input: " + str(positions))

        endX = positions[1][0]
        endY = positions[1][1]
        curX = positions[0][0]
        curY = positions[0][1]

        if (endX, endY) not in self.board[curX][curY].availableMoves(self.board):
            # print("Illegal Move")
            # print(self.board[curX][curY].availableMoves(self.board))
            return -1
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

                # #Forced pawn promotion
                # if type(item) == Pawn.Pawn and item.checkForPromotion((curX, curY)) and not item.promoted:
                #     item.promote()
            #End destination has another piece in that square
            elif type(self.board[curX][curY]) != int and self.board[curX][curY].player != self.playerTurn:
                # print("Illegal Move... please move your own piece")
                return -1
        
        #On success return 0
        return 0


    def drop(self, piece, posDrop):
        foundPiece = False
        if self.playerTurn == "lower":
            for item in self.lowerPlayer.captures:
                if piece.lower() == str(item):
                    foundPiece = True
                    if isSquareEmpty(posDrop, self.board):
                        if piece.lower() == "p":
                            if checkForPawnInColumn(posDrop[0], self.board, self.playerTurn) or Pawn.Pawn(self.playerTurn, posDrop[0], posDrop[1]).pawnDropInCheck(self.board):
                                return -1
                        pieceToDrop = item
                        pieceToDrop.name = pieceToDrop.name.lower()
                        pieceToDrop.posx = posDrop[0]
                        pieceToDrop.posy = posDrop[1]
                        pieceToDrop.player = "lower"
                        self.board[posDrop[0]][posDrop[1]] = pieceToDrop
                        self.lowerPlayer.captures.remove(item)
                    else:
                        #Square is not empty
                        return -1
            if foundPiece == False:
                return -1

        elif self.playerTurn == "UPPER":
            for item in self.upperPlayer.captures:
                if piece.upper() == str(item):
                    foundPiece = True
                    if isSquareEmpty(posDrop, self.board):
                        if piece.lower() == "p": 
                            if checkForPawnInColumn(posDrop[0], self.board, self.playerTurn) or Pawn.Pawn(self.playerTurn, posDrop[0], posDrop[1]).pawnDropInCheck(self.board):
                            # print("There is already a  Pawn in this column")
                                return -1
                        pieceToDrop = item
                        pieceToDrop.name = pieceToDrop.name.upper()
                        pieceToDrop.posx = posDrop[0]
                        pieceToDrop.posy = posDrop[1]
                        pieceToDrop.player = "UPPER"
                        self.board[posDrop[0]][posDrop[1]] = pieceToDrop
                        self.upperPlayer.captures.remove(item)
                    else:
                        #Square is not empty
                        return -1
            if foundPiece == False: 
                return -1
        else:
            # print("Invalid Drop")
            return -1
    
    def getInput(self):
        turnInput = input(self.playerTurn + "> ")
        inputList = turnInput.split(" ")
        return inputList

    def updateTurn(self):
        if self.playerTurn == "lower":
            self.playerTurn = "UPPER"

        elif self.playerTurn == "UPPER":
            self.playerTurn = "lower"
        
        if self.endedGame == True:
            return
        
        if self.playerTurn == "lower":
            self.moveCount += 1
            if self.moveCount == 200:
                #Check if checkmate occurred on last move
                returnVal = printIsInCheck(self)
                if returnVal == -1:
                    return -1
                self.returnMessage = "Tie game.  Too many moves."
                self.endedGame = True
                self.endGame()
                return -1
        

    def promotePiece(self, prevPos, curPos):
        """Called when user input promotes piece"""

        positions = self.parseInput(prevPos, curPos)
        prevX = positions[0][0]
        prevY = positions[0][1]
        curX = positions[1][0]
        curY = positions[1][1]

        item = self.board[curX][curY]

        # print("Positions: " + str(positions)) 
        # print("Entering promote: " + str(item.promoted))

        if type(item) != int:
            if item.promoted == True:
                return -1
            piece = item
            newPiece = copy.deepcopy(piece)
            # newPiece.posx = endX
            # newPiece.posy = endY
            canPromote = newPiece.checkForPromotion((prevX, prevY))
            
            if canPromote:
                # print("Entered promote")
                piece.promote()
                return 0
            else:
                # print("Illegal Move... Cannot promote")
                return -1
    
    def handleTurnCommand(self, command):
        """
        Entry point for command --- Just like a sys call :)
        """
        if command[0] == "move":
            positions = self.parseInput(command[1], command[2])

            #Check if piece can be promoted before moving
            #If user says promote, but piece cannot be promoted it is illegal move
            if len(command) > 3 and command[3] == "promote":
                item = self.board[positions[0][0]][positions[0][1]]
                if type(item) != int:
                    newPiece = copy.deepcopy(item)
                    #Move the copied piece to end position
                    newPiece.posx = positions[1][0]
                    newPiece.posy = positions[1][1]
                    canPromote = newPiece.checkForPromotion(positions[0])
                    if canPromote == False:
                        return -1

            #Check if player enters check with their move
            item = self.board[positions[0][0]][positions[0][1]]

            #Copy piece Set copied piece position to endPos
            newPiece = copy.deepcopy(item)
            newPiece.posx = positions[1][0]
            newPiece.posy = positions[1][1]

            #Copy board and surface level move the piece to endPos
            copyBoard = copy.deepcopy(self.board)
            copyBoard[positions[0][0]][positions[0][1]] = 1
            copyBoard[positions[1][0]][positions[1][1]] = newPiece

            #If copied board is in check
            if isInCheck(self.playerTurn, copyBoard):
                return -1

            #Move piece           
            returnVal = self.move(command[1], command[2])
            if returnVal == -1:
                return -1

            

            #If move successful, check for forced pawn
            if returnVal == 0:
                returnVal = checkForcedPawnPromote(self.board, positions)
                if returnVal == 1:
                    return
            #Do the promotion
            if len(command) > 3 and command[3] == "promote":
                returnVal = self.promotePiece(command[1], command[2])
                if returnVal == -1:
                    #Invert the move
                    # self.move(command[2], command[1])
                    return -1
        if command[0] == "drop":
            #Get the piece value to drop, and index position from input command
            pieceToDrop = command[1]
            dropLocation = command[2]

            dropLocationX = dropLocation[0]
            dropLocationX = map_from_alpha_to_index[dropLocationX]
            dropLocationY = int(dropLocation[1]) - 1

            returnVal = self.drop(pieceToDrop, (dropLocationX, dropLocationY))
            if returnVal == -1:
                return -1

    def endGame(self):
        """
        End the game
        """
        self.endedGame = True
        if self.file_mode == True:
            printBeginTurn(self, [])
            print("")

        if self.returnMessage == "Tie game.  Too many moves.":
            print(self.returnMessage)
            return
        else:    
            print(self.gameWinner + " player wins. " + self.returnMessage)
                

    def gameLoop(self):
        playerIsInCheck = 0
        alphaPossibleMoves = []
        while 1:
            #Do check detection
            # possibleKingMoves = checkDetection(self.playerTurn, self.board)
            # if type(possibleKingMoves) == list:
            #     isInCheck = 1
            #     print(self.playerTurn + " player is in check!")
            #     print("Available moves:")
            #     self.printPossibleKingMoves(possibleKingMoves)

            #Check if the king exists
            king = findKing(self.playerTurn, self.board)
            if type(king) == bool and king == False:
                self.returnMessage = "Checkmate."
                if self.playerTurn == "lower":
                    self.gameWinner = "UPPER"
                else:
                    self.gameWinner = "lower"
                    self.endGame()
                    return

            if self.playerTurn == "lower" and self.moveCount == 200:
                self.returnMessage = "Tie game. Too many moves."
                self.endGame()

            #Check detection at the beginning of every turn
            if isInCheck(self.playerTurn, self.board):
                self.playerInCheck = True
                playerIsInCheck = 1
                possibleMoves = getPossibleMovesOutCheck(self.playerTurn, self.board)
                if len(possibleMoves) == 0:
                    if self.playerTurn == "lower":
                        self.gameWinner = "UPPER"
                    else:
                        self.gameWinner = "lower"
                    self.returnMessage = "Checkmate."
                    self.endGame()
                    return
                else:
                    alphaPossibleMoves = ListPossibleCheckMoves(self, possibleMoves)
            else:
                #Otherwise not in check, continue on normally
                alphaPossibleMoves = []
                self.playerInCheck = False
                pass

            #Print the beginning of the turn, wait for user input
            printBeginTurn(self, alphaPossibleMoves)
            #Get the user command
            commandList = self.getInput()
            #IF the player is in check and they do a move other than the moves given, then they lose (Illegal Move)
            if playerIsInCheck and " ".join(commandList) not in alphaPossibleMoves:
                self.returnMessage = "Illegal move."
                if self.playerTurn == "lower":
                    self.gameWinner = "UPPER"
                else:
                    self.gameWinner = "lower"
                    self.endGame()
                    return

            #Print the command
            self.prevMove = " ".join(commandList)
            #Do the command (move, drop, etc.)
            returnVal = self.handleTurnCommand(commandList)
            #-1 means Illegal move was inputted
            if returnVal == -1:
                self.returnMessage = "Illegal move."
                self.endGame()
                return
            #Update whos turn it is before the next turn
            self.updateTurn()
      


if __name__ == "__main__":
    newGame = Game()
    newGame.defineCLIOptions()

    # newGame.gameLoop()
    newGame.completeFromFile()
