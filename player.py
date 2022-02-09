from mob import Mob
import pygame
from range_weapon import RangeWeapon
from object import GroupNames
from object import Group
from UI import UI


class Player(Mob):
    def __init__(self, **kwargs):
        super().__init__(health=70, move_speed=2, image_path="assets/mobs/player/magician_no_weapon.png", **kwargs)
        self._ui = UI(screen=self._screen, player=self)
        self._weapon_name = "wand"
        self._weapon_offset = pygame.Vector2(RangeWeapon.weapon_list[self._weapon_name]["weapon_offset"])
        self._weapon = RangeWeapon(screen=self._screen, position=self._position + self._weapon_offset,
                                   **RangeWeapon.weapon_list[self._weapon_name])
        if GroupNames.player not in Player.groups.keys():
            Player.groups[GroupNames.player] = Group(GroupNames.player)
        Player.groups[GroupNames.player].add(self)

    def auto_attack(self, mouse_position):
        self._weapon.attack(mouse_position)

    def switch_weapon(self, weapon_name):
        self._weapon.die()
        self._weapon_name = weapon_name
        self._weapon_offset = pygame.Vector2(RangeWeapon.weapon_list[self._weapon_name]["weapon_offset"])
        self._weapon = RangeWeapon(screen=self._screen, position=self._position + self._weapon_offset,
                                   **RangeWeapon.weapon_list[self._weapon_name])

    def move(self) -> None:
        self.translate(self._move_vec)
        self._weapon.position = self._position + self._weapon_offset

    def draw(self) -> None:
        super().draw()
        self._ui.draw()
