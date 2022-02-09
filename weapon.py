from item import Item


class Weapon(Item):
    def __init__(self, attack_damage: int = 1, attack_speed: float = 1, **kwargs):  # attack_speed [attacks per sec]
        super().__init__(**kwargs)
        self._attack_damage = attack_damage
        self._attack_speed = attack_speed  # attack per s
        self._last_attack_time = 0

    @property
    def damage(self):
        return self._attack_damage

    @property
    def attack_delay_ms(self):
        return 1 / (self._attack_speed / 1000)

    def attack(self, *args, **kwargs):
        pass
