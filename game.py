from utils import load_config

import pygame
import json


class Game:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = None

    def load_screen(self, resizable=True):
        flags = pygame.RESIZABLE if resizable else 0
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        return self.screen
