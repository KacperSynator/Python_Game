from enemy import Enemy
import pygame
from object import GroupNames


class Imp(Enemy):
    def __init__(self, **kwargs):
        super().__init__(image_path="assets/mobs/enemies/imp.png", health=20, move_speed=1.4, attack_damage=5,
                         attack_delay=1000, **kwargs)

    def move(self):
        player = Imp.groups[GroupNames.player].list[0]
        if self.check_group_collisions(Imp.groups[GroupNames.player]) is None:
            self._move_vec = (pygame.math.Vector2(player.position) - self._position).normalize()
            self.translate(self._move_vec)
        else:
            self.attack(player)
            self.translate((0, 0))

    def attack(self, target):
        if self._attack_time + self._attack_delay <= pygame.time.get_ticks():
            print("imp: attack")
            target.receive_damage(self._attack_damage)
            self._attack_time = pygame.time.get_ticks()
