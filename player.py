from mob import Mob
import pygame
from range_weapon import RangeWeapon
from object import Group, GroupNames
from HUD import HUD
from skills import MeteoriteSkill
from weapon import Weapon


class Player(Mob):
    def __init__(self, **kwargs):
        super().__init__(health=70, move_speed=2, image_path="assets/mobs/player/magician_no_weapon.png", **kwargs)
        self._hud = HUD(screen=self._screen, player=self)
        self._weapon_offset = pygame.Vector2(RangeWeapon.weapon_list["wand"]["weapon_offset"])
        self._weapon = RangeWeapon(screen=self._screen, position=self._position + self._weapon_offset,
                                   **RangeWeapon.weapon_list["wand"])
        self._skill = MeteoriteSkill(screen=self._screen)
        if GroupNames.player not in Player.groups.keys():
            Player.groups[GroupNames.player] = Group(GroupNames.player)
        Player.groups[GroupNames.player].add(self)

    @property
    def weapon(self):
        return self._weapon

    def auto_attack(self, mouse_position):
        self._weapon.attack(mouse_position)

    def skill(self, mouse_position):
        self._skill.use(position=mouse_position)

    def pick_item(self):
        objs = self.check_group_collisions(self.groups[GroupNames.item])
        if objs and len(objs) > 1:
            objs.remove(self._weapon)
            self.switch_weapon(objs[0])

    def switch_weapon(self, weapon):
        self._weapon.position = weapon.position
        self._weapon_offset = pygame.Vector2(RangeWeapon.weapon_list[weapon.name]["weapon_offset"])
        self._weapon = weapon

    def move(self) -> None:
        self.translate(self._move_vec)
        self._weapon.position = self._position + self._weapon_offset

    def draw(self) -> None:
        super().draw()
        self._hud.draw()
