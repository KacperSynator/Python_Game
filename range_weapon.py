import pygame
from weapon import Weapon
from projectile import Projectile


class RangeWeapon(Weapon):
    weapon_list = {"wand": {"name": "wand", "attack_damage": 5, "attack_speed": 2, "projectile_range": 500, "angle": 45,
                             "projectile_start_offset": (0, -20), "image_path": "assets/items/weapons/staff.png",
                             "weapon_offset": (22, 0),
                            "projectile": {"image_path": "assets/projectiles/snowflake.png", "rotate_speed": 3, "move_speed": 5}},

                   "crystal_wand": {"name": "crystal_wand", "attack_damage": 10, "attack_speed": 1, "projectile_range": 500,
                             "angle": 45, "projectile_start_offset": (0, -20), "image_path": "assets/items/weapons/staff2.png",
                             "weapon_offset": (22, 0),
                             "projectile": {"image_path": "assets/projectiles/fire.png", "rotate_speed": 3, "move_speed": 5}},
                   }

    def __init__(self, projectile_range: int = 500, projectile_start_offset: tuple = (0, 0),  **kwargs):
        super().__init__(**kwargs)
        self._projectile_range = projectile_range
        self._projectile_start_offset = pygame.Vector2(projectile_start_offset)

    def attack(self, mouse_position):
        if self._last_attack_time + self.attack_delay_ms <= pygame.time.get_ticks():
            Projectile.spawn(screen=self._screen, move_vec=mouse_position, damage=RangeWeapon.weapon_list[self._name]["attack_damage"],
                       position=self._projectile_start_offset+self._position, **RangeWeapon.weapon_list[self._name]["projectile"])

            self._last_attack_time = pygame.time.get_ticks()
