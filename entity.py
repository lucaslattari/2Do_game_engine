class Entity:
    def __init__(self, tile_data):
        self.tiles = []
        self.parse(tile_data)

    def parse(self, tile_data):
        for t in tile_data:
            tile = {
                "current_frame": 0,
                "timer_next_frame": 0.0,
                "id": t.get("id"),
                "width": t.get("width"),
                "height": t.get("height"),
                "position": t.get("position", []).copy(),
                "sprites": t.get("sprites"),
                "collidable_horizontal": t.get("collidable_horizontal"),
                "collidable_vertical": t.get("collidable_vertical"),
            }

            self.tiles.append(tile)

    def render(self, screen, block_size):
        for tile in self.tiles:
            for position in tile["position"]:
                screen.blit(
                    tile["sprites"][tile["current_frame"]],
                    (
                        position[0] * block_size[0],
                        position[1] * block_size[1],
                    ),
                )

    def update(self, delta_time):
        for tile in self.tiles:
            if tile["timer_next_frame"] > delta_time:
                tile["current_frame"] = (tile["current_frame"] + 1) % len(
                    tile["sprites"]
                )
                tile["timer_next_frame"] -= delta_time
            else:
                tile["timer_next_frame"] += delta_time

    def check_collision(self, rect1, rect2):
        x1, y1, w1, h1 = tuple(map(int, rect1))
        x2, y2, w2, h2 = tuple(map(int, rect2))
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2
