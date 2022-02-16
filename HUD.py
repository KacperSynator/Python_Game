import pygame
from UI import Bar, Text
from object import GroupNames


class HUD:
    def __init__(self, player, screen, skill, move_skill):
        self._player = player
        self._screen = screen
        self._skill = SkillDisplay(screen=screen, skill=skill, top_left_position=(10, 40))
        self._move_skill = SkillDisplay(screen=screen, skill=move_skill, top_left_position=(60, 40))
        self._health_bar = Bar(screen=screen, top_left=(10, 10), bar_size=(200, 20), front_color=(255, 0, 0),
                               max_value_range=player.max_health)
        self._pick_item_text = Text(screen, 32, (screen.get_width()/2, 100))

    def update(self):
        self._health_bar.change_fill(self._player.health / self._player.max_health)

    def draw(self):
        self.update()
        self._health_bar.draw()
        self._skill.draw()
        self._move_skill.draw()
        objs = self._player.check_group_collisions(self._player.groups[GroupNames.item])
        if objs and len(objs) > 1:
            objs.remove(self._player.weapon)
            self._pick_item_text.draw(f"Press E to pick {objs[0].name}")


class SkillDisplay:
    def __init__(self, screen, skill, top_left_position: tuple):
        self._screen = screen
        self._skill = skill
        self._top_left = pygame.Vector2(top_left_position)
        self._cooldown_text = Text(screen, int(skill.icon.get_height() * 0.7), center_position=self.center)

    @property
    def center(self) -> tuple:
        return tuple(self._top_left + pygame.Vector2(self._skill.icon.get_size())/2)

    def draw(self):
        self._screen.blit(self._skill.icon, self._top_left)
        cooldown_time_s = self._skill.remaining_cooldown / 1000
        if cooldown_time_s > 0.0:
            self._cooldown_text.draw(f"{cooldown_time_s:.1f}")

