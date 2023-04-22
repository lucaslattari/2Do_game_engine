import pygame
import pytmx
import time


class TiledLevel:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.animations = self.load_animations()
        self.gid_to_animation = {
            animation["gid"]: i for i, animation in enumerate(self.animations)}

    def load_animations(self):
        animations = []
        for tileset in self.tmx_data.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                tile = self.tmx_data.get_tile_properties_by_gid(gid)
                if tile and 'frames' in tile:
                    animation = {
                        "gid": gid,
                        "frames": [],
                        "timer": 0,
                        "frame_index": 0
                    }
                    for frame in tile['frames']:
                        image = self.tmx_data.get_tile_image_by_gid(frame.gid)
                        animation["frames"].append(
                            (image, frame.duration / 1000))
                    animations.append(animation)
        return animations

    def update_animations(self, delta_time):
        for animation in self.animations:
            if animation["frames"]:
                animation["timer"] += delta_time
                current_frame_duration = animation["frames"][animation["frame_index"]][1]

                # Check if it's time to switch to the next frame
                if animation["timer"] >= current_frame_duration:
                    animation["timer"] -= current_frame_duration
                    animation["frame_index"] = (
                        animation["frame_index"] + 1) % len(animation["frames"])

    def render(self, surface):
        tile_width = self.tmx_data.tilewidth
        tile_height = self.tmx_data.tileheight
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):  # is it a tiled layer?
                for x, y, gid in layer:
                    if gid in self.gid_to_animation:
                        animation = self.animations[self.gid_to_animation[gid]]
                        tile_image = animation["frames"][animation["frame_index"]][0]
                    else:
                        tile_image = self.tmx_data.get_tile_image_by_gid(gid)

                    if tile_image:
                        surface.blit(
                            tile_image, (x * tile_width,
                                         y * tile_height)
                        )

    def update(self, delta_time):
        self.update_animations(delta_time)
