import mob
import pygame
from object import GroupNames
from object import Group


class Player(mob.Mob):
    def __init__(self, **kwargs):
        super().__init__(health=100, image_path="assets/mobs/player/magician.png", **kwargs)
        self._move_speed = 2
        if GroupNames.player not in Player.groups.keys():
            Player.groups[GroupNames.player] = Group(GroupNames.player)
        Player.groups[GroupNames.player].add(self)

    def move(self):
        self.translate(self._move_vec)

