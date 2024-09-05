import matplotlib.pyplot as plt

from src.objects import Food, Snake


class GraphRenderer:
    highest_scores = [-1]
    current_round = 0

    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        plt.show()

    def draw_snake(self, snake: Snake) -> None:
        if snake.score > self.highest_scores[self.current_round]:
            self.highest_scores[self.current_round] = snake.score
            self.ax.plot(self.highest_scores)

    def draw_scene(self, snakes: list[Snake], food: Food) -> None: ...
    def draw_food(self, food: Food) -> None: ...
    def quit(self) -> None: ...
