# main.py
import pygame
import random
import time
import logging

from game import Game
from input_handler import InputHandler
from utils import *

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
)

pygame.init()
pygame.font.init()

config_parser = read_config_file("config.ini")

game = Game(config_parser=config_parser)
game.load_screen()
game.screen.set_colorkey((0, 0, 0))  # define transparent

game.load_level("maps/level1.tmx")
logger.info("Nível carregado")

input_handler = InputHandler()

clock = pygame.time.Clock()
running = True

while running:
    delta_time = clock.tick(60) / 1000  # tempo decorrido desde o último frame

    input_handler.update()

    if input_handler.fullscreen_toggled:
        # Alternar entre tela cheia e modo janela
        game.toggle_fullscreen()
        game.load_screen()

        # Resetar o estado de toggle após lidar com ele
        input_handler.reset_toggle_fullscreen()

    game.update(delta_time, input_handler)

    # Clear the screen with a background color
    game.screen.fill((0, 0, 0))

    # Renderiza o nível e os personagens
    game.render(game.screen)

    # Render the FPS on the screen
    render_fps(clock.get_fps(), game.screen)

    pygame.display.update()

# Clean up and quit
pygame.quit()
