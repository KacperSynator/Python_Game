import pygame
from moving_object import MovingObject
from object import GroupNames


class Projectile(MovingObject):
    def __init__(self, move_vec: tuple, damage: float = 1, rotate_speed: float = 0, max_range: int = 500, **kwargs):
        super().__init__(**kwargs)
        self._move_vec = (pygame.math.Vector2(move_vec) - self._position).normalize()
        self._start_pos = self._position[:]
        self._max_range = max_range
        self._damage = damage
        self._rotate_speed = rotate_speed

    def move(self):
        self.rotate_translate(self._rotate_speed, self._move_vec)
        obj = self.check_group_collisions(Projectile.groups[GroupNames.enemy])
        if obj is not None:
            obj.receive_damage(self._damage)
            self.die()
            return

        if (self._position - self._start_pos).length() > self._max_range:
            self.die()
