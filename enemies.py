import pygame
from mob import Mob
from object import Group, GroupNames
from UI import Bar
from projectiles import Projectile
from abc import ABC, abstractmethod
import functools
import random
from weapons import RangeWeapon


class EnemySpawner:
    enemies_names_list = ["Imp", "FireElemental", "Cthulhu"]
    def __init__(self, screen):
        self._screen = screen
        self._max_spawn_coordinate = screen.get_size()

    def spawn_enemy_at(self, position: tuple):
        eval(f"{random.choice(EnemySpawner.enemies_names_list)}(screen=self._screen, position={position})")

    def spawn_enemy(self):
        max_fixed_value = {"x_0": 0, "x_max": self._max_spawn_coordinate[0], "y_0": 0, "y_max": self._max_spawn_coordinate[1]}
        fixed = random.choice(list(max_fixed_value.keys()))
        position = None
        if fixed in ("x_0", "x_max"):
            position = (max_fixed_value[fixed], random.randrange(0, self._max_spawn_coordinate[1]))
        if fixed in ("y_0", "y_max"):
            position = (random.randrange(0, self._max_spawn_coordinate[0]), max_fixed_value[fixed])
        self.spawn_enemy_at(position=position)

    def spawn_enemies(self, count: int):
        for i in range(0, count):
            self.spawn_enemy()


class Enemy(Mob, ABC):
    count = 0
    alive = 0

    def _check_delay(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            if self._attack_time + self._attack_delay <= pygame.time.get_ticks():
                self._attack_time = pygame.time.get_ticks()
                return fn(self, *args, **kwargs)

        return wrapper

    def __init__(self, attack_damage=0, attack_delay_ms=1000, **kwargs):
        Mob.__init__(self, **kwargs)
        self._attack_damage = attack_damage
        self._attack_delay = attack_delay_ms
        self._attack_time = -attack_delay_ms
        self._bar_center_offset = pygame.Vector2(0, -self._image_size[1] // 2 - 5)
        self._health_bar = Bar(screen=self._screen, bar_size=(self._image_size[0] * 0.8, 5), front_color=(255, 0, 0),
                               top_left=self._position + self._bar_center_offset, border_width=1, show_text=False)
        Enemy.count += 1
        Enemy.alive += 1
        if GroupNames.enemy not in Enemy.groups.keys():
            Enemy.groups[GroupNames.enemy] = Group(GroupNames.enemy)
        Enemy.groups[GroupNames.enemy].add(self)

    def die(self):
        Enemy.groups[GroupNames.enemy].remove(self)
        Enemy.alive -= 1
        Mob.die(self)

    def draw(self) -> None:
        Mob.draw(self)
        self._health_bar.center = self._position + self._bar_center_offset
        self._health_bar.change_fill(self._health / self._max_health)
        self._health_bar.draw()

    @_check_delay
    @abstractmethod
    def attack(self, target):
        pass

    _check_delay = staticmethod(_check_delay)


class Imp(Enemy):
    def __init__(self, **kwargs):
        super().__init__(image_path="assets/mobs/enemies/imp.png", health=40, move_speed=1.4, attack_damage=10,
                         attack_delay_ms=1000, **kwargs)

    def move(self):
        player = Imp.groups[GroupNames.player].list[0]
        if not self._collisions or player not in self._collisions:
            self.move_vec = (pygame.math.Vector2(player.position) - self._position).normalize()
            self.translate(tuple(self._move_vec))
        else:
            self.attack(player)
            self.translate((0, 0))

    @Enemy._check_delay
    def attack(self, target):
        print("imp: attack")
        target.receive_damage(self._attack_damage)
        self._attack_time = pygame.time.get_ticks()


class FireElemental(Imp):
    def __init__(self, **kwargs):
        super(Imp, self).__init__(image_path="assets/mobs/enemies/fire_elemental_48px.png", health=20, move_speed=2,
                                  attack_damage=5, attack_delay_ms=1000, **kwargs)


class Cthulhu(Enemy):
    def __init__(self, **kwargs):
        super().__init__(image_path="assets/mobs/enemies/cthulhu.png", move_speed=1, health=50, attack_damage=10,
                         attack_delay_ms=4000, **kwargs)
        self._end_position = self._position

    def move(self):
        player = Cthulhu.groups[GroupNames.player].list[0]
        if (self._position - self._end_position).length() < 5:

            self._end_position = pygame.Vector2(player.position) + (self._position - pygame.Vector2(player.position)).rotate(90)/2
        self.translate(self._end_position-self._position, normalize=True)
        self.attack(player)

    @Enemy._check_delay
    def attack(self, target):
        print("cthulhu: attack")
        Projectile(screen=self._screen, end_position=target.position, damage=self._attack_damage, position=self.position,
                   target_player_enemies=(True, False), image_path="assets/projectiles/slime.png", max_range=600, move_speed=5)


