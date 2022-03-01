import pygame
from player import Player
from moving_object import MovingObject
from object import Object
from weapons import RangeWeapon
from enemies import Enemy
from my_events import MyEvents
from wave_system import WaveSystem


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Create the screen
        self._screen_size = (1280, 720)
        self._screen = pygame.display.set_mode(self._screen_size)
        # Title & icon
        pygame.display.set_caption("Game")
        icon = pygame.image.load("assets/items/weapons/staff.png")
        pygame.display.set_icon(icon)
        # Enemies
        self._waves = WaveSystem(screen=self._screen)
        # Player
        self._player = Player(screen=self._screen, position=(300, 300))
        RangeWeapon(screen=self._screen, **RangeWeapon.weapon_list["crystal_wand"], position=(600, 200))
        # Clock
        self._clock = pygame.time.Clock()

    @staticmethod
    def start():
        Game().game_loop()

    def restart(self):
        Object.groups = {}
        Object.count = 0
        Enemy.damage_received = 0
        Enemy.count = 0
        Enemy.alive = 0
        Game.start()

    def game_loop(self):
        # Game loop
        running = True
        paused = False
        while running:
            self._clock.tick(60)
            self._screen.fill((255, 255, 255))

            self._waves.update()

            for event in pygame.event.get():
                if event.type == MyEvents.game_over_event:
                    paused = True
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_p, pygame.K_ESCAPE]:
                        if paused:
                            paused = False
                            MyEvents.post_event(MyEvents.unpause_event)
                        else:
                            paused = True
                            MyEvents.post_event(MyEvents.pause_event)
                if event.type == MyEvents.unpause_event:
                    paused = False
                if event.type == MyEvents.restart_event:
                    self.restart()
                    return

                if not paused:
                    # mouse input
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pressed_buttons = pygame.mouse.get_pressed()
                        if pressed_buttons[0]:
                            self._player.auto_attack(pygame.mouse.get_pos())
                    # keyboard input
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_a, pygame.K_LEFT]:
                            self._player.move_vec = (-1, self._player.move_vec[1])
                        if event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self._player.move_vec = (1, self._player.move_vec[1])
                        if event.key in [pygame.K_w, pygame.K_UP]:
                            self._player.move_vec = (self._player.move_vec[0], -1)
                        if event.key in [pygame.K_s, pygame.K_DOWN]:
                            self._player.move_vec = (self._player.move_vec[0], 1)
                        if event.key == pygame.K_e:
                            self._player.pick_item()
                        if event.key == pygame.K_r:
                            self._player.skill(pygame.mouse.get_pos())
                        if event.key == pygame.K_SPACE:
                            self._player.move_skill(pygame.mouse.get_pos())
                    if event.type == pygame.KEYUP:
                        if event.key in [pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT]:
                            self._player.move_vec = (0, self._player.move_vec[1])
                        if event.key in [pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN]:
                            self._player.move_vec = (self._player.move_vec[0], 0)

            if not paused:
                MovingObject.move_all()
            Object.draw_all()
            pygame.display.update()

