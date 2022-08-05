from src.game import Game


def main():
    help_descr = """
    Buttons:
     arrows move camera
     - or =     -> changes zoom
     , or .     -> changes simulation speed
     c          -> centers camera
     j          -> skip 10 cycles
     e          -> exit
     leftclick  -> adding fish (demo)
     q          -> change fish
    """
    print(help_descr)

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
