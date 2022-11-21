import pygame # импорт библиотек
from pygame.draw import *
from random import randint
from random import choice
pygame.init()

FPS = 300 # кадры в секунду
dt = 1/FPS # промежуток времени
screen = pygame.display.set_mode((1200, 900)) # экран

#цвета
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

k = 1.01 #коэффициент увеличения скорости

class Ball:
    """класс шариков"""
    def __init__(self, screen: pygame.Surface, x=40, y=450, r=10, vx=10, vy=10):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        r - радиус
        vx и vy - скорости по горизонтали и вертикали
        """
        self.screen = screen #экран
        self.x = x #координаты
        self.y = y
        self.r = r #радиус
        self.vx = vx #скорости
        self.vy = vy
        self.color = choice(GAME_COLORS) #цвет

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx*dt #новые координаты
        self.y -= self.vy*dt
        if (self.x+self.r)>WIDTH: #столкновение с правой стеной
            self.x = WIDTH-self.r
            self.vx = - self.vx*k
        if (self.y+self.r)>(HEIGHT-SPACE): #столкновение с низом
            self.y = (HEIGHT-SPACE)-self.r
            self.vy = - self.vy*k #замедление по у
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

    def refrash(self):
        """Обновляет координаты шара и прибавляет Oчко"""
        self.r = randint(10, 100)
        self.x = randint(r, 600)
        self.y = randint(r, 400)
        self.vx = randint(100, 500)
        self.vy = randint(100, 500)
        self.color = choice(GAME_COLORS)

def pointing(points):
    """Вывести Очки на экран

        Метод выводит Очки на экран
        """
    font = pygame.font.Font(None, 50) # выводим очки на экран
    text = font.render("Очки:", True, YELLOW)
    text2 = font.render(str(points), True, YELLOW)
    screen.blit(text, [20,20])
    screen.blit(text2, [150,20])



pygame.display.update()
clock = pygame.time.Clock()
balls = [] # массив шаров
for i in range (5): # создание шаров
    r = randint(10, 100)
    x0 = randint(r, 600)
    y0 = randint(r, 400)
    vx = randint(100, 500)
    vy = randint(100, 500)
    b = Ball(screen, x0, y0, r, vx, vy)
    balls.append(b)
finished = False
points = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # завершение программы
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN: # нажатие мыши
            for b in balls:
                if (event.pos[0] - b.x)**2 + (event.pos[1] - b.y)**2 <= b.r**2: #проверка попадания клика на шарик
                    points += 1
                    b.refrash()
    for b in balls: # рисуем  и двигаем шары
        b.draw()
        b.move()
    pointing(points) # выводим очки
    pygame.display.update() # обновление экрана
    screen.fill(BLACK) # заполнение экрана чёрным цветом

pygame.quit()
