import pytmx


class AssetManager:
    def __init__(self, level, tile_types=None):
        if tile_types is None:
            tile_types = ["Player", "Item", "Platform"]
        self.tile_types = tile_types
        self.tiles = self.load_tiles(level)
        self.tile_width = level.tilewidth
        self.tile_height = level.tileheight

    def load_tiles(self, level):
        tiles = {tile_type: [] for tile_type in self.tile_types}
        gid_to_position = {}

        # Reunir posições dos GIDs
        for layer in level.layers:
            for x, y, gid in layer:
                gid_to_position.setdefault(gid, []).append((x, y))

        # Populando os tiles
        for tileset in level.tilesets:
            for gid in range(tileset.firstgid, tileset.firstgid + tileset.tilecount):
                tile = level.get_tile_properties_by_gid(gid)
                if not tile:
                    continue

                tile["gid"] = gid

                # Verificar as propriedades 'collidable' e 'can_descend'
                tile["collidable_horizontal"] = tile.get("collidable_horizontal", False)
                tile["collidable_vertical"] = tile.get("collidable_vertical", False)
                tile["can_descend"] = tile.get("can_descend", False)

                self.update_tiles(tile, tiles, gid_to_position.get(gid), level)

        return tiles

    def update_tiles(self, tile, tiles, gid_to_position, level):
        tile_type = tile.get("type")
        if tile_type and any(tile_type.startswith(term) for term in self.tile_types):
            tile["sprites"] = self.load_sprites(level, tile)

            if gid_to_position:
                tile["position"] = gid_to_position

            if "_" in tile_type:
                tile_type = tile_type.split("_")[0]

            if "position" in tile:
                tiles[tile_type].append(tile)

    def load_sprites(self, level, tile):
        sprites = []
        frames = tile.get("frames", [])

        if not frames:
            sprite = level.get_tile_image_by_gid(tile["gid"])
            if sprite:
                sprites.append(sprite)
        else:
            for frame in frames:
                sprite = level.get_tile_image_by_gid(frame.gid)
                if sprite:
                    sprites.append(sprite)
        return sprites

    def get_asset(self, asset_type):
        return self.tiles.get(asset_type, [])
