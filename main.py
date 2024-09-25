# main.py
import pygame
import logging

from game import Game
from input_handler import InputHandler
from utils import render_fps, read_config_file

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
game.screen.set_colorkey((0, 0, 0))  # define transparente

game.load_level("maps/level1.tmx")
logger.info("Nível carregado")

input_handler = InputHandler(config_parser)

clock = pygame.time.Clock()
running = True

# Carrega a fonte uma vez para uso no render_fps
font = pygame.font.Font(None, 30)

while running:
    delta_time = clock.tick(60) / 1000.0  # tempo em segundos desde o último frame

    input_handler.process_events()

    if input_handler.quit_game:
        running = False

    game.update(delta_time, input_handler)

    # Clear the screen with a background color
    game.screen.fill((0, 0, 0))

    # Renderiza o nível e os personagens
    game.render(game.screen)

    # Render the FPS on the screen
    render_fps(clock.get_fps(), game.screen, font)

    pygame.display.update()

# Clean up and quit
pygame.quit()
