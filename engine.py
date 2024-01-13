import pygame
from pygame import Surface
from pygame.math import Vector2


class EventSystem:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def call_event(self, event, *args):
        for listener in self.listeners:
            listener(event, *args)


class BaseEventListener:
    def __init__(self, event_system=None):
        self.event_system = self.__class__.default_event_system if event_system is None else event_system
        self.event_system.add_listener(self.__getattribute__(self.__class__.method_name))

    def __del__(self):
        self.event_system.remove_listener(self.__getattribute__(self.__class__.method_name))


class GameEventListener(BaseEventListener):
    default_event_system = None
    method_name = 'listen_event'

    def listen_event(self, event, *args):
        pass


class Renderable(BaseEventListener):
    default_event_system = None
    method_name = '_render'

    def _render(self, event):
        self.render(event.screen, event.deltatime)

    def render(self, screen, deltatime):
        pass


class UpdateEvent:
    def __init__(self, deltatime):
        self.deltatime = deltatime


class RenderEvent:
    def __init__(self, screen, deltatime):
        self.screen = screen
        self.deltatime = deltatime


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

    def render(self, screen: Surface, deltatime):
        scaled_image = pygame.transform.scale(self.image, self.size)
        rotated_image = pygame.transform.rotate(scaled_image, self.rotation)
        render_pos = self.pos + self.center_offset.rotate(-self.rotation) - rotated_image.get_rect().center
        screen.blit(rotated_image, render_pos)


def init_event_systems(common_event_system, render_system):
    GameEventListener.default_event_system = common_event_system
    Renderable.default_event_system = render_system
