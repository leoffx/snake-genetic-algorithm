from nn import Snake, Food
import pygame as pg
import numpy as np


RES_X = 600
RES_Y = 600
POPULATION = 40


class Game:
    snakes: list[Snake]
    foods: Food

    best_score = 1
    winners: list[Snake] = []

    def __init__(self):
        pg.init()
        pg.display.set_caption("Snake")
        self.window = pg.display.set_mode([RES_X, RES_Y])
        self.snakes = [Snake() for _ in range(POPULATION)]
        self.food = Food(RES_X, RES_Y)

    def draw_snake(self, snake):
        pg.draw.rect(
            self.window,
            (255, 0, 255),
            (snake.head_x, snake.head_y, snake.heigth, snake.width),
        )
        for x in range(len(snake.body)):
            pg.draw.rect(
                self.window,
                (255, 255, 255),
                (snake.body[x][0], snake.body[x][1], snake.heigth, snake.width),
            )

    def main(self):
        self.load_winners()
        while True:
            try:
                self.game_loop()
            except StopIteration:
                break
        pg.quit()

    def check_lose(self, snake: Snake):
        return (
            0 > snake.head_x
            or snake.head_x > (RES_X - 10)
            or 0 > snake.head_y
            or snake.head_y > (RES_Y - 10)
        )

    def reset_game(self):
        self.snakes = [Snake() for _ in range(POPULATION)]
        self.food = Food(RES_X, RES_Y)

        if not self.winners:
            return
        for winner in self.winners:
            self.snakes.extend(winner.create_children(10))
        self.winners = []

    def handle_frame(self, snake: Snake):
        snake.score += 1
        if (self.food.x == snake.head_x) and (self.food.y == snake.head_y):
            snake.score += 1
            self.food = Food(RES_X, RES_Y)
        else:
            snake.body.pop(0)

        self.draw_snake(snake)
        snake.body.append([snake.head_x, snake.head_y])

        snake.mov_x, snake.mov_y = snake.choose_move(self.food)
        snake.head_x += snake.mov_x
        snake.head_y += snake.mov_y

        if self.food.lifespan >= 400 or self.check_lose(snake):
            if snake.score > self.best_score:
                self.winners.append(snake)
                self.best_score = snake.score
            self.snakes.remove(snake)

    def draw_food(self):
        pg.draw.rect(
            self.window,
            (255, 0, 0),
            (self.food.x, self.food.y, self.food.heigth, self.food.width),
        )

    def game_loop(self):
        pg.time.delay(10)
        self.window.fill((0, 0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.store_winners()
                raise StopIteration()

        self.draw_food()
        for snake in self.snakes:
            self.handle_frame(snake)
        self.food.lifespan += 1
        pg.display.update()

        if self.snakes == []:
            self.reset_game()

    def store_winners(self):
        np.save("winners.npy", self.winners)

    def load_winners(self):
        try:
            self.winners = np.load("winners.npy").tolist()
        except FileNotFoundError:
            self.winners = []
