import pygame

from entity import Entity

ANIMATION_TYPES = ["run", "idle", "jump"]
SPRITE_BLOCK_SIZE = 16


class Player(Entity):
    def __init__(self, data):
        super().__init__(data)

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
        self.jump_acceleration = -12.0
        self.gravity = 35
        self.on_ground = True

        self.jump_time_max = 0.2
        self.jump_time_current = 0

    def parse(self, tile_data):
        for _t in tile_data:
            animation_name = _t["type"].split("_")[1].lower()
            tile = {
                "animation_name": animation_name,
                "current_frame": 0,
                "timer_next_frame": 0.0,
                "id": _t.get("id"),
                "width": _t.get("width"),
                "height": _t.get("height"),
                "position": _t.get("position", []).copy(),
                "sprites": _t.get("sprites"),
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
        self.update_state_and_velocity(input_handler, delta_time)
        self.update_position(delta_time, tiles)
        self.update_animation_frames(delta_time)

    def update_state_and_velocity(self, input_handler, delta_time):
        # Lógica de Salto
        if self.state != "jump":
            if input_handler.is_pressed("up") and self.on_ground:
                self.state = "jump"
                self.on_ground = False
                self.vertical_velocity = self.jump_acceleration
                self.jump_time_current = 0

        if self.state == "jump":
            if input_handler.is_pressed("up"):
                self.jump_time_current += delta_time
                if self.jump_time_current >= self.jump_time_max:
                    self.state = "fall"
            else:
                self.state = "fall"

        # Lógica de Movimento Horizontal
        elif input_handler.is_pressed("left"):
            self.face_direction = "left"
            self.state = "run" if self.on_ground else self.state
            self.velocity = max(-self.max_velocity, self.velocity - self.acceleration)

        elif input_handler.is_pressed("right"):
            self.face_direction = "right"
            self.state = "run" if self.on_ground else self.state
            self.velocity = min(self.max_velocity, self.velocity + self.acceleration)

        # Estado 'Idle'
        else:
            if self.on_ground:
                self.state = "idle"
                self.apply_deceleration()

    def apply_deceleration(self):
        if self.velocity > 0:
            self.velocity = max(0, self.velocity - self.deceleration)
        elif self.velocity < 0:
            self.velocity = min(0, self.velocity + self.deceleration)

    def update_position(self, delta_time, tiles):
        new_x, new_y = self.calculate_new_positions(delta_time)
        new_x = self.handle_horizontal_collision(new_x, new_y, tiles)

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
                        if self.vertical_velocity > 0:
                            # Plataforma está abaixo do pé do personagem?
                            if player_bottom <= tile_top:
                                self.on_ground = True
                                self.vertical_velocity = 0
                                return round(self.y)
                            else:
                                pass
                        # Colidindo "por baixo"
                        else:
                            pass

        if not self.on_ground:
            self.vertical_velocity += self.gravity * delta_time

        return new_y  # Otherwise, return new y position

    def update_animation_frames(self, delta_time):
        for tile in self.tiles:
            if tile["timer_next_frame"] > delta_time:
                tile["current_frame"] = (tile["current_frame"] + 1) % len(
                    tile["sprites"]
                )
                tile["timer_next_frame"] -= delta_time
            else:
                tile["timer_next_frame"] += delta_time
