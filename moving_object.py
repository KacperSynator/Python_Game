import pygame
import object
from object import GroupNames as GroupNames
from object import Group


class MovingObject(object.Object):
    def __init__(self, move_speed: float = 0.5, move_vec: tuple = (0, 0), **kwargs):
        super().__init__(**kwargs)
        self._move_speed = move_speed
        if move_vec != (0, 0):
            self._move_vec = pygame.math.Vector2(move_vec).normalize()
        else:
            self._move_vec = pygame.math.Vector2(move_vec)
        if GroupNames.moving_object not in MovingObject.groups.keys():
            MovingObject.groups[GroupNames.moving_object] = Group(GroupNames.moving_object)
        MovingObject.groups[GroupNames.moving_object].add(self)

    def die(self):
        MovingObject.groups[GroupNames.moving_object].remove(self)

    @property
    def move_vec(self):
        return self._move_vec

    @move_vec.setter
    def move_vec(self, vec: tuple):
        if vec != (0.0, 0.0):
            self._move_vec = pygame.math.Vector2(vec).normalize()
        else:
            self._move_vec = pygame.math.Vector2(vec)

    def translate(self, vector: tuple):
        self._position += pygame.math.Vector2(vector) * self._move_speed
        self.draw()

    def rotate(self, angle: float):
        self._angle += angle
        self.draw()

    def rotate_translate(self, angle: float, vector: tuple):
        self.rotate(angle)
        self.translate(vector)
        self.draw()

    def move(self):
        pass

    @staticmethod
    def move_all():
        for moving_object in MovingObject.groups[GroupNames.moving_object].list:
            moving_object.move()
