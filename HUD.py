import pygame
from UI import Bar
from UI import Text
from object import GroupNames
from object import Group


class HUD:
    def __init__(self, player, screen):
        self._player = player
        self._screen = screen
        self._health_bar = Bar(screen=screen, top_left=(10, 10), bar_size=(200, 20), front_color=(255, 0, 0),
                               max_value_range=player.max_health)
        self._pick_item_text = Text(screen, 32, (screen.get_width()/2, 100))

    def update(self):
        self._health_bar.change_fill(self._player.health / self._player.max_health)

    def draw(self):
        self.update()
        self._health_bar.draw()
        objs = self._player.check_group_collisions(self._player.groups[GroupNames.item])
        if objs and len(objs) > 1:
            objs.remove(self._player.weapon)
            self._pick_item_text.draw(f"Press E to pick {objs[0].name}")
