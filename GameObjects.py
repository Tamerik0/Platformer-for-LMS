from engine import *


def set_sprite_transform(obj, x, y, angle, width, height):
    obj.sprite.width = width
    obj.sprite.height = height
    obj.transform.pos = Vector2(x / Transform.PPM, y / Transform.PPM)
    obj.transform.rotation = angle


def instantiate_physics_sprite_object(scene, x, y, angle, width, height, pivotX, pivotY, collider, type):
    obj = type(scene, collider)
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
        self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Box1)

class Block(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('block.png'))
        self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Block)
class Spike(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spike.png'))
        self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Spike)
class Spider_pad(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('spider_pad.png'))
        self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, Spider_pad)
class red_orb(GameObject):
    def __init__(self, scene, collider):
        super().__init__(scene)
        self.sprite = Sprite(self, pygame.image.load('red_orb.png'))
        self.sprite.pivot = Vector2(16, 16)
        self.body = RigidBody(scene.world, collider, body_type=b2_staticBody)
        self.transform = Transform(self, self.sprite, self.body)

    @staticmethod
    def instantiate(*args):
        return instantiate_physics_sprite_object(*args, red_orb)
class Spike1(Spike):
    pass
class Spike2(Spike):
    pass
