import pygame as pg
import numpy as np


class snake():
    def __init__(self, size=3):
        self.heigth = 10
        self.width = 10
        self.vel = 10
        self.head_x = 300
        self.head_y = 300
        self.score = 0
        self.initial_size = size
        self.body = []
        self.mov_x = self.vel
        self.mov_y = 0
        for _ in range(self.initial_size):
            self.body.append([self.head_x - 10, self.head_y])
        self.params = self.init_params()

    def init_params(self):
        #initialization
        W1 = np.random.uniform(low=-1, high=1, size=(16, 6))
        b1 = np.random.uniform(low=-1, high=1, size=(16, 1))

        W2 = np.random.uniform(low=-1, high=1, size=(4, 16))
        b2 = np.random.uniform(low=-1, high=1, size=(4, 1))

        params = {
            "W1": W1,
            "b1": b1,
            "W2": W2,
            "b2": b2,
        }

        return params

    def model_predict(self, X0):
        #first layer
        X = np.dot(self.params["W1"], X0)
        X = np.add(X, self.params["b1"])
        X = np.tanh(X)  #activation

        #final layer
        X = np.dot(self.params["W2"], X)
        X = np.add(X, self.params["b2"])
        X = np.exp(10 * X) / np.sum(np.exp(10 * X))  #softmax

        return X

    """def get_screen(self): #para fazer a versão com imagem
        gameState = pg.display.get_surface()
        imageArray = pg.surfarray.array2d(gameState)
        return imageArray"""

    def movimento(self, food):
        X0 = np.reshape([[self.head_x], [food.x], [self.head_y], [food.y],
                         [self.head_x - food.x], [self.head_y - food.y]],
                        (6, 1)) / 600  #, [food.x], [food.y]],(4, 1)) / 400

        move = self.model_predict(X0)
        move = np.random.choice(4, 1, p=move[:, 0])

        if move == 0:
            if self.mov_x == 0:
                self.mov_x = -self.vel
                self.mov_y = 0
        elif move == 1:
            if self.mov_x == 0:
                self.mov_x = self.vel
                self.mov_y = 0
        elif move == 2:
            if self.mov_y == 0:
                self.mov_x = 0
                self.mov_y = -self.vel
        elif move == 3:
            if self.mov_y == 0:
                self.mov_x = 0
                self.mov_y = self.vel

        return self.mov_x, self.mov_y

    def mutate(self, weights):
        for weight in weights:
            self.params[weight] = weights[weight] + np.random.normal(
                scale=.1, size=self.params[weight].shape)


class create_food():
    def __init__(self, res_x, res_y):
        self.heigth = 10
        self.width = 10
        self.x = (10 * np.random.randint(0, (res_x - 10) / 10))
        self.y = (10 * np.random.randint(0, (res_y - 10) / 10))
        self.lifespan = 0
