import pytmx


class AssetManager:
    def __init__(self, level):
        self.tiles = self.load_tiles(level)
        self.tile_width = level.tilewidth
        self.tile_height = level.tileheight

    def load_tiles(self, level):
        tiles = {}
        tiles["Player"] = []
        tiles["Item"] = []
        tiles["Terrain"] = []
        tiles["Platform"] = []

        gid_to_position = {}
        for layer in level.visible_layers:
            for x, y, gid in layer:
                if gid not in gid_to_position:
                    gid_to_position[gid] = []
                gid_to_position[gid].append((x, y))

        for tileset in level.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                tile = level.get_tile_properties_by_gid(gid)
                tile["gid"] = gid

                if gid in gid_to_position:
                    tile["position"] = gid_to_position[gid]

                if (
                    tile["type"] == "Player"
                    or tile["type"] == "Item"
                    or tile["type"] == "Platform"
                ):
                    if "frames" in tile:
                        sprites = []
                        for frame in tile["frames"]:
                            sprites.append(level.get_tile_image_by_gid(frame.gid))
                        tile["sprites"] = sprites
                elif tile["type"] == "Terrain":
                    tile["sprites"] = []
                    tile["sprites"].append(level.get_tile_image_by_gid(tile["gid"]))

                if tile["type"] == "Player":
                    if tile["frames"]:
                        tiles["Player"].append(tile)

                if tile["type"] == "Item":
                    if tile["frames"]:
                        tiles["Item"].append(tile)

                if tile["type"] == "Terrain":
                    if "position" in tile:
                        tiles["Terrain"].append(tile)

                if tile["type"] == "Platform":
                    if tile["frames"]:
                        tiles["Platform"].append(tile)

        return tiles

    def get_asset(self, type):
        return self.tiles[type]

    """
    def get_tile_image(self, gid):
        return self.tmx_data.get_tile_image_by_gid(gid)

    def get_tile_properties(self, gid):
        return self.tmx_data.get_tile_properties_by_gid(gid)

    def get_tileset_range(self, tileset):
        return range(tileset.firstgid, tileset.firstgid + tileset.tilecount)
    """
