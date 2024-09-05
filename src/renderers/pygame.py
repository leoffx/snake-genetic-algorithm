import pygame as pg

from src.configs import (
    FOOD_COLOR,
    FOOD_SIZE,
    GAME_BACKGROUND_COLOR,
    SCREEN_SIZE,
    SNAKE_BODY_COLOR,
    SNAKE_HEAD_COLOR,
    SNAKE_SIZE,
)
from src.objects import Food, Snake


class PyGameRenderer:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Snake")
        self.window = pg.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    def draw_snake(self, snake: Snake):
        pg.draw.rect(
            self.window,
            SNAKE_HEAD_COLOR,
            (snake.head_x, snake.head_y, SNAKE_SIZE, SNAKE_SIZE),
        )
        for x in range(len(snake.body)):
            pg.draw.rect(
                self.window,
                SNAKE_BODY_COLOR,
                (snake.body[x][0], snake.body[x][1], SNAKE_SIZE, SNAKE_SIZE),
            )

    def draw_food(self, food: Food):
        pg.draw.rect(
            self.window,
            FOOD_COLOR,
            (food.x, food.y, FOOD_SIZE, FOOD_SIZE),
        )

    def draw_scene(self, snakes: list[Snake], food: Food):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise StopIteration

        pg.time.delay(10)
        self.window.fill(GAME_BACKGROUND_COLOR)
        self.draw_food(food)
        for snake in snakes:
            self.draw_snake(snake)
        pg.display.update()

    def quit(self):
        pg.quit()
