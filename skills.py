import pygame
from abc import ABC, abstractmethod
from projectile import Meteorite
import functools


class Skill(ABC):
    def _check_cooldown(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            if self._last_use_time + self._cooldown <= pygame.time.get_ticks():
                self._last_use_time = pygame.time.get_ticks()
                return fn(self, *args, **kwargs)
        return wrapper

    def __init__(self, name: str, cooldown_s: float, **kwargs):
        self._name = name
        self._cooldown = cooldown_s * 1000  # convert to ms
        self._last_use_time = -self._cooldown

    @property
    def remaining_cooldown(self) -> float:
        remaining_time = self._last_use_time + self._cooldown - pygame.time.get_ticks()
        return remaining_time if remaining_time > 0.0 else 0.0

    @property
    def name(self):
        return self._name

    @_check_cooldown
    @abstractmethod
    def use(self, *args, **kwargs):
        pass

    _check_cooldown = staticmethod(_check_cooldown)


class MeteoriteSkill(Skill):
    def __init__(self, screen):
        Skill.__init__(self, name="Meteorite", cooldown_s=10)
        self._screen = screen

    @Skill._check_cooldown
    def use(self, position: tuple):
        Meteorite(damage=20, radius=30, screen=self._screen, end_position=position)


class Blink(Skill):
    def __init__(self, moving_object, max_range: int = 100):
        Skill.__init__(self, name="Blink", cooldown_s=5)
        self._max_range = max_range
        self._moving_object = moving_object

    @Skill._check_cooldown
    def use(self, position: tuple):
            move_vec = pygame.Vector2(position) - self._moving_object.position
            if move_vec.length() > self._max_range:
                move_vec = move_vec.normalize() * self._max_range
            self._moving_object.translate(tuple(move_vec), normalize=False)
