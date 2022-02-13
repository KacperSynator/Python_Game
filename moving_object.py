import pygame
from object import Object, Group, GroupNames
from abc import ABC, abstractmethod


class MovingObject(Object, ABC):
    def __init__(self, move_speed: float = 0.5, move_vec: tuple = (0, 0), solve_collision: bool = False, **kwargs):
        Object.__init__(self, **kwargs)
        self._move_speed = move_speed
        self._collisions = []
        self._solve = solve_collision
        if move_vec != (0, 0):
            self._move_vec = pygame.math.Vector2(move_vec).normalize()
        else:
            self._move_vec = pygame.math.Vector2(move_vec)
        if GroupNames.moving_object not in MovingObject.groups.keys():
            MovingObject.groups[GroupNames.moving_object] = Group(GroupNames.moving_object)
        MovingObject.groups[GroupNames.moving_object].add(self)

    def die(self):
        MovingObject.groups[GroupNames.moving_object].remove(self)
        Object.die(self)

    @property
    def move_vec(self):
        return self._move_vec

    @move_vec.setter
    def move_vec(self, vec: tuple):
        if vec != (0.0, 0.0):
            self._move_vec = pygame.math.Vector2(vec).normalize()
        else:
            self._move_vec = pygame.math.Vector2(vec)

    @property
    def solve(self) -> bool:
        return self._solve

    @solve.setter
    def solve(self, state: bool):
        self._solve = state

    def translate(self, vector: tuple):
        if vector == (0, 0):
            self._position += pygame.math.Vector2(vector) * self._move_speed
        else:
            self._position += pygame.math.Vector2(vector).normalize() * self._move_speed
        objs = self.check_group_collisions(MovingObject.groups[GroupNames.moving_object])
        self._collisions = objs
        if objs:
            for obj in objs:
                if self.solve:
                    self.solve_collision(obj)

    def rotate(self, angle: float):
        self._angle += angle
        if self._angle > 180:
            self._angle -= 360
        elif self._angle < -180:
            self._angle += 360

    def rotate_translate(self, angle: float, vector: tuple):
        self.rotate(angle)
        self.translate(vector)

    def solve_collision(self, obj):
        to_other_vec = pygame.Vector2(obj.position) - pygame.Vector2(self.position)
        current_distance = to_other_vec.length()
        max_distance = self.image_size[0]/2 + obj.image_size[0]/2
        move_vec = to_other_vec.normalize()*current_distance/max_distance/2
        if obj.solve:
            obj.position = obj.position + move_vec
            self.position = self.position - move_vec
        else:
            self.position = self.position - 2*move_vec

    @abstractmethod
    def move(self):
        pass

    @staticmethod
    def move_all():
        for moving_object in MovingObject.groups[GroupNames.moving_object].list:
            moving_object.move()
