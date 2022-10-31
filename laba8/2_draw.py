import pygame
from pygame.draw import *

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))



circle(screen, (250, 200, 0), (200, 175), 150)
circle(screen, (0, 0, 0), (200, 175), 150, 2)
circle(screen, RED, (125, 150), 30)
circle(screen, BLACK, (125, 150), 30, 3)
circle(screen, RED, (200, 150), 30)
circle(screen, BLACK, (200, 150), 30, 3)

circle(screen, BLUE, (300, 100), 10)
circle(screen, BLUE, (300, 120), 10)
circle(screen, BLUE, (280, 100), 10)
circle(screen, BLUE, (280, 120), 10)
circle(screen, RED, (290, 110), 10)

rect(screen, BLACK, (150, 250, 80, 10))

polygon(screen, BLUE, [(100,50), (200,0),
                              (300,50), (100,50)])





pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()