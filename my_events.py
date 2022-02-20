import pygame


class MyEvents:
    game_over_event = pygame.USEREVENT + 0
    pause_event = pygame.USEREVENT + 1
    unpause_event = pygame.USEREVENT + 2
    restart_event = pygame.USEREVENT + 3

    @staticmethod
    def post_event(event):
        pygame.event.post(pygame.event.Event(event))

