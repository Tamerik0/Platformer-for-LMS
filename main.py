import inspect
import math
import sys
import time

from Box2D import *
import pygame
from engine import *

from engine import Vector2
from GameObjects import *
pygame.init()
window_size = (width, height) = (501, 501)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('')
FPS = 60
clock = pygame.time.Clock()
classes = []
for _, i in inspect.getmembers(sys.modules['GameObjects']):
    if inspect.isclass(i):
        classes.append(i)
scene = Scene.load('construct/Layouts/Layout 1.xml', 'construct/New project.caproj', classes)
scene.main_camera = Camera(scene, Vector2(0.5, 0.5), 25.1, 25.1)
while True:
    deltatime = clock.tick(FPS) / 1000
    scene.update(deltatime)

    for event in pygame.event.get():
        scene.listen_event(event)
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(0xff00)
    scene.render(screen, None, deltatime=deltatime)
    for body in scene.world.bodies:
        for fixture in body.fixtures:
            vertices = [((i[0]+body.position.x)*Transform.PPM/2+7, height-(i[1]+body.position.y)*Transform.PPM/2-4) for i in fixture.shape.vertices]
            pygame.draw.polygon(screen,0xff0000,vertices, 1)
    pygame.display.flip()
