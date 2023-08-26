# main.py
import pygame
import random
import time
import logging

from game import Game
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

game = Game(width=1280, height=720, config_parser=config_parser)
game.load_screen()
game.screen.set_colorkey((0, 0, 0))  # define transparent

game.load_level("maps/level1.tmx")
logger.info("Nível carregado")

clock = pygame.time.Clock()
running = True

while running:
    delta_time = clock.tick(60) / 1000  # tempo decorrido desde o último frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for the KEYDOWN event and the ESC key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    game.update(delta_time)

    # Clear the screen with a background color
    game.screen.fill((0, 0, 0))

    # Renderiza o nível e os personagens
    game.render(game.screen)

    # Render the FPS on the screen
    render_fps(clock.get_fps(), game.screen)

    pygame.display.update()

# Clean up and quit
pygame.quit()
