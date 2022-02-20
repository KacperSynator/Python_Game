import pygame
from UI import Bar, Text, Button
from object import GroupNames
from  my_events import MyEvents


class HUD:
    def __init__(self, player, screen, skill, move_skill):
        self._player = player
        self._screen = screen
        self._skill = SkillDisplay(screen=screen, skill=skill, top_left_position=(10, 40))
        self._move_skill = SkillDisplay(screen=screen, skill=move_skill, top_left_position=(60, 40))
        self._health_bar = Bar(screen=screen, top_left=(10, 10), bar_size=(200, 20), front_color=(255, 0, 0),
                               max_value_range=player.max_health, text_color=(255, 255, 255))
        self._pick_item_text = Text(screen=screen, font_size=32, center_position=(screen.get_width()/2, screen.get_height()/6))
        self._pause_window = PauseWindow(screen=screen, size=(screen.get_width()/3, int(screen.get_height()*0.7)),
                                         top_left=(screen.get_width()/3, int(screen.get_height()*0.15)), color=(255, 255, 255))

    def update(self):
        self._health_bar.change_fill(self._player.health / self._player.max_health)
        if pygame.event.peek(MyEvents.pause_event):
            self._pause_window.show()
        if pygame.event.peek(MyEvents.unpause_event):
            self._pause_window.hide()

    def draw(self):
        self.update()
        self._health_bar.draw()
        self._skill.draw()
        self._move_skill.draw()
        self._pause_window.draw()
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


class PauseWindow:
    def __init__(self, screen, size: tuple, top_left: tuple, hide: bool = True, color: tuple = (0, 0, 0)):
        self._screen = screen
        self._size = size
        self._top_left = top_left
        self._color = color
        self._hide = hide
        self._rect = pygame.Rect(*top_left, *size)

        button_size = (int(size[0] * 5/7), int(size[1] * 2/13))
        button_position = [int(top_left[0] + size[0] * 1/7), int(top_left[1] + size[1] * 1/13)]
        text_position = tuple(pygame.Vector2(button_position) + pygame.Vector2(button_size)/2)
        self._info_text = Text(screen=screen, center_position=text_position, text="Game Paused", font_size=int(button_size[1] * 0.7))
        button_position[1] = int(button_position[1] + button_size[1] + size[1] * 1 / 13)
        self._resume_button = Button(screen=screen, top_left=button_position, bar_size=button_size, text="RESUME",
                                     front_color=(0, 0, 255), hover_text_color=(255, 255, 255), text_color=(170, 170, 170),
                                     font_size=(int(button_size[1]/2)))
        button_position[1] = int(button_position[1] + button_size[1] + size[1] * 1/13)
        self._restart_button = Button(screen=screen, top_left=button_position, bar_size=button_size, text="RESTART",
                                      front_color=(0, 0, 255), hover_text_color=(255, 255, 255), text_color=(170, 170, 170),
                                      font_size=(int(button_size[1]/2)))
        button_position[1] = int(button_position[1] + button_size[1] + size[1] * 1/13)
        self._quit_button = Button(screen=screen, top_left=button_position, bar_size=button_size, text="QUIT",
                                   front_color=(0, 0, 255), hover_text_color=(255, 255, 255), text_color=(170, 170, 170),
                                   font_size=(int(button_size[1] / 2)))

    def show(self):
        self._hide = False

    def hide(self):
        self._hide = True

    def _check_buttons_pressed(self):
        if self._resume_button.is_pressed:
            MyEvents.post_event(MyEvents.unpause_event)
            self.hide()
        if self._restart_button.is_pressed:
            MyEvents.post_event(MyEvents.restart_event)
        if self._quit_button.is_pressed:
            MyEvents.post_event(pygame.QUIT)

    def draw(self):
        if not self._hide:
            pygame.draw.rect(self._screen, self._color, self._rect)
            self._info_text.draw()
            self._resume_button.draw()
            self._restart_button.draw()
            self._quit_button.draw()
            self._check_buttons_pressed()


