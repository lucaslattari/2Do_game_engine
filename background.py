import pygame
import os


class Background:
    def __init__(self, tiled_level, config_parser):
        # Carrega a imagem de fundo usando o caminho do arquivo de configuração
        image_path = config_parser["background"]["image"]

        # Ajusta o caminho da imagem para ser relativo ao diretório principal do script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_image_path = os.path.join(base_dir, image_path)

        # Verifica se a imagem existe
        if not os.path.exists(bg_image_path):
            raise FileNotFoundError(f"Imagem de fundo não encontrada: {bg_image_path}")

        # Carrega a imagem de fundo
        self.tile_bg = pygame.image.load(bg_image_path).convert()

        # Carrega a velocidade de deslocamento do arquivo de configuração
        self.scroll_speed = float(config_parser["background"].get("scroll_speed", 0.3))

        # Analisa os limites de bloco do arquivo de configuração
        x_block_bounds = config_parser["background"]["x_block_bounds"]
        y_block_bounds = config_parser["background"]["y_block_bounds"]
        self.y_offset = 0

        # Remove espaços em branco e divide os limites
        self.x_block_bounds = tuple(
            map(int, x_block_bounds.replace(" ", "").split(","))
        )
        self.y_block_bounds = tuple(
            map(int, y_block_bounds.replace(" ", "").split(","))
        )

        self.create_scrolling_bg(tiled_level.tilewidth, tiled_level.tileheight)

    def create_scrolling_bg(self, level_block_size_x, level_block_size_y):
        # Calcula a largura e altura da imagem de fundo
        bg_width = (
            self.x_block_bounds[1] - self.x_block_bounds[0]
        ) * self.tile_bg.get_width()
        bg_height = (
            self.y_block_bounds[1] - self.y_block_bounds[0]
        ) * self.tile_bg.get_height()

        self.background_image = pygame.Surface((bg_width, bg_height)).convert()

        # Preenche a imagem de fundo com tiles
        for x in range(0, bg_width, self.tile_bg.get_width()):
            for y in range(0, bg_height, self.tile_bg.get_height()):
                self.background_image.blit(self.tile_bg, (x, y))

    def update(self, delta_time):
        # Usa delta_time para ajustar a velocidade de deslocamento
        self.y_offset += (
            self.scroll_speed * delta_time * 60
        )  # Multiplica por 60 para manter a velocidade original
        if self.y_offset > self.background_image.get_height():
            self.y_offset = 0

    def render(self, screen, block_size):
        # Blita a imagem de fundo na posição atual
        screen.blit(self.background_image, (0, -self.y_offset))
