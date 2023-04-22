# main.py
import pygame
import random
import time
import json

from tiled_level import TiledLevel
from game import Game

pygame.init()
pygame.font.init()
# You can replace None with a specific font file if you prefer.
font = pygame.font.Font(None, 36)

game = Game(width=1280, height=720)
game.load_screen()
game.screen.set_colorkey((0, 0, 0))  # define transparent


def render_fps(fps):
    fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
    game.screen.blit(
        fps_text, (game.screen.get_width() - fps_text.get_width(), 0))


level = TiledLevel("maps/level1.tmx")
clock = pygame.time.Clock()  # Add this line to create a Clock object
running = True
while running:
    delta_time = clock.tick(60) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        # Check for the KEYDOWN event and the ESC key
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

    # Clear the screen with a background color
    game.screen.fill((0, 0, 0))

    # Update map animations
    level.update(delta_time)

    # Call the map.render() function to draw the map
    level.render(game.screen)

    # Render the FPS on the screen
    render_fps(clock.get_fps())  # Use clock.get_fps() to get the current FPS

    pygame.display.update()

# Clean up and quit
pygame.quit()
