import pygame
from pygame.draw import *
from random import randint
from random import choice
pygame.init()

FPS = 70
dt = 1/FPS
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

#размеры экрана
WIDTH = 1200
HEIGHT = 900
SPACE = 0

G = 0 #гравитация
k = 1.01 #коэффициент трения
VYMIN2 = 50 #квадрат скорости, при которой происходит остановка

"""def new_ball():
    global x, y, r
    x = randint(100,700)
    y = randint(100,500)
    r = randint(30,50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)"""
class Ball:
    """класс вылетающих из пушки шариков"""
    def __init__(self, screen: pygame.Surface, x=40, y=450, r=10, vx=10, vy=10):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen #экран
        self.x = x #координаты
        self.y = y
        self.r = r #радиус
        self.vx = vx #скорости
        self.vy = vy
        self.color = choice(GAME_COLORS) #цвет
        self.live = 30 #
        self.time_live = 400 #время жизни


    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx*dt #новые координаты
        self.y -= self.vy*dt
        if self.time_live < 0: #удаление шара при его смерти
            balls.remove(self)
        self.vy -= G #изменение скорости по у в следствие гравитации
        if (self.x+self.r)>WIDTH: #столкновение с правой стеной
            self.x = WIDTH-self.r
            self.vx = - self.vx*k
        if (self.y+self.r)>(HEIGHT-SPACE): #столкновение с низом
            self.y = (HEIGHT-SPACE)-self.r
            if self.vy*self.vy < VYMIN2:
                self.vy = 0 #остановка, если скорость маленькая
            else:
                self.vy = - self.vy*k #иначе замедление по у
            self.vx = self.vx*k #замедление по х
        if (self.y-self.r)<0: #столкновение с верхом
            self.y = 0+self.r
            self.vy = - self.vy*k
        if (self.x-self.r)<0: #столкновение с левой стеной
            self.x = self.r
            self.vx = - self.vx*k

    def draw(self):
        """Отрисовать шарик

        Метод рисует шарик
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
            Удаляет шар при столкновении
        """
        if ((obj.x)-(self.x))**2 + ((obj.y)-(self.y))**2 <= (self.r + obj.r)**2:
            balls.remove(self)
            return True
        else:
            return False
    def refrash(self):
        """Обновляет координаты цели и прибавляет очко"""
        self.x = randint(600, 700)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        vx = randint(100, 500)
        vy = randint(100, 500)
        self.points += 1

def click(event):
    print(x, y, r)


pygame.display.update()
clock = pygame.time.Clock()
balls = [] # массив шаров
for i in range (5):
    r = randint(10, 100)
    x0 = randint(r, 600)
    y0 = randint(r, 400)
    vx = randint(100, 500)
    vy = randint(100, 500)
    b = Ball(screen, x0, y0, r, vx, vy)
    balls.append(b)
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
    for b in balls: # рисуем шары
        b.draw()
    for b in balls: # двигаем шары
        b.move()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
