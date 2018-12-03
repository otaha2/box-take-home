def isSquareEmpty(position, board):
    posX = position[0]
    posY = position[1]

    if board[posX][posY] == 1:
        return True
    else:
        return False