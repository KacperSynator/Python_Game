import pygame
from stats_tracker import StatTracker
from enemies import EnemySpawner
from UI import Text


class WaveSystem:
    def __init__(self, screen, enemy_starting_count: int = 3, additional_enemies_per_wave: int = 1,
                 round_delay_ms: int = 5000):
        self._screen = screen
        self._enemy_spawner = EnemySpawner(screen)
        self._round = 0
        self._enemy_spawn_count = enemy_starting_count
        self._additional_enemies = additional_enemies_per_wave
        self._round_info = Text(screen=screen, font_size=16, center_position=(110, 100))
        self._next_round_text = Text(screen=screen, font_size=16, center_position=(110, 130))
        self._next_round = False
        self._round_end_time = 0
        self._round_delay_ms = round_delay_ms

    def next_round(self):
        if self._round_end_time + self._round_delay_ms < pygame.time.get_ticks():
            self._next_round = False
            self._round += 1
            self._enemy_spawner.spawn_enemies(self._enemy_spawn_count)
            self._enemy_spawn_count += self._additional_enemies

    def draw_info(self):
        self._round_info.draw(f"Round: {self._round}   Enemies left: {StatTracker.get_alive_enemies()}")
        if self._next_round:
            self._next_round_text.draw(f"Next round in {(self._round_end_time - pygame.time.get_ticks() + self._round_delay_ms)/1000:.1f}s")

    def update(self):
        self.draw_info()
        if self._next_round:
            self.next_round()
        elif StatTracker.get_alive_enemies() <= 0:
            self._round_end_time = pygame.time.get_ticks()
            self._next_round = True


