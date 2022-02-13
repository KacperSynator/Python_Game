from moving_object import MovingObject
import pygame


class Mob(MovingObject):
    def __init__(self, health: float = 100, **kwargs):
        super().__init__(solve_collision=True, **kwargs)
        self._health = health
        self._max_health = health

    @property
    def health(self):
        return self._health

    @property
    def max_health(self):
        return self._max_health

    def heal(self, health: float) -> None:
        self._health += health

    def receive_damage(self, damage: float) -> None:
        self._health -= damage
        if self._health <= 0:
            self.die()





