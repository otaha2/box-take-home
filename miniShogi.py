import Game

if __name__ == "__main__":
    #Start a new game, define Command Line Option selected, and run it
    newGame = Game.Game()
    newGame.defineCLIOptions()
    newGame.run()