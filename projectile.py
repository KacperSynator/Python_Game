import pygame
from moving_object import MovingObject
from object import GroupNames, Object
from abc import ABC, abstractmethod


class Projectile(MovingObject):
    def __init__(self, move_vec: tuple = (0, 0), damage: float = 1, rotate_speed: float = 0, max_range: int = 500, **kwargs):
        super().__init__(**kwargs)
        self._move_vec = (pygame.math.Vector2(move_vec) - self._position).normalize()
        self._start_pos = self._position[:]
        self._max_range = max_range
        self._damage = damage
        self._rotate_speed = rotate_speed

    @staticmethod
    def spawn(**kwargs):
        Projectile(**kwargs)

    def move(self):
        self.rotate_translate(self._rotate_speed, tuple(self._move_vec))
        objs = self.check_group_collisions(Projectile.groups[GroupNames.enemy])
        if objs:
            for obj in objs:
                obj.receive_damage(self._damage)
            self.die()
            return

        if (self._position - self._start_pos).length() > self._max_range:
            self.die()


class Meteorite(Projectile):
    def __init__(self, end_position, radius, **kwargs):
        spawn_offset = pygame.Vector2(-200, -200)
        position = pygame.Vector2(end_position) + spawn_offset
        super().__init__(image_path="assets/projectiles/meteorite.png", move_speed=5, position=position, **kwargs)
        self._move_vec = -1 * spawn_offset
        self._end_position = pygame.Vector2(end_position)
        self._radius = radius

    @staticmethod
    def spawn(**kwargs):
        Meteorite(**kwargs)

    def move(self):
        self.translate(tuple(self._move_vec))
        if (self._position - self._end_position).length() < 5:
            objs = Object.circle_scan_group(Object.groups[GroupNames.enemy], radius=self._radius,
                                            position=tuple(self._end_position))
            if objs:
                for obj in objs:
                    obj.receive_damage(self._damage)
            self.die()

    def draw(self) -> None:
        super().draw()
        line_length = 5
        pygame.draw.circle(self._screen, (0, 255, 0), self._end_position, self._radius, 0)
        pygame.draw.line(self._screen, (0, 0, 0), (self._end_position[0] - line_length, self._end_position[1] - line_length),
                         (self._end_position[0] + line_length, self._end_position[1] + line_length), 2)
        pygame.draw.line(self._screen, (0, 0, 0), (self._end_position[0] - line_length, self._end_position[1] + line_length),
                         (self._end_position[0] + line_length, self._end_position[1] - line_length), 2)