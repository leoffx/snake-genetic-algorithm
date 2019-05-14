import keras as K
from keras.layers import Dense, Input, Flatten
from keras.models import Model
import pygame as pg
import numpy as np


class snake():
    def __init__(self, size=3):
        self.heigth = 10
        self.width = 10
        self.vel = 10
        self.head_x = 40
        self.head_y = 150
        self.score = 0
        self.initial_size = size
        self.body = []
        self.mov_x = self.vel
        self.mov_y = 0
        for _ in range(self.initial_size):
            self.body.append([self.head_x - 10, self.head_y])
        self.model = self.create_model()

    def create_model(self):
        X_input = Input(shape=(4, ))

        X = Dense(4, activation='relu')(X_input)

        X = Dense(4, activation='softmax')(X_input)

        model = Model(inputs=X_input, outputs=X)

        return model

    """def get_screen(self): #para fazer a versão com imagem
        gameState = pg.display.get_surface()
        imageArray = pg.surfarray.array2d(gameState)
        return imageArray"""

    def movimento(self, keys, food):
        move = self.model.predict(
            np.reshape([[self.head_x], [self.head_y], [food.x], [food.y]], (1,4,))) 

        if keys[pg.K_p]:
            self.mov_x = 0
            self.mov_y = 0
        elif move[0,0] > .8:
            if self.mov_x == 0:
                self.mov_x = -self.vel
                self.mov_y = 0
        elif move[0,1] > .8:
            if self.mov_x == 0:
                self.mov_x = self.vel
                self.mov_y = 0
        elif move[0,2] > .8:
            if self.mov_y == 0:
                self.mov_x = 0
                self.mov_y = -self.vel
        elif move[0,3] > .8:
            if self.mov_y == 0:
                self.mov_x = 0
                self.mov_y = self.vel

        return self.mov_x, self.mov_y

    def mutate(self, weights):
        weights = [((weight * (1 + .05 * np.random.uniform(low=-1.,high=1., size=weight.shape)))) for weight in weights]
        self.model.set_weights(weights)



class create_food():
    def __init__(self, res_x, res_y):
        self.heigth = 10
        self.width = 10
        self.x = (10 * np.random.randint(0, (res_x - 10) / 10))
        self.y = (10 * np.random.randint(0, (res_y - 10) / 10))
