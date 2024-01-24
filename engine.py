import math
import xml.etree.ElementTree
from typing import Any

import pygame
from Box2D import *
from pygame import Surface
from pygame.math import Vector2


class CollisionEvent:
    def __init__(self, contact, begin=True):
        self.contact = contact
        self.begin = begin

    def get__event_keys(self):
        return [self.contact.fixtureA, self.contact.fixtureB]


class CollisionSystem(b2ContactListener):
    def __init__(self):
        super().__init__()
        self.listeners = {None: []}

    def add_listener(self, listener, fixture=None):
        if fixture not in self.listeners.keys():
            self.listeners[fixture] = []
        self.listeners[fixture].append(listener)

    def BeginContact(self, contact: b2Contact):
        for i in self.listeners.get(contact.fixtureA, []):
            i.begin_contact(contact)
        for i in self.listeners.get(contact.fixtureB, []):
            i.begin_contact(contact)

    def EndContact(self, contact: b2Contact):
        for i in self.listeners.get(contact.fixtureA, []):
            i.end_contact(contact)
        for i in self.listeners.get(contact.fixtureB, []):
            i.end_contact(contact)


class CollisionListener:
    def begin_contact(self, contact: b2Contact):
        pass

    def end_contact(self, contact: b2Contact):
        pass


class Renderable:
    def render(self, screen, camera, deltatime):
        pass


class Updatable:
    def update(self, deltatime):
        pass


class InputEventListener:
    def listen_event(self, event):
        pass


class GameObject:
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.enabled = True
        if isinstance(parent, Scene):
            self.scene = parent
        else:
            self.scene = parent.scene
            parent.children.append(self)
        self.set_enabled(True)


    def load(self, x, y, angle, width, height, pivotX, pivotY, collider):
        body = None
        sprite = None
        if hasattr(self, 'rb_creator'):
            self.body = body = self.rb_creator(collider)
        if hasattr(self, 'sprite'):
            sprite = self.sprite
            self.sprite.width = width
            self.sprite.height = height
            self.sprite.pivot = Vector2(pivotX, pivotY)
        self.transform = Transform(self, sprite, body)
        self.transform.pos = Vector2(x / Transform.PPM, y / Transform.PPM)
        self.transform.rotation = angle

    def set_enabled(self, enabled):
        self.enabled = enabled
        for i in self.children:
            i.set_enabled(enabled)
        if enabled:
            if isinstance(self, Renderable):
                self.scene.renderables.append(self)
            if isinstance(self, InputEventListener):
                self.scene.input_listeners.append(self)
            if isinstance(self, Updatable):
                self.scene.updatables.append(self)
        else:
            if isinstance(self, Renderable):
                self.scene.renderables.remove(self)
            if isinstance(self, InputEventListener):
                self.scene.input_listeners.remove(self)
            if isinstance(self, Updatable):
                self.scene.updatables.remove(self)
    def Start(self):
        pass


class Sprite(GameObject, Renderable):
    def __init__(self, parent, img: pygame.image = None, x=0, y=0, width=None, height=None):
        super().__init__(parent)
        self._pivot = Vector2(0.5, 0.5)
        self.image = img
        self.rotation = 0
        self.scale = Vector2(1, 1)
        self.pos = Vector2(x, y)
        self.pivot = Vector2(0.5, 0.5)
        if width != None:
            self.width = width
        if height != None:
            self.height = height

    @property
    def pivot(self):
        return self._pivot

    @pivot.setter
    def pivot(self, value):
        self._pivot = value
        if self.image is not None:
            self.center_offset = self.image.get_rect().center - Vector2(value.x * self.image.get_width(), value.y * self.image.get_height())

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.center_offset = self.image.get_rect().center - self.pivot

    @property
    def size(self):
        return Vector2(self.width, self.height)

    @size.setter
    def size(self, value):
        if self.image is not None:
            self.scale = Vector2(value.x / self.image.get_rect().w, value.y / self.image.get_rect().h)

    @property
    def width(self):
        if self.image is not None:
            return self.image.get_rect().w * self.scale.x
        return 0

    @property
    def height(self):
        if self.image is not None:
            return self.image.get_rect().h * self.scale.y
        return 0

    @width.setter
    def width(self, value):
        self.size = Vector2(value, self.height)

    @height.setter
    def height(self, value):
        self.size = Vector2(self.width, value)

    def render(self, screen: Surface, camera, deltatime):
        t = Surface((self.image.get_width() + 20, self.image.get_height() + 20), pygame.SRCALPHA)
        t.blit(self.image, (10, 10))
        scaled_image = pygame.transform.scale(t, Vector2((t.get_rect().w*self.scale.x) * camera.scale.x,
                                                         (t.get_rect().h*self.scale.y) * camera.scale.y))
        self.rotation %= 360
        rotation = self.rotation
        if rotation % 90 < 1 or 89 < rotation % 90:
            rotation = round(rotation / 90) * 90
        rotated_image = pygame.transform.rotate(scaled_image, rotation)
        render_pos = self.pos - camera.pos * Transform.PPM
        render_pos = Vector2(render_pos.x * camera.scale.x, render_pos.y * camera.scale.y) - self.center_offset.rotate(
            -rotation) - rotated_image.get_rect().center
        screen.blit(pygame.transform.flip(rotated_image, 0, 1), render_pos)


