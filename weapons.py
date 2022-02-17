from item import Item
from abc import ABC, abstractmethod
from projectiles import Projectile
import functools
import pygame


class Weapon(Item, ABC):
    def _check_delay(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            if self._last_attack_time + self.attack_delay_ms <= pygame.time.get_ticks():
                self._last_attack_time = pygame.time.get_ticks()
                return fn(self, *args, **kwargs)
        return wrapper

    def __init__(self, attack_damage: int = 1, attack_speed: float = 1, **kwargs):  # attack_speed [attacks per sec]
        Item.__init__(self, **kwargs)
        self._attack_damage = attack_damage
        self._attack_speed = attack_speed  # attack per s
        self._last_attack_time = -self.attack_delay_ms

    @property
    def damage(self):
        return self._attack_damage

    @property
    def attack_delay_ms(self):
        return 1 / (self._attack_speed / 1000)

    @_check_delay
    @abstractmethod
    def attack(self, *args, **kwargs):
        pass

    _check_delay = staticmethod(_check_delay)


class RangeWeapon(Weapon):
    weapon_list = {"wand": {"name": "wand", "attack_damage": 5, "attack_speed": 2, "projectile_range": 500, "angle": 45,
                             "projectile_start_offset": (0, -20), "image_path": "assets/items/weapons/staff.png",
                             "weapon_offset": (22, 0),
                            "projectile": {"image_path": "assets/projectiles/snowflake.png", "rotate_speed": 3,
                                           "move_speed": 5, "rotating": True}},

                   "crystal_wand": {"name": "crystal_wand", "attack_damage": 10, "attack_speed": 1, "projectile_range": 500,
                             "angle": 45, "projectile_start_offset": (0, -20), "image_path": "assets/items/weapons/staff2.png",
                             "weapon_offset": (22, 0),
                             "projectile": {"image_path": "assets/projectiles/fire.png", "rotate_speed": 3,
                                            "move_speed": 5, "rotating": False}},
                   }

    def __init__(self, projectile_range: int = 500, projectile_start_offset: tuple = (0, 0),  **kwargs):
        super().__init__(**kwargs)
        self._projectile_range = projectile_range
        self._projectile_start_offset = pygame.Vector2(projectile_start_offset)

    @Weapon._check_delay
    def attack(self, mouse_position):
        Projectile.spawn(screen=self._screen, end_position=mouse_position, damage=RangeWeapon.weapon_list[self._name]["attack_damage"],
                         position=self._projectile_start_offset+self._position, **RangeWeapon.weapon_list[self._name]["projectile"])
