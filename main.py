from src.renderers.void import VoidRenderer
from src.game import Game
from src.renderers.pygame import PyGameRenderer


if __name__ == "__main__":
    renderer = PyGameRenderer()
    # renderer = VoidRenderer()
    game = Game(renderer)
    game.main()
