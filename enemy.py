import pygame

from mob import Mob
from object import GroupNames
from object import Group
from UI import Bar


class Enemy(Mob):
    def __init__(self, attack_damage=0, attack_delay=1000, **kwargs):
        super().__init__(**kwargs)
        self._attack_damage = attack_damage
        self._attack_delay = attack_delay
        self._attack_time = 0
        self._bar_center_offset = pygame.Vector2(0, -self._image_size[1] // 2)
        self._health_bar = Bar(screen=self._screen, bar_size=(self._image_size[0] * 0.8, 5), front_color=(255, 0, 0),
                               top_left=self._position + self._bar_center_offset, border_width=1, show_text=False)
        if GroupNames.enemy not in Enemy.groups.keys():
            Enemy.groups[GroupNames.enemy] = Group(GroupNames.enemy)
        Enemy.groups[GroupNames.enemy].add(self)

    def die(self):
        Enemy.groups[GroupNames.enemy].remove(self)
        super().die()

    def draw(self) -> None:
        super().draw()
        self._health_bar.center = self._position + self._bar_center_offset
        self._health_bar.change_fill(self._health / self._max_health)
        self._health_bar.draw()

    def attack(self, target):
        pass
