import math
import xml.etree.ElementTree

import pygame
from Box2D import *
from pygame import Surface
from pygame.math import Vector2


class EventSystem:
    def __init__(self):
        self.listeners = dict()

    def add_listener(self, listener, event_type=None, key=None):
        if isinstance(listener, BaseEventListener):
            listener.add_to_system(self)
        else:
            if event_type not in self.listeners.keys():
                self.listeners[event_type] = {None: []}
            if key not in self.listeners[event_type]:
                self.listeners[key] = []
            self.listeners[event_type][key].append(listener)

    def call_event(self, event):
        keys = [None]
        if hasattr(event, 'get_event_keys'):
            keys_ = event.get_event_keys
            if keys_ is not None:
                keys = keys_
        if event.__class__ in self.listeners.keys():
            for i in keys:
                for j in self.listeners[event.__class__][i]:
                    j(event)

    def remove_listener(self, listener, event_type=None, key=None):
        if isinstance(listener, BaseEventListener):
            listener = listener.get_event_method()
        if event_type is None:
            for i in self.listeners.items():
                for j in i.items():
                    j.remove(listener)
        else:
            if key is None:
                for i in self.listeners[event_type]:
                    i.remove(listener)
            else:
                self.listeners[event_type][key].remove(listener)


class CollisionEvent:
    def __init__(self, contact, begin=True):
        self.contact = contact
        self.begin = begin

    def get__event_keys(self):
        return [self.contact.fixtureA, self.contact.fixtureB]


class UpdateEvent:
    def __init__(self, deltatime):
        self.deltatime = deltatime


class RenderEvent:
    def __init__(self, screen, deltatime, camera=None):
        self.screen = screen
        self.camera = camera
        self.deltatime = deltatime


class CollisionSystem(b2ContactListener):
    def __init__(self, event_system):
        super().__init__()
        self.event_system = event_system

    def BeginContact(self, contact: b2Contact):
        self.event_system.call_event(CollisionEvent(contact, True))

    def EndContact(self, contact: b2Contact):
        self.event_system.call_event(CollisionEvent(contact, False))


class BaseEventListener:
    def __init__(self):
        self.event_systems = set()

    def add_to_system(self, event_system, listener_type):
        for i in self.get_event_keys():
            event_system.add_listener(listener_type.get_event_method(self), listener_type.get_event_type(self), i)
        self.event_systems.add(event_system)

    def remove(self, listener_type):
        for system in self.event_systems:
            system.remove_listener(listener_type.get_event_method(self), listener_type.get_event_type(self))

    def get_event_method(self):
        return lambda *args: None

    def get_event_type(self):
        return None

    def get_event_keys(self):
        return [None]


class Renderable(BaseEventListener):
    def get_event_method(self):
        return self._render

    def get_event_type(self):
        return RenderEvent

    def _render(self, event):
        self.render(event.screen, event.camera, event.deltatime)

    def render(self, screen, camera, deltatime):
        pass


class Updatable(BaseEventListener):
    def get_event_method(self):
        return self._update

    def get_event_type(self):
        return UpdateEvent

    def _update(self, event):
        self.update(event.deltatime)

    def update(self, deltatime):
        pass


class GameEventListener(BaseEventListener):
    def get_event_method(self):
        return self.listen_event

    def get_event_type(self):
        return pygame.event.Event

    def listen_event(self, event):
        pass


class Sprite(Renderable):
    def __init__(self, img=None):
        super().__init__()
        self._pivot = Vector2(0, 0)
        self.image = img
        self.rotation = 0
        self.scale = Vector2(1, 1)
        self.pos = Vector2(0, 0)

    @property
    def pivot(self):
        return self._pivot

    @pivot.setter
    def pivot(self, value):
        self._pivot = value
        if self.image is not None:
            self.center_offset = self.image.get_rect().center - value

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
        scaled_image = pygame.transform.scale(self.image,
                                              Vector2(self.size.x * camera.scale.x, self.size.y * camera.scale.y))
        self.rotation %= 360
        rotation = self.rotation
        if rotation % 90 < 0.1 or 89.9 < rotation % 90:
            rotation = round(rotation / 90) * 90
        rotated_image = pygame.transform.rotate(scaled_image, rotation)
        render_pos = self.pos - camera.pos * Transform.PPM
        render_pos = Vector2(render_pos.x * camera.scale.x, render_pos.y * camera.scale.y) - self.center_offset.rotate(
            -rotation) - rotated_image.get_rect().center
        screen.blit(rotated_image, render_pos)


class Transform(Updatable):
    PPM = 40

    def __init__(self, sprite=None, body=None):
        super().__init__()
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
    def __init__(self, scale, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.scale = scale


class Scene(Renderable, GameEventListener, Updatable):
    def __init__(self):
        super(Renderable, self).__init__()
        super(GameEventListener, self).__init__()
        super(Updatable, self).__init__()
        self.world = b2World((0, -9.81), True)
        self.event_system = EventSystem()
        self.collision_system = CollisionSystem(self.event_system)
        self.world.contactListener = self.collision_system
        self.objects = []
        self.main_camera = None

    def render(self, screen: Surface, camera, deltatime):
        canvas = Surface((self.main_camera.width * Transform.PPM * self.main_camera.scale.x,
                          self.main_camera.height * Transform.PPM * self.main_camera.scale.y))
        self.event_system.call_event(RenderEvent(canvas, deltatime, self.main_camera))
        screen.blit(pygame.transform.flip(canvas, 0, 1), (0, 0))

    def listen_event(self, event, *args):
        self.event_system.call_event(event, *args)

    def update(self, deltatime):
        self.world.Step(deltatime, 6, 6)
        self.event_system.call_event(UpdateEvent(deltatime))

    @staticmethod
    def load(layout_path, proj_path, types: list[type] = []):
        root = xml.etree.ElementTree.parse(layout_path).getroot()
        proj = xml.etree.ElementTree.parse(proj_path).getroot().iter('c2project').__next__().iter(
            'object-folder').__next__()
        scene = Scene()
        for instance in root.iter('c2layout').__next__().iter('layers').__next__().iter('layer').__next__().iter(
                'instances').__next__().iter('instance'):
            type = instance.get('type')
            world = instance.iter('world').__next__()
            x = float(world.iter('x').__next__().text)
            y = float(world.iter('y').__next__().text)
            angle = float(world.iter('angle').__next__().text)
            width = float(world.iter('width').__next__().text)
            height = float(world.iter('height').__next__().text)
            pivotX = float(world.iter('hotspotX').__next__().text)
            pivotY = float(world.iter('hotspotY').__next__().text)
            collider = []
            for i in proj.iter('object-type'):
                if i.get('name') == type:
                    for point in i.iter('animation-folder').__next__().iter('animation').__next__().iter(
                            'frame').__next__().iter('collision-poly').__next__().iter('point'):
                        collider.append(Vector2(float(point.get('x')), float(point.get('y'))))
            for i in types:
                if i.__name__ == type:
                    obj = i.instantiate(scene, x, y, angle, width, height, pivotX, pivotY, collider)
                    break

            scene.objects.append(obj)
            if isinstance(obj, Renderable):
                obj.add_to_system(scene.event_system, Renderable)
            if isinstance(obj, GameEventListener):
                obj.add_to_system(scene.event_system, GameEventListener)
            if isinstance(obj, Updatable):
                obj.add_to_system(scene.event_system, Updatable)
        return scene
