import moving_object
import pygame


class Mob(moving_object.MovingObject):
    def __init__(self, health: float = 100, **kwargs):
        super().__init__(**kwargs)
        self._health = health

    def heal(self, health: float) -> None:
        self._health += health

    def receive_damage(self, damage: float) -> None:
        self._health -= damage
        if self._health <= 0:
            self.die()

    def attack(self):
        pass



