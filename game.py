import pygame
import player
import projectile
import moving_object
import imp


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
        # Player
        self._player = player.Player(screen=self._screen, position=(300, 300))
        # Enemy
        imp.Imp(screen=self._screen, position=(500, 600))
        # Clock
        self._clock = pygame.time.Clock()

    def start(self):
        # Game loop
        running = True
        while running:
            self._clock.tick(60)
            self._screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # mouse input
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                    projectile.Projectile(screen=self._screen, position=self._player.position, move_vec=pygame.mouse.get_pos())
                # keyboard input
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_a, pygame.K_LEFT]:
                        print("left")
                        self._player.move_vec = (-1, self._player.move_vec[1])
                    if event.key in [pygame.K_d, pygame.K_RIGHT]:
                        print("right")
                        self._player.move_vec = (1, self._player.move_vec[1])
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        print("up")
                        self._player.move_vec = (self._player.move_vec[0], -1)
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        print("down")
                        self._player.move_vec = (self._player.move_vec[0], 1)
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT]:
                        self._player.move_vec = (0, self._player.move_vec[1])
                    if event.key in [pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN]:
                        self._player.move_vec = (self._player.move_vec[0], 0)

            moving_object.MovingObject.move_all()
            pygame.display.update()

