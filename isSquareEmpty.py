#This function is on its own due to import troubles, this was the quickest way to solve that

def isSquareEmpty(position, board):
    """
        Checks if specified square is empty
    """
    posX = position[0]
    posY = position[1]

    #Emoty square is represented by 1
    if board[posX][posY] == 1:
        return True
    else:
        return False