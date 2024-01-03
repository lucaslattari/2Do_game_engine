import pygame, pytmx, configparser

# assets
from asset_manager import AssetManager
from player import Player
from item import Item
from platformer import Platform
from background import Background


class Game:
    def __init__(self, config_parser, width=800, height=600):
        self.config_parser = config_parser

        resolution_str = self.config_parser.get(
            "graphics", "resolution", fallback="1280x720"
        )
        self.width, self.height = map(int, resolution_str.split("x"))

        # Ler o modo de tela cheia
        fullscreen_str = self.config_parser.get("graphics", "fullscreen", fallback="no")
        self.is_fullscreen = fullscreen_str.lower() == "yes"

        self.screen = None
        self.background = None

    def load_screen(self):
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.FULLSCREEN
            )
        else:
            flags = pygame.RESIZABLE
            self.screen = pygame.display.set_mode((self.width, self.height), flags)
        return self.screen

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen

    def load_level(self, level_filename):
        self.tiled_level = pytmx.load_pygame(level_filename)
        self.load_assets()

        self.background = Background(self.tiled_level, self.config_parser)

    def load_assets(self):
        self.asset_manager = AssetManager(self.tiled_level)

        self.player = Player(self.asset_manager.get_asset("Player"))
        self.item = Item(self.asset_manager.get_asset("Item"))
        self.platform = Platform(self.asset_manager.get_asset("Platform"))

    def get_block_size(self):
        return self.tiled_level.tilewidth, self.tiled_level.tileheight

    def update(self, delta_time, input_handler):
        if self.background:
            self.background.update(delta_time)

        if self.item:
            self.item.update(delta_time)

        if self.platform:
            self.platform.update(delta_time)

        if self.player:
            self.player.update(delta_time, input_handler, self.platform.tiles)

    def render(self, screen):
        block_size = self.get_block_size()

        if self.background:
            self.background.render(screen, block_size)

        if self.item:
            self.item.render(screen, block_size)

        if self.platform:
            self.platform.render(screen, block_size)

        if self.player:
            self.player.render(screen, block_size)
