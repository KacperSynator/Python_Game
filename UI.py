import pygame


class Text:
    def __init__(self, screen, font_size: int, center_position: tuple, text: str = "", font: str = 'freesansbold.ttf',
                 color: tuple = (0, 0, 0),):
        self._font = pygame.font.Font(font, font_size)
        self._screen = screen
        self._color = color
        self._text = text
        self._center = center_position

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text: str):
        self._text = new_text

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, new_center: tuple):
        self._center = new_center

    def draw(self, _text: str = None):
        if _text is not None:
            self._text = _text
        text = self._font.render(self._text, True, self._color)
        text_rect = text.get_rect()
        text_rect.center = self._center
        self._screen.blit(text, text_rect)


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
        self._screen = screen
        self._back_rect = pygame.Rect(*top_left, bar_size[0]+2*border_width, bar_size[1]+2*border_width)
        self._front_rect = pygame.Rect(top_left[0]+border_width, top_left[1]+border_width,
                                       bar_size[0]*bar_fill, bar_size[1]*bar_fill)
        self._front_color = front_color
        self._back_color = back_color
        self._text = Text(screen, bar_size[1] - 2, center_position=self._back_rect.center, color=(255, 255, 255))

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
            self._text.center = self._back_rect.center
            self._text.draw(f"{int(self._bar_fill*self._max_value_range)}/{self._max_value_range}")