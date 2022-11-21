import math #импорт библиотек
from random import choice
from random import randint
import numpy as np
import pygame

FPS = 50 #кадры в секунду
#цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (144, 238, 144)
MAGENTA = (255, 0, 255 )
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

#размеры экрана
WIDTH = 800
HEIGHT = 600
SPACE = 50

G = 1 #гравитация
k = 0.7 #коэффициент трения
VYMIN2 = 50 #квадрат скорости, при которой происходит остановка
class Ball:
    """класс вылетающих из пушки шариков"""
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen #экран
        self.x = x #координаты
        self.y = y
        self.r = 10 #радиус
        self.vx = 0 #скорости
        self.vy = 0
        self.color = choice(GAME_COLORS) #цвет
        self.live = 30 #
        self.time_live = 400 #время жизни


    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx #новые координаты
        self.y -= self.vy
        self.time_live -= 1 #уменьшение времени жизни
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


class Gun:
    """класс Пушка"""
    def __init__(self, screen):
        """ Конструктор класса gun

        Args:
        screen - экран
        """
        self.screen = screen #экран
        self.f2_power = 10 #начальная мощность
        self.f2_on = 0 #наводят ли пушку
        self.an = 1 #угол пушки
        self.color = GREY #цвет пушки
        self.y = 450 #координаты
        self.x = 20
        self.leng = 20+self.f2_power//1.25 #длина пушки

    def fire2_start(self, event):
        """Функция начинает наведение пушки

        Args:
            obj: Событие (нажатие мышки)
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls #массив с шариками
        new_ball = Ball(self.screen) #новый мяч
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x)) #вычисление угла
        new_ball.vx = self.f2_power * math.cos(self.an) #вычисление скоростей
        new_ball.vy = - self.f2_power * math.sin(self.an)
        new_ball.x = self.x
        new_ball.y = self.y
        balls.append(new_ball) #добавление мяча в массив
        self.f2_on = 0 #пушка больше не наводится
        self.f2_power = 10 #обычная мощность

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x)) #угол
        if self.f2_on: #цвет в зависимости от включенности
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисует пушку"""
        rectangle_surface = pygame.Surface((WIDTH, HEIGHT))
        rectangle_surface.fill((255, 255, 255))
        old_center = rectangle_surface.get_rect().center
        pygame.draw.circle(rectangle_surface, BLUE, old_center, 10)
        pygame.draw.rect(rectangle_surface, self.color, pygame.Rect(WIDTH//2, HEIGHT//2, self.leng+self.f2_power/2, 10))
        rectangle_surface = pygame.transform.rotate(rectangle_surface, -self.an * 180 / math.pi)
        rect = rectangle_surface.get_rect()
        rect.center = (old_center[0] + self.x - WIDTH//2, old_center[1] + self.y - HEIGHT//2)
        self.screen.blit(rectangle_surface, rect)


    def power_up(self):
        """Увеличивает мощность при нажатии"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move_of_gun (self):
        if flag == 1:
            self.x += 3
        if flag == -1:
            self.x -= 3


class Target:
    """Класс цели"""
    def __init__(self, screen: pygame.Surface, x=700, y=500, r=50):
        """ Конструктор класса Target

        Args:
        screen - экран
        x, y - координаты
        r - радиус
        """
        self.screen = screen # экран
        self.x = x # координаты и радиус
        self.y = y
        self.r = r
        self.color = RED # цвет
        self.live = 1 # живая ли мишень
        self.points = 0 # количество очков

    def draw(self):
        """Рисует цель"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
    def refrash(self):
        """Обновляет координаты цели и прибавляет очко"""
        self.x = randint(600, 700)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        self.points += 1


pygame.init() # начало работы с pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # экран
balls = [] # массив шаров

clock = pygame.time.Clock() # часы
gun = Gun(screen) # пушка
target = Target(screen) # цель
flag = 0
finished = False # программа не закончена

while not finished:
    screen.fill(WHITE)
    gun.draw() # рисуем пушку и цель
    target.draw()
    for b in balls: # рисуем шары
        b.draw()
    for b in balls: # двигаем шары
        b.move()
    for b in balls: # проверяем шары на момент столкновения с мишенью
        if b.hittest(target):
            target.refrash()
    font = pygame.font.Font(None, 20) # выводим очки на экран
    text = font.render("Очки: ", True, BLUE)
    text2 = font.render(str(target.points), True, BLUE)
    screen.blit(text, [20,20])
    screen.blit(text2, [70,20])
    clock.tick(FPS)
    for event in pygame.event.get(): # считываем события
        if event.type == pygame.QUIT: # завершение программы
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN: # начало прицеливания
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP: # выстрел
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION: # поворот пушки
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                flag = -1
            if event.key == pygame.K_RIGHT:
                flag = 1
        elif event.type == pygame.KEYUP:
            flag = 0
    gun.move_of_gun()
    gun.power_up() # увеличивает мощность пушки
    pygame.display.update() # обновление экрана
pygame.quit()
