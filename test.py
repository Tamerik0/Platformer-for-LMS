from Box2D.examples.framework import Framework
from Box2D import *
import Box2D

class Simulation(Framework):
    def __init__(self):
        super(Simulation, self).__init__()
        # Ground body
        self.world.CreateBody(shapes=b2LoopShape(vertices=[(20, 0), (20, 40), (-20, 40), (-20, 0)]))
        # Dynamic body
        circle = b2FixtureDef(shape=b2CircleShape(radius=2), density=1, friction=0, restitution=1)
        self.world.CreateBody(type=b2_dynamicBody, position=b2Vec2(0,30), fixtures=circle, linearVelocity=(50, 0))
        self.world.CreateBody(type=b2_dynamicBody, position=b2Vec2(10,30), fixtures=circle, linearVelocity=(-5, 0))
        self.world.CreateBody(type=b2_dynamicBody, position=b2Vec2(-10,30), fixtures=circle, linearVelocity=(0, 0))
        box = b2FixtureDef(shape=b2PolygonShape(box=(1, 4)))

        self.world.CreateDynamicBody(fixtures=[circle,box], position=(10,10))

    def Step(self, settings):
        super(Simulation, self).Step(settings)

if __name__ == "__main__":
    Simulation().run()