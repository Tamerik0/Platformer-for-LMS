import pygame

from engine import *

restart = lambda: print('restart')
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
        self.rb_creator = lambda collider: RigidBody(scene.world, collider, body_type=b2_staticBody, friction=1)


class Spike(GameObject, CollisionListener):
    def __init__(self, scene):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spike.png'))
        self.rb_creator = lambda collider: RigidBody(scene.world, collider, body_type=b2_staticBody)
    def Start(self):
        self.scene.collision_system.add_listener(self, self.body.fixtures[0])
    def begin_contact(self, contact: b2Contact):
        if 'Player' in [contact.fixtureA.userData, contact.fixtureB.userData]:
            restart()


class Spider_pad(GameObject, CollisionListener):
    def __init__(self, scene):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spider_pad.png'))
        self.rb_creator = lambda collider: RigidBody(scene.world, collider, body_type=b2_staticBody)
    def Start(self):
        self.scene.collision_system.add_listener(self, self.body.fixtures[0])
    def begin_contact(self, contact: b2Contact):
        if 'Player' in [contact.fixtureA.userData, contact.fixtureB.userData]:
            player = contact.fixtureA.body if contact.fixtureA.userData == 'Player' else contact.fixtureB.body
            player.linearVelocity = b2Vec2(0, 20)
            self.scene.world.gravity = b2Vec2(0, 9.81)
            print('spider')

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


class Lovushka1(Spike, Updatable):
    def Start(self):
        super().Start()
        self.set_enabled(False)
    def update(self, deltatime):
        self.body.transform.position += b2Vec2(0, -10*deltatime)


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
            self.lovushka.set_enabled(True)


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
        self.speed = 3
        self.acceleration = 30
        self.left_point = 999
        self.right_point = -999
        self.jump_cd = 0

    def rb_creator(self, collider):
        body = RigidBody(self.scene.world, collider, friction=0.5, restitution=0)
        body.fixtures[0].userData = 'Player'
        for i in body.fixtures[0].shape.vertices:
            if i[0] < self.left_point:
                self.left_point = i[0]
            if i[0] > self.right_point:
                self.right_point = i[0]
        return body

    def update(self, deltatime):
        self.jump_cd -= deltatime
        move = int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a])
        if abs(self.body.linearVelocity.x) <= self.speed or self.body.linearVelocity.x * move < 0:
            self.body.linearVelocity += b2Vec2(move * self.acceleration * deltatime, 0)
        # print(pygame.key.get_pressed()[pygame.K_SPACE], self.jump_cd)
        d = -1 if self.scene.world.gravity.y > 0 else 1
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.jump_cd<=0:
            for contact in self.body.contacts:
                for point in contact.contact.worldManifold.points:
                    if ((point[1] < self.body.position.y and d==1) or (point[1] > self.body.position.y and d==-1)) and self.left_point + self.body.position.x <= point[
                        0] <= self.right_point + self.body.position.x and point != (0, 0):
                        self.body.linearVelocity += b2Vec2(0, 5)*d
                        self.body.transform.position += b2Vec2(0, 0.1)*d
                        self.jump_cd = 0.1
                        break
