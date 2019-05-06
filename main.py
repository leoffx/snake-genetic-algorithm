import pygame as pg
import random
pg.init()

res_x = 400
res_y = 400

win = pg.display.set_mode([res_x, res_y])

pg.display.set_caption("Snake")

class snake():
    def __init__(self, size = 3):
        self.heigth = 10
        self.width = 10
        self.vel = 10
        self.head_x = 40
        self.head_y = 150
        self.score = 0
        self.initial_size = size
        self.body = []
        for k in range(self.initial_size):
            self.body.append([self.head_x-10, self.head_y])

class food():
    def __init__(self):
        self.heigth = 10
        self.width = 10
        self.x = (10 * random.randint(0, (res_x-10)/10))
        self.y = (10 * random.randint(0, (res_y-10)/10))
    
def movimento(keys, mov_x , mov_y):
    if keys[pg.K_p]:
        mov_x = 0
        mov_y = 0
    if keys[pg.K_LEFT]:
        if mov_x == 0:
            mov_x = -cobra.vel
            mov_y = 0
    if keys[pg.K_RIGHT]:
        if mov_x == 0:
            mov_x = cobra.vel
            mov_y = 0
    if keys[pg.K_UP]:
        if mov_y == 0:
            mov_x = 0
            mov_y = -cobra.vel
    if keys[pg.K_DOWN]:
        if mov_y == 0:
            mov_x = 0
            mov_y = cobra.vel
    return mov_x , mov_y



    
def draw_snake(cobra):
    pg.draw.rect(win,(255,0,255), (cobra.head_x, cobra.head_y, cobra.heigth, cobra.width)) #constroi a cabeça
    for x in range(len(cobra.body)):
        pg.draw.rect(win,(255,255,255), (cobra.body[x][0], cobra.body[x][1], cobra.heigth, cobra.width)) #constroi o corpo




        
def check_lose(res_x, res_y, cobra):
    lose = False
    if (cobra.head_x < 0 or cobra.head_y < 0 or cobra.head_x > res_x-10 or cobra.head_y > res_y-10 or ([cobra.head_x, cobra.head_y] in cobra.body)):
        lose = True
    return lose



cobra = snake()
food = food()


mov_x = cobra.vel
mov_y = 0
pop = True
run = True
lose = False


while run:
    pg.time.delay(50) #game refresh
    win.fill((0,0,0)) #preenche display
    
    for event in pg.event.get(): #checa se clicou fechar
        if event.type==pg.QUIT:
            run = False
            
    if food.x == cobra.head_x and food.y == cobra.head_y: #acertou a cabeça na comida
        cobra.score+=1
        print(cobra.score)
        food.x = (10 * random.randint(0, (res_x-10)/10))
        food.y = (10 * random.randint(0, (res_y-10)/10))
        while [food.x, food.y] in cobra.body: #nao deixa a comida nascer dentro do corpo
            food.x = (10 * random.randint(0, (res_x-10)/10))
            food.y = (10 * random.randint(0, (res_y-10)/10))
        pop = False #deixa crescer 1
    
    
    if pop: #corta o rabo
        cobra.body.pop(0)
    pop = True
    

    pg.draw.rect(win,(255,0,0), (food.x, food.y, food.heigth, food.width)) #draw food
    draw_snake(cobra) #draw snake
    cobra.body.append([cobra.head_x, cobra.head_y]) #em t+1 passa o ultimo pixel pro lugar da cabeça em t
    pg.display.update()
    keys = pg.key.get_pressed()
    
    if keys.count(1)==1: #evitar andar pra trás
        mov_x, mov_y = movimento(keys, mov_x, mov_y)

    cobra.head_x += mov_x
    cobra.head_y += mov_y
    if check_lose(res_x, res_y, cobra):
        print("LOSER", cobra.head_x, cobra.head_y)
        cobra = []
        cobra = snake()
        mov_x = cobra.vel
        mov_y = 0

pg.quit()
