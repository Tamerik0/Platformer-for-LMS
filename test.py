import inspect
import math

import pygame
from pygame.time import Clock

import GameObjects
import sys

from Box2D.examples.framework import Framework
from Box2D import *
import Box2D
from pygame import Vector2

from engine import Camera, Scene, Transform


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
s = Framework()
world = b2World(gravity=(0, -10), doSleep=True)
# s.world = world
s.scene = Scene.load('construct/Layouts/Layout 1.xml', 'construct/New project.caproj', classes, s.world)
s.scene.main_camera = Camera(s.scene, Vector2(0.5, 0.5), 25.1, 25.1)
clock = Clock()
if __name__ == "__main__":
    # Simulation().run()
    while True:
        deltatime = clock.tick(60) / 1000
        # scene.update(deltatime)
        # running = s.checkEvents()
        s.screen.fill((0, 0, 0))

        # Check keys that should be checked every loop (not only on initial
        # keydown)
        # s.CheckKeys()
        screen.fill(0xff00)
        # scene.render(screen, None, deltatime=deltatime)
        for body in s.scene.world.bodies:
            for fixture in body.fixtures:
                vertices = [((i[0] + body.transform.position.x) * Transform.PPM / 2 + 7,
                             height - (i[1] + body.transform.position.y) * Transform.PPM / 2 - 4) for i in [Vector2(j[0],j[1]).rotate(body.angle/math.pi*180) for j in fixture.shape.vertices]]
                pygame.draw.polygon(screen, 0xff0000, vertices, 1)
        pygame.display.flip()
        # Run the simulation loop
        s.Step(s.settings)
        deltatime = clock.tick(60) / 1000
        s.scene.update(deltatime)

        for event in pygame.event.get():
            s.scene.listen_event(event)
            if event.type == pygame.QUIT:
                sys.exit(0)

        # if s.settings.drawMenu:
        #     s.gui_app.paint(s.screen)

        pygame.display.flip()
        # clock.tick(s.settings.hz)
        # s.fps = clock.get_fps()
        # s.SimulationLoop()
        # for i in s.scene.objects:
        #     if isinstance(i, GameObjects.Player):
        #         i.update(deltatime)
        # for event in pygame.event.get():
        #     s.scene.listen_event(event)
        #     if event.type == pygame.QUIT:
        #         sys.exit(0)

        # s.screen.fill(0xff00)
        # s.scene.render(s.screen, None, deltatime=deltatime)
        # for body in s.scene.world.bodies:
        #     for fixture in body.fixtures:
        #         vertices = [((i[0] + body.position.x) * Transform.PPM / 2 + 7,
        #                      s.screen.get_height() - (i[1] + body.position.y) * Transform.PPM / 2 - 4) for i in fixture.shape.vertices]
        #         pygame.draw.polygon(s.screen, 0xff0000, vertices, 1)
        # pygame.display.flip()


