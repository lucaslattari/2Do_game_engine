import pygame, pytmx, configparser

# assets
from asset_manager import AssetManager
from player import Player
from item import Item
from terrain import Terrain
from platformer import Platform

from background import Background


class Game:
    def __init__(self, config_parser, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = None
        self.background = None
        self.config_parser = config_parser

    def load_screen(self, resizable=True):
        flags = pygame.RESIZABLE if resizable else 0
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        return self.screen

    def load_level(self, level_filename):
        self.tiled_level = pytmx.load_pygame(level_filename)
        self.load_assets()

        self.background = Background(self.tiled_level, self.config_parser)

    def load_assets(self):
        self.asset_manager = AssetManager(self.tiled_level)

        self.player = Player(self.asset_manager.get_asset("Player"))
        self.item = Item(self.asset_manager.get_asset("Item"))
        self.platform = Platform(self.asset_manager.get_asset("Platform"))
        self.terrain = Terrain(self.asset_manager.get_asset("Terrain"))

    def get_block_size(self):
        return self.tiled_level.tilewidth, self.tiled_level.tileheight

    def update(self, delta_time):
        if self.background:
            self.background.update(delta_time)

        if self.terrain:
            self.terrain.update(delta_time)

        if self.item:
            self.item.update(delta_time)

        if self.platform:
            self.platform.update(delta_time)

        if self.player:
            self.player.update(delta_time)

    def render(self, screen):
        block_size = self.get_block_size()

        if self.background:
            self.background.render(screen, block_size)

        if self.terrain:
            self.terrain.render(screen, block_size)

        if self.item:
            self.item.render(screen, block_size)

        if self.platform:
            self.platform.render(screen, block_size)

        if self.player:
            self.player.render(screen, block_size)
