import moving_object
import pygame
import imp
from object import GroupNames


class Projectile(moving_object.MovingObject):
    def __init__(self, move_vec: tuple, **kwargs):
        super().__init__(image_path="assets/projectiles/snowflake_white.png", **kwargs)
        self._move_vec = (pygame.math.Vector2(move_vec) - self._position).normalize()
        self._move_speed = 5
        self._start_pos = self._position[:]
        self._max_range = 500

    def move(self):
        self.rotate_translate(3, self._move_vec)
        obj = self.check_group_collisions(Projectile.groups[GroupNames.enemy])
        if obj is not None:
            obj.receive_damage(10)
            self.die()
            return

        if (self._position - self._start_pos).length() > self._max_range:
            self.die()
