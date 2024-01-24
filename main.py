import inspect
import math

import pygame

import GameObjects
import sys

from Box2D.examples.framework import Framework
from Box2D import *
import Box2D
from pygame import Vector2

from engine import Camera, Scene, Transform

pygame.init()
window_size = (width, height) = (600, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('')
FPS = 60
clock = pygame.time.Clock()
classes = []
for _, i in inspect.getmembers(sys.modules['GameObjects']):
    if inspect.isclass(i):
        classes.append(i)
def load_level():
    global scene
    Transform.PPM = 40
    scene = Scene.load('construct/Layouts/Layout 1.xml', 'construct/New project.caproj', classes)
    scene.main_camera = Camera(scene, Vector2(0.5, 0.5), 25.1, 25.1)
load_level()
GameObjects.restart = load_level
while True:
    deltatime = clock.tick(FPS) / 1000
    # print(deltatime)
    scene.update(deltatime)
    for i in scene.objects:
        if isinstance(i, GameObjects.Player):
            i.update(deltatime)
    for event in pygame.event.get():
        scene.listen_event(event)
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(0xff00)
    scene.render(screen, None, deltatime=deltatime)
    # scene.objects[3].sprite.render(screen, scene.main_camera, 0)
    # for body in scene.world.bodies:
    #     pygame.draw.circle(screen, 0xff00,(body.position.x*Transform.PPM/2+7,height-body.position.y*Transform.PPM/2-4),3)
    #     for fixture in body.fixtures:
    #         vertices = [((i[0]+body.position.x)*Transform.PPM/2+7, height-(i[1]+body.position.y)*Transform.PPM/2-4) for i in [Vector2(j[0],j[1]).rotate(body.angle/math.pi*180) for j in fixture.shape.vertices]]
    #         pygame.draw.polygon(screen,0xff0000,vertices, 1)
    pygame.display.flip()
