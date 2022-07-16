from src.game import Game


def main():
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


if __name__ == "__main__":
    main()
