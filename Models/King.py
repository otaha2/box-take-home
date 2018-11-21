from Models import Piece

class King(Piece.Piece):

    def __init__(self, player, posx, posy):
        super().__init__(player, posx, posy)
        if self.player == "UPPER":
            self.name = "K"
        else:
            self.name = "k"
    
    def availableMoves(self, posx, posy, board):
        print("King implemented")
    
    def doSomething(self):
        super().doSomething()
        print("Now King is doing something!")

if __name__ == "__main__":
    newKing = King("lower", 1, 1)
    # newKing.doSomething()
    print("Printing King: ")
    print(newKing)
    newKing.promote()
    print(newKing)