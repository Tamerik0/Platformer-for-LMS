import pygame

from engine import *


def set_sprite_transform(obj, x, y, angle, width, height):
    obj.sprite.width = width
    obj.sprite.height = height
    obj.transform.pos = Vector2(x / Transform.PPM, y / Transform.PPM)
    obj.transform.rotation = angle


def instantiate_physics_sprite_object(scene, x, y, angle, width, height, pivotX, pivotY, collider, t):
    obj = t(scene, collider)
    set_sprite_transform(obj, x, y, angle, width, height)
    return obj


class Box(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('box.png'))
        self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Box)


class Box1(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('box.png'))
        # self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Box1)


class Block(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('block.png'))
        # self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Block)


class Spike(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spike.png'))
        # self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Spike)


class Spider_pad(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spider_pad.png'))
        # self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Spider_pad)


class red_orb(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('red_orb.png'))
        # self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, red_orb)


class Background(GameObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.sprite = Sprite(parent, pygame.image.load('bg.png'))
        self.transform = Transform(self, self.sprite, None)

    @staticmethod
    def instantiate(scene, x, y, angle, width, height, pivotX, pivotY, collider):
        obj = Background(scene)
        set_sprite_transform(obj, x, y, angle, width, height)
        return obj


class Spike1(Spike):
    pass


class Spike2(Spike):
    pass
class Lovushka1(Spike):
    pass

class Player(GameObject, Updatable):
    def __init__(self, parent, collider):
        super().__init__(parent)
        self.sprite = Sprite(self, pygame.image.load('player.png'))
        self.body = RigidBody(self.scene.world, collider=collider)
        self.transform = Transform(self, self.sprite, self.body)
        self.speed = 2
        self.acceleration = 50
        self.left_point = 999
        self.right_point = -999
        for i in self.body.fixtures[0].shape.vertices:
            if i[0] < self.left_point:
                self.left_point = i[0]
            if i[0] > self.right_point:
                self.right_point = i[0]

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

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Player)
