import pygame


class UI:
    def __init__(self, player, screen):
        self._player = player
        self._screen = screen
        self._health_bar = Bar(screen=screen, top_left=(10, 10), bar_size=(200, 20), front_color=(255, 0, 0),
                               max_value_range=player.max_health)

    def update(self):
        self._health_bar.change_fill(self._player.health / self._player.max_health)

    def draw(self):
        self.update()
        self._health_bar.draw()


class Bar:
    def __init__(self, screen, top_left : tuple, bar_size: tuple, front_color=(0, 0, 0), back_color=(0, 0, 0),
                 border_width: int = 2, bar_fill: float = 1.0, show_text: bool = True, max_value_range: float = 100):
        if bar_fill > 1.0:
            bar_fill = 1.0
        elif bar_fill < 0.0:
            bar_fill = 0.0

        self._bar_fill = bar_fill
        self._bar_width = bar_size[0]
        self._show_text = show_text
        self._max_value_range = max_value_range
        self._font = pygame.font.Font('freesansbold.ttf', bar_size[1] - 2)
        self._screen = screen
        self._back_rect = pygame.Rect(*top_left, bar_size[0]+2*border_width, bar_size[1]+2*border_width)
        self._front_rect = pygame.Rect(top_left[0]+border_width, top_left[1]+border_width,
                                       bar_size[0]*bar_fill, bar_size[1]*bar_fill)
        self._front_color = front_color
        self._back_color = back_color

    @property
    def top_left(self):
        return self._back_rect.center

    @top_left.setter
    def top_left(self, position: tuple):
        self._back_rect.topleft = position
        self._front_rect.topleft = position

    @property
    def center(self):
        return self._back_rect.center

    @center.setter
    def center(self, position: tuple):
        self._back_rect.center = position
        self._front_rect.center = position

    def change_fill(self, bar_fill: float):
        if bar_fill > 1.0:
            bar_fill = 1.0
        elif bar_fill < 0.0:
            bar_fill = 0.0

        self._front_rect.width = self._bar_width * bar_fill
        self._bar_fill = bar_fill

    def draw(self):
        pygame.draw.rect(self._screen, self._back_color, self._back_rect)
        pygame.draw.rect(self._screen, self._front_color, self._front_rect)
        if self._show_text:
            text = self._font.render(f"{int(self._bar_fill * self._max_value_range)}/{self._max_value_range}", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = self._back_rect.center
            self._screen.blit(text, text_rect)

