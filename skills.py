import pygame
from abc import ABC, abstractmethod
from projectile import Meteorite


class Skill(ABC):
    def __init__(self, name: str, cooldown_s: float, **kwargs):
        self._name = name
        self._cooldown = cooldown_s * 1000  # convert to ms
        self._last_use_time = -self._cooldown

    @property
    def name(self):
        return self._name

    @abstractmethod
    def use(self, *args, **kwargs):
        pass


class MeteoriteSkill(Skill):
    def __init__(self, screen):
        Skill.__init__(self, name="Meteorite", cooldown_s=10)
        self._screen = screen

    def use(self, position: tuple):
        if self._last_use_time + self._cooldown <= pygame.time.get_ticks():
            self._last_use_time = pygame.time.get_ticks()
            Meteorite(damage=20, radius=30, screen=self._screen, end_position=position)
