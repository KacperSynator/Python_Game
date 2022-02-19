import pygame
from moving_object import MovingObject
from object import GroupNames, Object
from abc import ABC, abstractmethod


class Projectile(MovingObject):
    def __init__(self, end_position: tuple = (0, 0), damage: float = 1, rotate_speed: float = 0, max_range: int = 500,
                 target_player_enemies: tuple = (False, True), rotating: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._move_vec = (pygame.math.Vector2(end_position) - self._position).normalize()
        if not rotating:
            self.rotate(self._move_vec.angle_to(pygame.Vector2(0, 1)))  # front of projectile must be at the bottom of image
        self._start_pos = self._position[:]
        self._end_position = pygame.Vector2(end_position)
        self._max_range = max_range
        self._damage = damage
        self._rotate_speed = rotate_speed
        self._target_pl_en = target_player_enemies
        self._rotating = rotating

    @staticmethod
    def spawn(**kwargs):
        Projectile(**kwargs)

    def handle_collisions(self) -> bool:
        objs = []
        if self._target_pl_en[1] and self.check_group_collisions(Projectile.groups[GroupNames.enemy]):
            objs.append(*self.check_group_collisions(Projectile.groups[GroupNames.enemy]))
        if self._target_pl_en[0] and self.check_group_collisions(Projectile.groups[GroupNames.player]):
            objs.append(*self.check_group_collisions(Projectile.groups[GroupNames.player]))
        if objs:
            for obj in objs:
                obj.receive_damage(self._damage)
            self.die()
            return True
        return False

    def move(self):
        if self._rotating:
            self.rotate_translate(self._rotate_speed, tuple(self._move_vec))
        else:
            self.translate(tuple(self._move_vec))
        if self.handle_collisions():
            return

        if (self._position - self._start_pos).length() > self._max_range:
            self.die()


class SlerpProjectile(Projectile):
    def __init__(self, end_position, **kwargs):
        super().__init__(end_position=end_position, **kwargs)
        self._pivot_point = self._position + (self._end_position - self._start_pos) / 2 + ((self._end_position - self._start_pos) / 2).rotate(90)

    def move(self):
        next_position = self._pivot_point + (self._position - self._pivot_point).slerp(self._end_position - self._pivot_point, 0.1)
        self._move_vec = next_position - self._position
        self.translate(self._move_vec)
        if self.handle_collisions():
            return
        if (self._position - self._end_position).length() < 5:
            self.die()


class Meteorite(Projectile):
    def __init__(self, end_position, radius, **kwargs):
        spawn_offset = pygame.Vector2(-200, -200)
        spawn_position = pygame.Vector2(end_position) + spawn_offset
        super().__init__(image_path="assets/projectiles/meteorite.png", move_speed=5, position=spawn_position,
                         end_position=end_position, **kwargs)
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
        # pygame.draw.circle(self._screen, (0, 255, 0), self._end_position, self._radius, 0)
        pygame.draw.line(self._screen, (0, 0, 0), (self._end_position[0] - line_length, self._end_position[1] - line_length),
                          (self._end_position[0] + line_length, self._end_position[1] + line_length), 2)
        pygame.draw.line(self._screen, (0, 0, 0), (self._end_position[0] - line_length, self._end_position[1] + line_length),
                          (self._end_position[0] + line_length, self._end_position[1] - line_length), 2)

