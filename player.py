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

        self.velocity = 0.0
        self.max_velocity = 7.0
        self.acceleration = 0.2
        self.deceleration = 0.2

        self.vertical_velocity = 0.0
        self.jump_acceleration = -15.0
        self.gravity = 9.8
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

    def update(self, delta_time, input_handler):
        print(self.x, self.y, self.on_ground)
        self.update_state_and_velocity(input_handler)
        self.update_position(delta_time)
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

    def update_position(self, delta_time):
        self.x += self.velocity * delta_time
        self.y += self.vertical_velocity * delta_time

        # Aplicando a gravidade
        if not self.on_ground:
            self.vertical_velocity += self.gravity * delta_time
            if self.y >= 22:
                self.vertical_velocity = 0.0
                self.on_ground = True
                self.state = "idle"

    def update_animation_frames(self, delta_time):
        for tile in self.tiles:
            if tile["timer_next_frame"] > delta_time:
                tile["current_frame"] = (tile["current_frame"] + 1) % len(
                    tile["sprites"]
                )
                tile["timer_next_frame"] -= delta_time
            else:
                tile["timer_next_frame"] += delta_time
