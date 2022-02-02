import mob
import pygame
from object import GroupNames
from object import Group


class Imp(mob.Mob):
    def __init__(self, **kwargs):
        super().__init__(image_path="assets/mobs/enemies/imp.png", **kwargs)
        self._move_speed = 1.4
        self._health = 20
        if GroupNames.enemy not in Imp.groups.keys():
            Imp.groups[GroupNames.enemy] = Group(GroupNames.enemy)
        Imp.groups[GroupNames.enemy].add(self)

    def move(self):
        player = Imp.groups[GroupNames.player].list[0]
        self._move_vec = (pygame.math.Vector2(player.position) - self._position).normalize()
        self.translate(self._move_vec)
