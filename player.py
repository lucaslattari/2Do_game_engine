import pygame

from entity import Entity

ANIMATION_TYPES = ["run", "idle", "jump"]
SPRITE_BLOCK_SIZE = 16


class Player(Entity):
    def __init__(self, data):
        super().__init__(data)

        # Inicializa a lista de tiles do jogador
        self.tiles = []
        self.parse(data)  # Parse dos dados iniciais

        self.state = "idle"
        self.face_direction = "right"
        self.x = self.tiles[0]["position"][0][0]  # posição inicial
        self.y = self.tiles[0]["position"][0][1]

        self.width = self.tiles[0]["width"]
        self.height = self.tiles[0]["height"]

        self.velocity = 0.0
        self.max_velocity = 12.0
        self.acceleration = 1.0
        self.deceleration = 8.0

        self.vertical_velocity = 0.0
        self.jump_acceleration = -24.0
        self.gravity = 35
        self.on_ground = True

        self.jump_time_max = 0.2
        self.jump_time_current = 0

        self.descend_time_max = 0.12
        self.descend_time_current = 0

    def parse(self, tile_data):
        for _t in tile_data:
            animation_name = _t["type"].split("_")[1].lower()
            tile = {
                "animation_name": animation_name,  # Nome da animação (ex: "run", "idle", "jump")
                "current_frame": 0,  # Quadro atual da animação
                "timer_next_frame": 0.0,  # Temporizador para controlar a mudança de quadros da animação
                "id": _t.get("id"),  # ID do tile (se disponível nos dados originais)
                "width": _t.get("width"),  # Largura do tile
                "height": _t.get("height"),  # Altura do tile
                "position": _t.get(
                    "position", []
                ).copy(),  # Posições do tile (cópia da lista de posições para evitar modificar os dados originais)
                "sprites": _t.get("sprites"),
                "can_descend": _t.get("can_descend", False),  # Novo atributo
            }
            self.tiles.append(tile)

    def render(self, screen, block_size):
        for tile in self.tiles:
            if self.state == tile["animation_name"]:
                sprite_to_draw = tile["sprites"][tile["current_frame"]]

                if self.face_direction == "left":
                    sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)

                screen.blit(
                    sprite_to_draw,
                    (self.x * block_size[0], self.y * block_size[1]),
                )

    def update(self, delta_time, input_handler, tiles):
        self.update_state_and_velocity(input_handler, delta_time, tiles)
        self.update_position(delta_time, tiles)
        self.update_animation_frames(delta_time)

    def update_state_and_velocity(self, input_handler, delta_time, tiles):
        # Estado atual do personagem
        state = self.state

        # Atualiza a lógica de descida
        if (
            input_handler.is_pressed("down")
            and self.on_ground
            and (state == "idle" or state == "run")
        ):
            for tile in tiles:
                if "can_descend" in tile and tile["can_descend"]:
                    for position in tile["position"]:
                        tile_rect = (
                            position[0] * SPRITE_BLOCK_SIZE,
                            position[1] * SPRITE_BLOCK_SIZE,
                            tile["width"],
                            tile["height"],
                        )
                        player_rect = (
                            self.x * SPRITE_BLOCK_SIZE,
                            self.y * SPRITE_BLOCK_SIZE
                            + 0.2,  # Checar logo abaixo do jogador
                            self.width,
                            self.height,
                        )
                        if self.check_collision(player_rect, tile_rect):
                            self.state = "descend"
                            self.on_ground = False
                            self.vertical_velocity = self.gravity * delta_time
                            self.descend_time_current = (
                                0  # Reiniciar o temporizador de descida
                            )
                            return

        # Lógica de movimento horizontal
        if input_handler.is_pressed("left"):
            self.face_direction = "left"
            if self.on_ground:
                self.state = "run"
            self.velocity = max(-self.max_velocity, self.velocity - self.acceleration)
        elif input_handler.is_pressed("right"):
            self.face_direction = "right"
            if self.on_ground:
                self.state = "run"
            self.velocity = min(self.max_velocity, self.velocity + self.acceleration)
        else:
            if self.on_ground and (state == "run" or state == "idle"):
                self.state = "idle"
                self.apply_deceleration()

        # Lógica de salto
        if state != "jump" and input_handler.is_pressed("up") and self.on_ground:
            self.state = "jump"
            self.on_ground = False
            self.vertical_velocity = self.jump_acceleration
            self.jump_time_current = 0

        # Lógica de queda
        if state == "jump":
            if input_handler.is_pressed("up"):
                self.jump_time_current += delta_time
                if self.jump_time_current >= self.jump_time_max:
                    self.state = "fall"
            else:
                self.state = "fall"

        if not self.on_ground and state != "jump" and state != "descend":
            self.state = "fall"

        # Verificação de colisão vertical para retornar ao estado 'idle' quando no chão
        if self.on_ground and (self.state == "fall" or self.state == "descend"):
            self.state = "idle"

    def handle_vertical_collision(self, current_x, new_y, tiles, delta_time):
        player_rect = (
            current_x * SPRITE_BLOCK_SIZE,
            new_y * SPRITE_BLOCK_SIZE,
            self.width,
            self.height,
        )
        for tile in tiles:
            if "collidable_vertical" in tile and tile["collidable_vertical"]:
                for position in tile["position"]:
                    tile_rect = (
                        position[0] * SPRITE_BLOCK_SIZE,
                        position[1] * SPRITE_BLOCK_SIZE,
                        tile["width"],
                        tile["height"],
                    )
                    if self.check_collision(player_rect, tile_rect):
                        player_top = round(self.y) * SPRITE_BLOCK_SIZE
                        player_bottom = (
                            round(self.y) * SPRITE_BLOCK_SIZE + SPRITE_BLOCK_SIZE * 2
                        )

                        tile_top = tile_rect[1]
                        tile_bottom = tile_rect[1] + tile_rect[3]

                        # Colidindo "por cima"
                        if self.vertical_velocity > 0 and self.state != "descend":
                            # Plataforma está abaixo do pé do personagem?
                            if player_bottom <= tile_top:
                                self.on_ground = True
                                self.vertical_velocity = 0
                                return round(self.y)
                        # Colidindo "por baixo"
                        elif self.vertical_velocity < 0:
                            pass

        if not self.on_ground:
            self.vertical_velocity += self.gravity * delta_time

        return new_y  # Caso contrário, retorna a nova posição y

    def apply_deceleration(self):
        if self.velocity > 0:
            self.velocity = max(0, self.velocity - self.deceleration)
        elif self.velocity < 0:
            self.velocity = min(0, self.velocity + self.deceleration)

    def update_position(self, delta_time, tiles):
        new_x, new_y = self.calculate_new_positions(delta_time)
        new_x = self.handle_horizontal_collision(new_x, self.y, tiles)  # Correção aqui

        # Atualiza a posição Y e a velocidade vertical
        if self.state == "jump":
            if self.jump_time_current < self.jump_time_max:
                additional_jump_force = (
                    -2
                    * (self.jump_time_max - self.jump_time_current)
                    / self.jump_time_max
                )
                self.vertical_velocity += (
                    additional_jump_force * self.gravity * delta_time
                )
        else:
            self.vertical_velocity += self.gravity * delta_time

        new_y = self.y + self.vertical_velocity * delta_time

        # Adiciona o temporizador de descida
        if self.state == "descend":
            self.descend_time_current += delta_time
            if self.descend_time_current >= self.descend_time_max:
                self.state = "fall"

        new_y = self.handle_vertical_collision(new_x, new_y, tiles, delta_time)

        self.x = new_x
        self.y = new_y

    def calculate_new_positions(self, delta_time):
        new_x = self.x + self.velocity * delta_time
        new_y = self.y + self.vertical_velocity * delta_time
        return new_x, new_y

    def handle_horizontal_collision(self, new_x, current_y, tiles):
        player_rect = (
            new_x * SPRITE_BLOCK_SIZE,
            current_y * SPRITE_BLOCK_SIZE,
            self.width,
            self.height,
        )
        for tile in tiles:
            if "collidable_horizontal" in tile and tile["collidable_horizontal"]:
                for position in tile["position"]:
                    tile_rect = (
                        position[0] * SPRITE_BLOCK_SIZE,
                        position[1] * SPRITE_BLOCK_SIZE,
                        tile["width"],
                        tile["height"],
                    )
                    if self.check_collision(player_rect, tile_rect):
                        return self.x  # Reset x position if collision detected
        return new_x  # Otherwise, return new x position

    def update_animation_frames(self, delta_time):
        for tile in self.tiles:
            if tile["timer_next_frame"] > delta_time:
                tile["current_frame"] = (tile["current_frame"] + 1) % len(
                    tile["sprites"]
                )
                tile["timer_next_frame"] -= delta_time
            else:
                tile["timer_next_frame"] += delta_time

    def check_collision(self, rect1, rect2):
        return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
