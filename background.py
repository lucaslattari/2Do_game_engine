import pygame


class Background:
    def __init__(self, tiled_level, config_parser):
        self.tile_bg = pygame.image.load(config_parser["background"]["image"])
        x_block_bounds = config_parser["background"]["x_block_bounds"]
        y_block_bounds = config_parser["background"]["y_block_bounds"]
        self.y_offset = 0

        self.x_block_bounds = tuple(map(int, x_block_bounds.split(", ")))
        self.y_block_bounds = tuple(map(int, y_block_bounds.split(", ")))

        self.create_scrolling_bg(tiled_level.tilewidth, tiled_level.tileheight)

    def create_scrolling_bg(self, level_block_size_x, level_block_size_y):
        self.background_image = pygame.Surface(
            (
                (self.x_block_bounds[1] - self.x_block_bounds[0])
                * self.tile_bg.get_width(),
                (self.y_block_bounds[1] - self.y_block_bounds[0])
                * self.tile_bg.get_height(),
            )
        )
        for x in range(
            self.x_block_bounds[0] * level_block_size_x,
            self.x_block_bounds[1] * level_block_size_x,
            self.tile_bg.get_width(),
        ):
            for y in range(
                self.y_block_bounds[0] * level_block_size_y,
                self.y_block_bounds[1] * level_block_size_y,
                self.tile_bg.get_height(),
            ):
                self.background_image.blit(
                    self.tile_bg,
                    (x, y),
                )

    def update(self, delta_time):
        self.y_offset += 0.3
        if self.y_offset > self.tile_bg.get_height():
            self.y_offset = 0

    def render(self, screen, block_size):
        screen.blit(self.background_image, (0, self.y_offset))