class Transform(GameObject, Updatable):
    PPM = 40

    def __init__(self, parent, sprite=None, body=None):
        super().__init__(parent)
        self.sprite = sprite
        self.body = body
        self._pos = Vector2(0, 0)
        self._rotation = 0

    def update(self, deltatime):
        if self.body is not None:
            self.pos = Vector2(*self.body.position)
            self.rotation = self.body.angle / math.pi * 180

    @property
    def pos(self):
        self.update(0)
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        if self.body is not None:
            self.body.position = b2Vec2(*value)
        if self.sprite is not None:
            self.sprite.pos = value * Transform.PPM

    @property
    def rotation(self):
        self.update(0)
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        if self.body is not None:
            self.body.angle = value / 180 * math.pi
        if self.sprite is not None:
            self.sprite.rotation = value


class Camera(Transform):
    def __init__(self, scene, scale, width, height):
        super().__init__(scene)
        self.width = width
        self.height = height
        self.scale = scale


class Scene(Renderable, InputEventListener, Updatable):
    def __init__(self):
        super(Renderable, self).__init__()
        super(InputEventListener, self).__init__()
        super(Updatable, self).__init__()
        self.world = b2World((0, -9.81), True)
        self.renderables = []
        self.updatables = []
        self.input_listeners = []
        self.collision_system = CollisionSystem()
        self.world.contactListener = self.collision_system
        self.objects = []
        self.main_camera = None
        self.first_frame = True

    def render(self, screen: Surface, camera, deltatime):
        canvas = Surface((self.main_camera.width * Transform.PPM * self.main_camera.scale.x,
                          self.main_camera.height * Transform.PPM * self.main_camera.scale.y))
        canvas.fill(0)
        for i in self.renderables:
            i.render(canvas, self.main_camera, deltatime)
        screen.blit(pygame.transform.flip(canvas, 0, 1), (0, 0))

    def listen_event(self, event):
        for i in self.input_listeners:
            i.listen_event(event)

    def update(self, deltatime):
        if self.first_frame:
            for i in self.objects:
                i.Start()
            self.first_frame = False
        for i in self.updatables:
            i.update(deltatime)
        self.world.Step(deltatime, 10, 10)

    @staticmethod
    def load(layout_path, proj_path, types=[]):

        root = xml.etree.ElementTree.parse(layout_path).getroot()
        proj = xml.etree.ElementTree.parse(proj_path).getroot().iter('c2project').__next__().iter(
            'object-folder').__next__()
        scene = Scene()
        layout_height = float(root.iter('c2layout').__next__().iter('size').__next__().iter('height').__next__().text)
        for layer in root.iter('c2layout').__next__().iter('layers').__next__().iter('layer'):
            for instance in layer.iter('instances').__next__().iter('instance'):
                type = instance.get('type')
                world = instance.iter('world').__next__()
                x = float(world.iter('x').__next__().text)
                y = layout_height - float(world.iter('y').__next__().text)
                angle = float(world.iter('angle').__next__().text) / math.pi * 180
                width = float(world.iter('width').__next__().text)
                height = float(world.iter('height').__next__().text)
                pivotX = float(world.iter('hotspotX').__next__().text)
                pivotY = float(world.iter('hotspotY').__next__().text)
                collider = []
                for i in proj.iter('object-type'):
                    if i.get('name') == type:
                        try:
                            for point in i.iter('animation-folder').__next__().iter('animation').__next__().iter(
                                    'frame').__next__().iter('collision-poly').__next__().iter('point'):
                                collider.append(((float(point.get('x')) - 0.5) * width / Transform.PPM,
                                                 (float(point.get('y')) - 0.5) * height / Transform.PPM))
                        except:
                            collider = [(-0.5, 0.5), (-0.5, -0.5), (0.5, -0.5), (0.5, 0.5)]
                            collider = [((i[0] * width / Transform.PPM,
                                          i[1] * height / Transform.PPM)) for i in collider]
                            break

                for i in types:
                    if i.__name__ == type:
                        obj = i(scene)
                        obj.load(x, y, angle, width, height, pivotX, pivotY, collider)
                        scene.objects.append(obj)
                        break
        return scene


def RigidBody(world: b2World, collider, pos=Vector2(0, 0), angle=0, body_type=b2_dynamicBody, density=1, friction=0,
              restitution=0.1):
    fixtureDef = b2FixtureDef()
    fixtureDef.shape = b2PolygonShape(vertices=collider)
    fixtureDef.restitution = restitution
    fixtureDef.friction = friction
    fixtureDef.density = density
    bodyDef = b2BodyDef()
    bodyDef.fixtures = fixtureDef
    bodyDef.type = body_type
    bodyDef.position = (pos.x, pos.y)
    bodyDef.angle = angle
    body = world.CreateBody(bodyDef)
    return body
