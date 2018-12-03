import Models
import utils
import argparse
import sys
import copy

from Models import Pawn, King, GoldGeneral, SilverGeneral, Bishop, Rook, Player
from Functions import *
from printingFunctions import *
from FileModeFunctions import *
from isSquareEmpty import isSquareEmpty


class Game():
    """
        Game object is the object that runs the entire miniShogi game. It contains all game information, game flow, game rules, etc
    """

    #Command Line Options
    interactive_mode = False
    file_mode = False
    fname = ""

    def __init__(self):
        """
            The game stores:
                a 2-D Array called board. board contains either 1 for empty space or the piece object for a speicifc sqaure.
                a 2-D Array called strBoard. strBoard has the string representation of board "" for empty space, and "p" for a Pawn
                2 player objects which keep track of their captures
                Number of moves made in moveCount
                prevMove to keep track of last move made
                playerInCheck. flag for when a player is in check
                Checkmate. flag for a checkmate
                endedGame. flag used in endGame signaling the game has ended. used so specific things do not happen if the game has already ended
                flags for file mode game or interative mode
                fname. file path passed in as input for file mode

        """
        #Intialize game object
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
        
        return

    #Set up the object represented board and string board
    def initBoard(self):
        """
            Initialize both the piece representation of board and string representation of board
            Add pieces to board
        """

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
            
        return

    def refreshStrBoard(self):
        """
            Refreshes the string representation of board from the object representation of board
            1 --> ""
            Pawn Object --> "p" or "P"
        """

        # i represents row
        for i in range(5):
            # j represents col
            for j in range(5):
                if(self.board[i][j] != 1):
                    self.strBoard[i][j] = str(self.board[i][j])
                else:
                    self.strBoard[i][j] = ""
                
        return

    def defineCLIOptions(self):
        """
            Use system arguments to define Command Line Interface options
        """
        if len(sys.argv) > 1:
            if sys.argv[1] == "-i":
                self.interactive_mode = True
                
            elif sys.argv[1] == "-f":
                self.file_mode = True
                self.fname = sys.argv[2]
        
        return

    def getInput(self):
        """
            Prompt User for input
        """
        turnInput = input(self.playerTurn + "> ")
        inputList = turnInput.split(" ")
        return inputList

    def move(self, curPos, endPos):
        """
        Move the piece and update the board
        Input:      curPos --- current Position of the piece to be moved
                    endPos --  end Position of the piece to be moved
        Returns:    -1 on error
                    0 on success
        """

        #Get the index representation of the positions
        positions = parseInput(curPos, endPos)

        endX = positions[1][0]
        endY = positions[1][1]
        curX = positions[0][0]
        curY = positions[0][1]

        #endPosition is not possible for this piece
        if (endX, endY) not in self.board[curX][curY].availableMoves(self.board):
            return -1

        else:
            #Empty out the end destination and make sure item at current position is a piece object (or not an int)
            if type(self.board[curX][curY]) != int and self.board[curX][curY].player == self.playerTurn:
                #Add a capture
                if (self.board[endX][endY] != 1):
                    if self.playerTurn == "lower":
                        self.lowerPlayer.addCapture(self.board[endX][endY])
                    else:
                        self.upperPlayer.addCapture(self.board[endX][endY])
                #Update board and piece
                item = self.board[curX][curY]
                item.posx = endX
                item.posy = endY
                self.board[endX][endY] = item
                self.board[curX][curY] = 1

            #Attempting to move a player that is not yours
            elif type(self.board[curX][curY]) != int and self.board[curX][curY].player != self.playerTurn:
                return -1
        
        #On success return 0
        return 0


    def drop(self, piece, posDrop):
        """
            Drop a piece on the board
            Input:      piece   --- string representation of the piece to drop ex: "p" means drop a Pawn
                        posDrop --- position to drop on the board
            Returns:    0 on success
                        -1 on failure
        """
        foundPiece = False
        if self.playerTurn == "lower":
            for item in self.lowerPlayer.captures:
                if piece.lower() == str(item):
                    #Piece is in captures list
                    foundPiece = True
                    if isSquareEmpty(posDrop, self.board):
                        #Can only drop a pawn if there is not another pawn in the col, no immediate check, or promotion zone
                        if piece.lower() == "p":
                            if checkForPawnInColumn(posDrop[0], self.board, self.playerTurn) or Pawn.Pawn(self.playerTurn, posDrop[0], posDrop[1]).pawnDropInCheck(self.board):
                                return -1
                        #drop the piece and update its piece values with position and player
                        pieceToDrop = item
                        pieceToDrop.name = pieceToDrop.name.lower()
                        pieceToDrop.posx = posDrop[0]
                        pieceToDrop.posy = posDrop[1]
                        pieceToDrop.player = "lower"
                        #update the board
                        self.board[posDrop[0]][posDrop[1]] = pieceToDrop
                        #remove from captures list
                        self.lowerPlayer.captures.remove(item)
                        return 0
                    else:
                        #Square is not empty
                        return -1
            if foundPiece == False:
                return -1

        elif self.playerTurn == "UPPER":
            for item in self.upperPlayer.captures:
                if piece.upper() == str(item):
                    #Piece is in captures list
                    foundPiece = True
                    if isSquareEmpty(posDrop, self.board):
                        #Can only drop a pawn if there is not another pawn in the col, no immediate check, or promotion zone
                        if piece.lower() == "p": 
                            if checkForPawnInColumn(posDrop[0], self.board, self.playerTurn) or Pawn.Pawn(self.playerTurn, posDrop[0], posDrop[1]).pawnDropInCheck(self.board):
                                return -1
                         #drop the piece and update its piece values with position and player
                        pieceToDrop = item
                        pieceToDrop.name = pieceToDrop.name.upper()
                        pieceToDrop.posx = posDrop[0]
                        pieceToDrop.posy = posDrop[1]
                        pieceToDrop.player = "UPPER"
                        #update the board
                        self.board[posDrop[0]][posDrop[1]] = pieceToDrop
                        #remove from captures list
                        self.upperPlayer.captures.remove(item)
                        return 0
                    else:
                        #Square is not empty
                        return -1
            if foundPiece == False: 
                return -1
        
        return -1

    def handleTurnCommand(self, command):
        """
        Entry point for command --- Just like a sys call :)
        Input:      command --- ["move", "a1", "a2"]
        Returns:    0 on success
                    -1 on failure
        """
        if command[0] == "move":
            positions = parseInput(command[1], command[2])

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

            #Copy piece and Set the copied piece position to endPos
            newPiece = copy.deepcopy(item)
            newPiece.posx = positions[1][0]
            newPiece.posy = positions[1][1]

            #Copy the board and set the endPos on the board to the copied piece
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
        
        #Drop takes a turn
        if command[0] == "drop":
            #Get the piece value to drop, and index position from input command
            pieceToDrop = command[1]
            dropLocation = command[2]

            dropLocationX = dropLocation[0]
            dropLocationX = map_from_alpha_to_index[dropLocationX]
            dropLocationY = int(dropLocation[1]) - 1
            #Drop the piece
            returnVal = self.drop(pieceToDrop, (dropLocationX, dropLocationY))
            if returnVal == -1:
                return -1

        return 0

    def promotePiece(self, prevPos, curPos):
        """
        Called when user input promotes piece
        Returns:    0 if piece promoted
                    -1 if Illegal move
        """
        #Get index value of positions
        positions = parseInput(prevPos, curPos)
        prevX = positions[0][0]
        prevY = positions[0][1]
        curX = positions[1][0]
        curY = positions[1][1]

        #Get the item
        item = self.board[curX][curY]

        #Item must be a piece object (or not an int in this case)
        if type(item) != int:
            if item.promoted == True:
                return -1
            piece = item
            #Copy the piece and check if the piece can be promoted
            newPiece = copy.deepcopy(piece)
            canPromote = newPiece.checkForPromotion((prevX, prevY))
            
            if canPromote:
                piece.promote()
                return 0
            else:
                return -1
            
        #Item is not a piece... Illegal move
        return -1
    
    def updateTurn(self):
        """
            Called at the end of every turn
            updates playerTurn
            Increments moveCount
            Returns:    0 if updated fine
                        -1 if Tie Game or checkmate occured on last turn
        """

        #Update whos turn it is
        if self.playerTurn == "lower":
            self.playerTurn = "UPPER"
        elif self.playerTurn == "UPPER":
            self.playerTurn = "lower"
        
        #Game has already been updated... return
        if self.endedGame == True:
            return 0
        
        #Increment moveCount
        if self.playerTurn == "lower":
            self.moveCount += 1
            if self.moveCount == 200:
                #Check if checkmate occurred on last move
                returnVal = printIsInCheck(self)
                if returnVal == -1:
                    return -1
                #Checkmate did not occur... Tie Game
                self.returnMessage = "Tie game.  Too many moves."
                self.endedGame = True
                self.endGame()
                return -1
        
        return 0

    def endGame(self):
        """
        End the game
        For File Mode: print beginning of the turn
        print end game message
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
        
        return


    def completeFromFile(self):
        """
            File Mode Game
            Parses input file, initializes game state, and does all the moves specified
        """

        #Initialize board and player turn
        #Board is stored in [Column][Row] Order
        self.board = [[1] * 5 for i in range(5)]
        self.strBoard = [[""] * 5 for i in range(5)]
        self.playerTurn = "lower"

        #Initialize list used to get possible moves out of check
        listOfPossibleMoves = []

        #Call parseTestCase to get input
        parsedFileInput = utils.parseTestCase(self.fname)
        #Assign lists for relevant information
        listOfPieces = parsedFileInput["initialPieces"]
        upperCaptures = parsedFileInput["upperCaptures"]
        lowerCaptures = parsedFileInput["lowerCaptures"]
        inputMoves = parsedFileInput["moves"]

        #Initialize all pieces on the board
        for item in listOfPieces:
            piece = item["piece"]
            piecePosition = item["position"]
            addPieceToBoard(piece, piecePosition, self.board)
        
        #Initialize the captures
        initCaptures(self, upperCaptures, 0)
        initCaptures(self, lowerCaptures, 1)

        #Iterate list for every move
        for command in inputMoves:
            #Before the turn happens, check if the player is in check
            if isInCheck(self.playerTurn, self.board):
                #Player is in check, get all possible moves to get out of check
                    listOfPossibleMoves = printIsInCheck(self)
                    #Error occurred
                    if listOfPossibleMoves == -1:
                        return
                    self.playerInCheck = True
            
            #Player is not in check, get space seperated list of the command
            commandList = getMoveCommand(command)
            #Update the prev command
            self.prevMove = command

            #Do the command (move or drop)
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
            #Error occurred
            if returnVal == -1:
                return

        #All the moves have been completed. check if the player that would have gone next is in check
        if isInCheck(self.playerTurn, self.board):
            #Get all possible way to get out of check
            listOfPossibleMoves = printIsInCheck(self)
            self.playerInCheck = True
        else:
            self.playerInCheck = False

        #Input file has given a partially complete game, print the beginning of the turn
        if self.endedGame == False:
            printBeginTurn(self, listOfPossibleMoves)
            print("")
            print(self.playerTurn + "> ")
        
        return
                

    def gameLoop(self):
        """
            Game loop for interactive mode
        """
        #Keep the game going until its over
        while 1:
            possibleMoves = []
            #Check detection at the beginning of every turn
            if isInCheck(self.playerTurn, self.board):
                self.playerInCheck = True
                possibleMoves = printIsInCheck(self)
                if possibleMoves == -1:
                    return
            else:
                #Otherwise not in check, continue on normally
                self.playerInCheck = False

            #Print the beginning of the turn
            printBeginTurn(self, possibleMoves)
            #Get the user input command
            commandList = self.getInput()
            #IF the player is in check and they do a move other than the moves given, then they lose (Illegal Move)
            if self.playerInCheck and " ".join(commandList) not in possibleMoves:
                self.returnMessage = " Illegal move."
                if self.playerTurn == "lower":
                    self.gameWinner = "UPPER"
                else:
                    self.gameWinner = "lower"
                    self.endGame()
                    return

            #Store the command to be printed later
            self.prevMove = " ".join(commandList)
            #Do the command (move, drop, etc.)
            returnVal = self.handleTurnCommand(commandList)
            #-1 means Illegal move was inputted
            if returnVal == -1:
                self.returnMessage = " Illegal move."
                self.endGame()
                return
            #Update whos turn it is before the next turn
            self.updateTurn()
        
        return

    def run(self):
        """
            run the game depending on game mode
            Entry point for starting a game
            (file, or interactive)
        """
        if self.file_mode == True:
            self.completeFromFile()
        elif self.interactive_mode == True:
            self.gameLoop()

        return
      

if __name__ == "__main__":
    pass
