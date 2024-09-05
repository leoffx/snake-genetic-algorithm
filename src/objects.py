import numpy as np

from src.configs import SCREEN_SIZE, SNAKE_INITIAL_SIZE


class Snake:
    vel: int
    head_x: int
    head_y: int
    score: int
    initial_size: int
    body: list
    mov_x: int
    mov_y: int

    def __init__(self):
        self.vel = 10
        self.head_x = 300
        self.head_y = 300
        self.score = 0
        self.body = []
        self.mov_x = self.vel
        self.mov_y = 0
        for _ in range(SNAKE_INITIAL_SIZE):
            self.body.append([self.head_x - 10, self.head_y])
        self.init_params()

    def init_params(self):
        W1 = np.random.normal(size=(16, 6)) / np.sqrt(16)
        b1 = np.zeros((16, 1))

        W2 = np.random.normal(size=(4, 16)) / np.sqrt(4)
        b2 = np.zeros((4, 1))

        self.params = {
            "W1": W1,
            "b1": b1,
            "W2": W2,
            "b2": b2,
        }

    def model_predict(self, X0):
        X = np.dot(self.params["W1"], X0)
        X = np.add(X, self.params["b1"])
        X = np.tanh(X)

        X = np.dot(self.params["W2"], X)
        X = np.add(X, self.params["b2"])
        X = np.exp(10 * X) / np.sum(np.exp(10 * X))

        return X

    def choose_move(self, food):
        X0 = (
            np.reshape(
                [
                    [self.head_x],
                    [food.x],
                    [self.head_y],
                    [food.y],
                    [self.head_x - food.x],
                    [self.head_y - food.y],
                ],
                (6, 1),
            )
            / SCREEN_SIZE
        )

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
                scale=0.1, size=self.params[weight].shape
            )

    def create_children(self, child_num) -> list["Snake"]:
        w = self.params
        children = []
        for i in range(child_num):
            child = Snake()
            child.mutate(w)
            children.append(child)
        return children


class Food:
    def __init__(self, res_x, res_y):
        self.x = 10 * np.random.randint(0, (res_x - 10) / 10)
        self.y = 10 * np.random.randint(0, (res_y - 10) / 10)
        self.lifespan = 0
