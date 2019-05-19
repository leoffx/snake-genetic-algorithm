import pygame as pg
import random
from nn import *
import matplotlib.pyplot as plt
import numpy as np
pg.init()

res_x = 600
res_y = 600

win = pg.display.set_mode([res_x, res_y])

pg.display.set_caption("Snake")


def draw_snake(cobra):
    pg.draw.rect(win, (255, 0, 255), (cobra.head_x, cobra.head_y, cobra.heigth,
                                      cobra.width))  #constroi a cabeça
    for x in range(len(cobra.body)):
        pg.draw.rect(win, (255, 255, 255),
                     (cobra.body[x][0], cobra.body[x][1], cobra.heigth,
                      cobra.width))  #constroi o corpo


def check_lose(res_x, res_y, cobra):
    lose = False
    if (cobra.head_x < 0 or cobra.head_y < 0 or cobra.head_x > res_x - 10
            or cobra.head_y >
            res_y - 10):  #or ([cobra.head_x, cobra.head_y] in cobra.body)):
        lose = True
    return lose


populationNum = 500
cobras = [snake() for _ in range(populationNum)]

food = create_food(res_x, res_y)

pop = True
run = True
lose = False
being_alive_score = 0
best_score = 1
best_winners = []

try:
    winners = np.load('winners.npy').tolist()
except FileNotFoundError:
    winners = []

while run:
    #pg.time.delay(10)  #game refresh
    win.fill((0, 0, 0))  #preenche display

    for event in pg.event.get():  #checa se clicou fechar
        if event.type == pg.QUIT:
            np.save('winners.npy', winners)
            run = False

    pg.draw.rect(win, (255, 0, 0),
                 (food.x, food.y, food.heigth, food.width))  #draw food
    for cobra in cobras:
        cobra.score += being_alive_score
        if (food.x == cobra.head_x) and (
                food.y == cobra.head_y):  #acertou a cabeça na comida
            cobra.score += 1.
            food = create_food(res_x, res_y)
            """food.x = (10 * np.random.randint(0, (res_x - 10) / 10))
            food.y = (10 * np.random.randint(0, (res_y - 10) / 10))"""
            """while [food.x, food.y
                   ] in cobra.body:  #nao deixa a comida nascer dentro do corpo
                food.x = (10 * np.random.randint(0, (res_x - 10) / 10))
                food.y = (10 * np.random.randint(0, (res_y - 10) / 10))"""
            pop = False  #deixa crescer 1

        if pop:  #corta o rabo
            cobra.body.pop(0)
        pop = True

        draw_snake(cobra)  #draw snake
        cobra.body.append([
            cobra.head_x, cobra.head_y
        ])  #em t+1 passa o ultimo pixel pro lugar da cabeça em t

        cobra.mov_x, cobra.mov_y = cobra.movimento(food)
        cobra.head_x += cobra.mov_x
        cobra.head_y += cobra.mov_y

        if (food.lifespan >= 400) or check_lose(res_x, res_y, cobra):
            if cobra.score > best_score:  #check if snake is better than others
                winners.append(cobra)
                best_winners.append(
                    cobra
                )  #reserve snake for a new population when it reaches a threshold
                print(len(best_winners))
                if len(best_winners) >= 3:  #arbitrary number
                    winners = best_winners
                    best_score = cobra.score
                    best_winners = []
            elif cobra.score == best_score:  #check if snake reaches current score threshold
                for winner in winners:
                    if (np.array_equal(cobra.params['W1'], winner.params['W1'])
                        ):  #check if this snake is already in the winner list
                        break
                else:
                    winners.append(cobra)
            cobras.remove(cobra)

    food.lifespan += 1  #increases current acceptable idle time for snakes
    pg.display.update()
    if (cobras == []):
        food.lifespan = 0
        cobras = [snake() for _ in range(populationNum + len(winners))
                  ]  #create new population with slots for the winners
        print(len(cobras))
        if (winners):  #breeding
            for i in range(len(winners)):
                child_num = int(populationNum / len(winners))
                weights = winners[i].params
                for cobra in cobras[i * child_num:(
                        i + 1) * child_num]:  #mutate the children of winners
                    cobra.mutate(weights)
                cobras[populationNum +
                       i].params = weights  #add winners to the new population

pg.quit()
