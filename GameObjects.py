import pygame

from engine import *


class Box(GameObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('box.png'))
        self.rb_creator = (lambda collider: RigidBody(scene.world, collider))


class Box1(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('box.png'))
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)


class Block(GameObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('block.png'))
        self.rb_creator = lambda collider: RigidBody(scene.world, collider, body_type=b2_staticBody)


class Spike(GameObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spike.png'))
        self.rb_creator = lambda collider: RigidBody(scene.world, collider, body_type=b2_staticBody)


class Spider_pad(GameObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spider_pad.png'))
        self.rb_creator = lambda collider: RigidBody(scene.world, collider, body_type=b2_staticBody)


class red_orb(GameObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('red_orb.png'))
        self.rb_creator = lambda collider: RigidBody(scene.world, collider, body_type=b2_staticBody)


class Background(GameObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.sprite = Sprite(parent, pygame.image.load('bg.png'))


class Spike1(Spike):
    pass


class Spike2(Spike):
    pass


class Lovushka1(Spike):
    pass


class Trigger1(GameObject):
    def Start(self):
        for i in self.scene.objects:
            if isinstance(i, Lovushka1):
                self.lovushka = i

    def rb_creator(self, collider):
        fixtureDef = b2FixtureDef()
        fixtureDef.shape = b2PolygonShape(vertices=collider)
        fixtureDef.isSensor = True
        bodyDef = b2BodyDef()
        bodyDef.fixtures = fixtureDef
        bodyDef.type = b2_staticBody
        body = self.scene.world.CreateBody(bodyDef)
        self.scene.collision_system.add_listener(self, body.fixtures[0])
        return body

    def begin_contact(self, contact: b2Contact):
        if 'Player' in [contact.fixtureA.userData, contact.fixtureB.userData]:
            self.lovushka.body.position -= b2Vec2(1, 0)

    def end_contact(self, *args):
        pass

    @staticmethod
    def instantiate(scene, x, y, angle, width, height, pivotX, pivotY, collider):
        obj = Trigger1(scene, collider)
        obj.transform.pos = Vector2(x / Transform.PPM, y / Transform.PPM)
        obj.transform.rotation = angle
        return obj


class Player(GameObject, Updatable):
    def __init__(self, parent):
        super().__init__(parent)
        self.sprite = Sprite(self, pygame.image.load('player.png'))
        self.speed = 2
        self.acceleration = 50
        self.left_point = 999
        self.right_point = -999

    def rb_creator(self, collider):
        body = RigidBody(self.scene.world, collider)
        body.fixtures[0].userData = 'Player'
        for i in body.fixtures[0].shape.vertices:
            if i[0] < self.left_point:
                self.left_point = i[0]
            if i[0] > self.right_point:
                self.right_point = i[0]
        return body

    def update(self, deltatime):
        move = int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a])
        if abs(self.body.linearVelocity.x) <= self.speed or self.body.linearVelocity.x * move < 0:
            self.body.linearVelocity += b2Vec2(move * self.acceleration * deltatime, 0)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            for contact in self.body.contacts:
                for point in contact.contact.worldManifold.points:
                    if point[1] < self.body.position.y and self.left_point + self.body.position.x <= point[
                        0] <= self.right_point + self.body.position.x and point != (0, 0):
                        self.body.linearVelocity += b2Vec2(0, self.acceleration * deltatime)
                        break
