import pickle
from src.configs import POPULATION, SCREEN_SIZE, SNAKE_MAX_HUNGER_TICKS, SNAKE_SIZE
from src.objects import Snake, Food
from src.renderer import PyGameRenderer, Renderer, VoidRenderer


class Game:
    snakes: list[Snake]
    foods: Food
    renderer: Renderer

    best_score = 1
    winners: list[Snake] = []

    def __init__(self):
        self.snakes = [Snake() for _ in range(POPULATION)]
        self.food = Food(SCREEN_SIZE, SCREEN_SIZE)
        self.renderer = PyGameRenderer()

    def main(self):
        self.load_winners()
        while True:
            try:
                self.game_loop()
            except StopIteration:
                break
        self.store_winners()
        self.renderer.quit()

    def check_lose(self, snake: Snake):
        return (
            0 > snake.head_x
            or snake.head_x > (SCREEN_SIZE - SNAKE_SIZE)
            or 0 > snake.head_y
            or snake.head_y > (SCREEN_SIZE - SNAKE_SIZE)
        )

    def reset_game(self):
        self.snakes = [Snake() for _ in range(POPULATION)]
        self.food = Food(SCREEN_SIZE, SCREEN_SIZE)

        if not self.winners:
            return
        for winner in self.winners:
            self.snakes.extend(winner.create_children(10))

    def update_snake(self, snake: Snake):
        snake.score += 1
        if (self.food.x == snake.head_x) and (self.food.y == snake.head_y):
            snake.score += 1
            self.food = Food(SCREEN_SIZE, SCREEN_SIZE)
        else:
            snake.body.pop(0)

        snake.body.append([snake.head_x, snake.head_y])

        snake.mov_x, snake.mov_y = snake.choose_move(self.food)
        snake.head_x += snake.mov_x
        snake.head_y += snake.mov_y

        if self.food.lifespan >= SNAKE_MAX_HUNGER_TICKS or self.check_lose(snake):
            if snake.score > self.best_score:
                self.winners = [snake]
                self.best_score = snake.score
            self.snakes.remove(snake)

    def game_loop(self):
        for snake in self.snakes:
            self.update_snake(snake)
        self.renderer.draw_scene(snakes=self.snakes, food=self.food)
        self.food.lifespan += 1

        if self.snakes == []:
            self.reset_game()

    def store_winners(self):
        with open("winners.pkl", "w+b") as f:
            pickle.dump(self.winners, f)

    def load_winners(self):
        try:
            with open("winners.pkl", "rb") as f:
                self.winners = pickle.load(f)
        except Exception:
            self.winners = []