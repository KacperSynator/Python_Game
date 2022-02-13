from item import Item
from abc import ABC, abstractmethod


class Weapon(Item, ABC):
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

    @abstractmethod
    def attack(self, *args, **kwargs):
        pass
