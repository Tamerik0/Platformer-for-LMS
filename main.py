import sys

from Box2D import b2World, b2PolygonShape
import pygame
import engine

from engine import Vector2

pygame.init()
window_size = (width, height) = (501, 501)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('')
FPS = 60
clock = pygame.time.Clock()

PPM = 40.0

phys_world = b2World(gravity=(0, -10), doSleep=True)
ground_body = phys_world.CreateStaticBody(
    position=(0, 1),
    shapes=b2PolygonShape(box=(25, 2.5)),
)
dynamic_body = phys_world.CreateDynamicBody(position=(5, 7.5), angle=15)
box = dynamic_body.CreatePolygonFixture(box=(1, 0.5), density=1, friction=0.3)
box1 = dynamic_body.CreatePolygonFixture(box=(0.5, 1), density=1, friction=0.3)

event_system = engine.EventSystem()
render_system = engine.EventSystem()
engine.init_event_systems(event_system, render_system)
a = engine.Sprite(pygame.image.load('bebra.png'))
a.pos = Vector2(100, 100)
while True:
    deltatime = clock.tick(FPS)
    phys_world.Step(deltatime / 1000, 10, 10)
    for event in pygame.event.get():
        event_system.call_event(event)
        if event.type == pygame.QUIT:
            sys.exit(0)
    screen.fill(0xffffff)
    for body in phys_world.bodies:
        for fixture in body.fixtures:
            shape = fixture.shape
            vertices = [(body.transform * v) * PPM for v in shape.vertices]
            vertices = [(int(v[0]), int(501 - v[1])) for v in vertices]
            pygame.draw.polygon(screen, 0xfff000, vertices)
    render_system.call_event(engine.RenderEvent(screen, deltatime))
    pygame.display.flip()
