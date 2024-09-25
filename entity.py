import pygame


class Tile:
    def __init__(self, tile_data):
        self.current_frame = 0
        self.timer_next_frame = 0.0
        self.id = tile_data.get("id")
        self.width = tile_data.get("width")
        self.height = tile_data.get("height")
        self.position = tile_data.get("position", []).copy()
        self.sprites = tile_data.get("sprites")
        self.collidable_horizontal = tile_data.get("collidable_horizontal", False)
        self.collidable_vertical = tile_data.get("collidable_vertical", False)
        self.can_descend = tile_data.get("can_descend", False)

    def update(self, delta_time, frame_duration=0.1):
        self.timer_next_frame += delta_time
        if self.timer_next_frame >= frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
            self.timer_next_frame -= frame_duration  # Reseta o temporizador

    def render(self, screen, block_size):
        for pos in self.position:
            screen.blit(
                self.sprites[self.current_frame],
                (
                    pos[0] * block_size[0],
                    pos[1] * block_size[1],
                ),
            )

    def get_rect(self, block_size):
        # Retorna uma lista de pygame.Rect para cada posição
        rects = []
        for pos in self.position:
            rect = pygame.Rect(
                pos[0] * block_size[0], pos[1] * block_size[1], self.width, self.height
            )
            rects.append(rect)
        return rects


class Entity:
    def __init__(self, tile_data):
        self.tiles = []
        self.parse(tile_data)

    def parse(self, tile_data):
        for t in tile_data:
            tile = Tile(t)
            self.tiles.append(tile)

    def render(self, screen, block_size):
        for tile in self.tiles:
            tile.render(screen, block_size)

    def update(self, delta_time):
        for tile in self.tiles:
            tile.update(
                delta_time
            )  # Chama o update de Tile sem frame_duration específico

    def check_collision(self, rect1, rect2):
        return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
