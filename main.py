from src.game import Game

if __name__ == "__main__":
    help_descr = """
    Buttons:
     arrows move camera
     - or = changes zoom
     , or . changes simulation speed
     c centers camera
    """
    print(help_descr)

    game = Game()
    game.run()
