
class Game():

    chess_map_from_alpha_to_index = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4}
    chess_map_from_index_to_alpha = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}


    def __init__(self):
        self.playerTurn = "lower"
        self.initBoard()

    def initBoard(self):
        #Board is stored in Row-Column Order
        self.board = [[1] * 5 for i in range(5)]
        self.board[1][0] = "p"
        self.board[3][4] = "P"
        pieceOnBoard = ["k", "g", "s", "b", "r"]
        for i in range(5):
            self.board[0][i] = pieceOnBoard[i]
            self.board[4][4-i] = pieceOnBoard[i].upper()
        

    def printBoard(self):
        for row in self.board:
            print(row)

if __name__ == "__main__":
    newGame = Game()
    newGame.printBoard()