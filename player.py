import pygame

from entity import Entity

ANIMATION_TYPES = ["run", "idle", "jump"]


class Player(Entity):
    def __init__(self, data):
        super().__init__(data)

        self.state = "idle"
        self.face_direction = "right"
        self.x = self.tiles[0]["position"][0][0]  # todo: consertar isso daqui
        self.y = self.tiles[0]["position"][0][1]

        self.width = self.tiles[0]["width"]
        self.height = self.tiles[0]["height"]

        self.velocity = 0.0
        self.max_velocity = 10.0
        self.acceleration = 0.4
        self.deceleration = 0.4

        self.vertical_velocity = 0.0
        self.jump_acceleration = -11.0
        self.gravity = 12.8
        self.on_ground = True

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
        self.update_state_and_velocity(input_handler)
        self.update_position(delta_time, tiles)
        self.update_animation_frames(delta_time)

    def update_state_and_velocity(self, input_handler):
        if input_handler.is_pressed("up") and self.on_ground:
            self.vertical_velocity = self.jump_acceleration
            self.state = "jump"
            self.on_ground = False

        if input_handler.is_pressed("left"):
            self.face_direction = "left"
            self.state = "run"
            self.velocity = max(-self.max_velocity, self.velocity - self.acceleration)
        elif input_handler.is_pressed("right"):
            self.face_direction = "right"
            self.state = "run"
            self.velocity = min(self.max_velocity, self.velocity + self.acceleration)
        else:
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
        new_y = self.handle_vertical_collision(new_x, new_y, tiles, delta_time)

        self.x = new_x
        self.y = new_y

    def calculate_new_positions(self, delta_time):
        new_x = self.x + self.velocity * delta_time
        new_y = self.y + self.vertical_velocity * delta_time
        return new_x, new_y

    def handle_horizontal_collision(self, new_x, current_y, tiles):
        player_rect = (new_x * 16, current_y * 16, self.width, self.height)
        for tile in tiles:
            if "collidable" in tile and tile["collidable"]:
                for position in tile["position"]:
                    tile_rect = (
                        position[0] * 16,
                        position[1] * 16,
                        tile["width"],
                        tile["height"],
                    )
                    if self.check_collision(player_rect, tile_rect):
                        return self.x  # Reset x position if collision detected
        return new_x  # Otherwise, return new x position

    def handle_vertical_collision(self, current_x, new_y, tiles, delta_time):
        self.on_ground = False
        player_rect = (current_x * 16, new_y * 16, self.width, self.height)
        for tile in tiles:
            if "collidable" in tile and tile["collidable"]:
                for position in tile["position"]:
                    tile_rect = (
                        position[0] * 16,
                        position[1] * 16,
                        tile["width"],
                        tile["height"],
                    )
                    if self.check_collision(player_rect, tile_rect):
                        self.on_ground = True
                        self.vertical_velocity = 0
                        return self.y  # Reset y position if collision detected

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
