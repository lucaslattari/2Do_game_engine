import pytmx

TILE_TYPES = ["Player", "Item", "Platform"]


class AssetManager:
    def __init__(self, level):
        self.tiles = self.load_tiles(level)
        self.tile_width = level.tilewidth
        self.tile_height = level.tileheight

    def load_tiles(self, level):
        tiles = {tile_type: [] for tile_type in TILE_TYPES}
        gid_to_position = {}

        # Gather positions of gids
        for layer in level.layers:
            for x, y, gid in layer:
                gid_to_position.setdefault(gid, []).append((x, y))

        # Populate tiles
        for tileset in level.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                tile = level.get_tile_properties_by_gid(gid)
                if not tile:
                    continue
                tile["gid"] = gid

                # Verificar a propriedade 'collidable'
                tile["collidable"] = tile.get("collidable", False)

                self.update_tiles(tile, tiles, gid_to_position.get(gid), level)

        return tiles

    def update_tiles(self, tile, tiles, gid_to_position, level):
        tile_type = tile["type"]
        if any(tile_type.startswith(term) for term in TILE_TYPES):
            tile["sprites"] = self.load_sprites(level, tile)

            if gid_to_position:
                tile["position"] = gid_to_position

            tile_type = tile_type.split("_")[0]
            if "position" in tile:
                tiles[tile_type].append(tile)

    def load_sprites(self, level, tile):
        sprites = []
        frames = tile.get("frames", [])

        if not frames:
            sprites.append(level.get_tile_image_by_gid(tile["gid"]))
        else:
            for frame in frames:
                sprites.append(level.get_tile_image_by_gid(frame.gid))
        return sprites

    def get_asset(self, type):
        return self.tiles[type]
