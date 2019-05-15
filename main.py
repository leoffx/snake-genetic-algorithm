import pygame as pg
import random
from nn import *
import matplotlib.pyplot as plt
import numpy as np
#from keras.models import load_model, save_model
pg.init()

res_x = 400
res_y = 400

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
            or cobra.head_y > res_y - 10
            or ([cobra.head_x, cobra.head_y] in cobra.body)):
        lose = True
    return lose


populationNum = 100
cobras = [snake() for _ in range(populationNum)]
#brain = [cobra.create_brain() for cobra in cobras]

food = create_food(res_x, res_y)

pop = True
run = True
lose = False
being_alive_score = .001
winner = 0

while run:
    pg.time.delay(50)  #game refresh
    win.fill((0, 0, 0))  #preenche display

    for event in pg.event.get():  #checa se clicou fechar
        if event.type == pg.QUIT:
            #winner.model.save_weights('winner.h5')
            run = False

    for cobra in cobras:
        cobra.score += being_alive_score
        if (food.x == cobra.head_x) and (
                food.y == cobra.head_y):  #acertou a cabeça na comida
            cobra.score += 2.
            print(cobra.score)
            food.x = (10 * np.random.randint(0, (res_x - 10) / 10))
            food.y = (10 * np.random.randint(0, (res_y - 10) / 10))
            while [food.x, food.y
                   ] in cobra.body:  #nao deixa a comida nascer dentro do corpo
                food.x = (10 * np.random.randint(0, (res_x - 10) / 10))
                food.y = (10 * np.random.randint(0, (res_y - 10) / 10))
            pop = False  #deixa crescer 1

        if pop:  #corta o rabo
            cobra.body.pop(0)
        pop = True

        pg.draw.rect(win, (255, 0, 0),
                     (food.x, food.y, food.heigth, food.width))  #draw food
        draw_snake(cobra)  #draw snake
        cobra.body.append([
            cobra.head_x, cobra.head_y
        ])  #em t+1 passa o ultimo pixel pro lugar da cabeça em t
        pg.display.update()
        keys = pg.key.get_pressed()

        #if keys.count(1) == 1:  #evitar andar pra trás
        cobra.mov_x, cobra.mov_y = cobra.movimento(keys, food)

        cobra.head_x += cobra.mov_x
        cobra.head_y += cobra.mov_y
        if check_lose(res_x, res_y, cobra):
            if cobra.score > 0:
                if not winner:
                    winner = cobra
                elif cobra.score >= winner.score:
                    print(cobra.score)
                    winner = cobra
            cobras.remove(cobra)

            if (cobras == []):
                #print(winner.model.get_weights())
                food = create_food(res_x, res_y)
                #weights = winner.model.get_weights()

                if (winner):
                    print('foi!')
                    weights = winner.params
                    for cobra in cobras:
                        cobra.mutate(weights)
                cobras = [snake() for _ in range(200)]
                #winner = 0
pg.quit()
