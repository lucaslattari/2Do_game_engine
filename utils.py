# utils.py
import pygame
import configparser


def render_fps(fps, screen, font):
    fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
    screen.blit(fps_text, (screen.get_width() - fps_text.get_width() - 10, 10))


def read_config_file(ini_file):
    parser = configparser.ConfigParser()
    parser.read(ini_file)
    return parser
