# Sistema de Gerenciamento de Recursos

Este documento explica como o 2Do gerencia recursos gráficos (sprites, tiles) e outros assets necessários para o funcionamento do jogo.

## Visão Geral

O sistema de gerenciamento de recursos do 2Do é centralizado no arquivo `asset_manager.py`, que contém a classe `AssetManager`. Esta classe é responsável por:

1. Carregar tiles e sprites de arquivos de mapa (formato TMX)
2. Organizar os recursos por tipo (Player, Item, Platform, etc.)
3. Extrair propriedades importantes (colisão, animação)
4. Fornecer acesso fácil aos recursos para outras partes do motor

O 2Do utiliza a biblioteca PyTMX para carregar mapas criados com o Tiled Map Editor, o que permite aos desenvolvedores criar níveis visualmente e definir propriedades personalizadas para cada elemento do jogo.

## A Classe AssetManager

```python
class AssetManager:
    def __init__(self, level, tile_types=None):
        if tile_types is None:
            tile_types = ["Player", "Item", "Platform"]
        self.tile_types = tile_types
        self.tiles = self.load_tiles(level)
        self.tile_width = level.tilewidth
        self.tile_height = level.tileheight
```

O construtor da classe aceita dois parâmetros:
- `level`: O objeto de nível carregado pelo PyTMX (contém todas as informações do mapa)
- `tile_types`: Uma lista opcional de tipos de tiles a serem carregados (padrão: Player, Item, Platform)

## Processo de Carregamento de Recursos

### Inicialização

Quando um nível é carregado na classe `Game` através do método `load_level()`, o seguinte processo ocorre:

1. O arquivo TMX é carregado usando `pytmx.load_pygame()`
2. Uma instância de `AssetManager` é criada, recebendo o nível carregado
3. O `AssetManager` extrai todos os recursos e propriedades do arquivo TMX
4. Os recursos são agrupados por tipo e disponibilizados para as entidades do jogo

```python
# Trecho de game.py
def load_level(self, level_filename):
    try:
        self.tiled_level = pytmx.load_pygame(level_filename)
        self.load_assets()
        # ...
    except Exception as e:
        print(f"Erro ao carregar o nível: {e}")

def load_assets(self):
    self.asset_manager = AssetManager(self.tiled_level)
    
    self.player = Player(self.asset_manager.get_asset("Player"))
    self.item = Item(self.asset_manager.get_asset("Item"))
    self.platform = Platform(self.asset_manager.get_asset("Platform"))
```

### O Método load_tiles

O método `load_tiles` é o coração do sistema de carregamento de recursos:

```python
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

            # Verificar as propriedades especiais
            tile["collidable_horizontal"] = tile.get("collidable_horizontal", False)
            tile["collidable_vertical"] = tile.get("collidable_vertical", False)
            tile["can_descend"] = tile.get("can_descend", False)

            self.update_tiles(tile, tiles, gid_to_position.get(gid), level)

    return tiles
```

Vamos analisar como este método funciona:

1. **Preparação das estruturas de dados**:
   - Cria um dicionário `tiles` para armazenar tiles organizados por tipo. Tiles podem ser de plataforma (por exemplo, um bloco de terra ou pedra onde o jogador caminha), de jogador (posição do personagem principal) e de item (pode ser uma moeda, power-up ou chave).
   - Cria um dicionário `gid_to_position` para mapear identificadores globais (GIDs) para suas posições no mapa. O GID significa "Global Identifier", ou seja, um número de série único para cada tipo de tile do jogo. 

   Este dicionário é como um mapa que diz: "Este tipo de bloco (GID) aparece nestas coordenadas do mapa". Por exemplo:
   
   - O bloco de terra (GID 101) aparece nas posições (5,10), (6,10) e (7,10) - formando uma plataforma horizontal
   - A moeda dourada (GID 201) aparece na posição (5,5) - flutuando acima da plataforma
   - O personagem (GID 301) aparece na posição (7,3) - posicionado para pular na plataforma
   
   Este mapeamento permite que o jogo saiba onde colocar cada elemento visual na tela.

2. **Mapeamento de posições**:
   - Percorre todas as camadas do mapa
   - Para cada tile encontrado, registra sua posição (x, y) no dicionário `gid_to_position`

3. **Processamento de tilesets**:
   - Percorre todos os tilesets carregados
   - Para cada GID válido, obtém as propriedades associadas
   - Adiciona o GID às propriedades e configura flags de colisão (indicando quais tiles podem ser atravessados ou não pelo jogador)
   - Chama `update_tiles` para processar os tiles e organizá-los por tipo

### O Método update_tiles

Este método categoriza os tiles com base em seu tipo e prepara-os para uso no jogo:

```python
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
```

Este método:
1. Verifica se o tile possui um tipo definido que corresponde a um dos tipos esperados
2. Carrega os sprites associados ao tile através do método `load_sprites`
3. Adiciona informações de posição ao tile
4. Processa o tipo do tile (removendo qualquer sufixo após o underscore)
5. Adiciona o tile ao dicionário de tiles do tipo apropriado

### O Método load_sprites

O método `load_sprites` é responsável por carregar as imagens dos tiles, incluindo suporte para animações:

```python
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
```

Este método:
1. Verifica se o tile possui frames de animação definidos
2. Se não houver frames, carrega a imagem estática do tile
3. Se houver frames, carrega cada frame como um sprite separado
4. Retorna uma lista de sprites que pode conter uma única imagem (tile estático) ou múltiplas imagens (animação)

## Acessando os Recursos

Após o carregamento, os recursos podem ser acessados através do método `get_asset`:

```python
def get_asset(self, asset_type):
    return self.tiles.get(asset_type, [])
```

Este método retorna todos os tiles de um determinado tipo (por exemplo, "Player", "Item", "Platform"). Esses tiles são então passados para as classes correspondentes durante a inicialização:

```python
# Em game.py
self.player = Player(self.asset_manager.get_asset("Player"))
self.item = Item(self.asset_manager.get_asset("Item"))
self.platform = Platform(self.asset_manager.get_asset("Platform"))
```

## Propriedades Especiais de Tiles

O AssetManager reconhece e processa propriedades especiais definidas no Tiled Map Editor:

- **`collidable_horizontal`**: Indica se o tile causa colisão horizontal (impede movimento lateral)
- **`collidable_vertical`**: Indica se o tile causa colisão vertical (impede movimento para cima/baixo)
- **`can_descend`**: Indica se o jogador pode descer através da plataforma (pressionando para baixo)

Estas propriedades devem ser definidas no Tiled Map Editor como propriedades personalizadas dos tiles.

## Estrutura de Dados de Tiles

Cada tile processado pelo AssetManager possui a seguinte estrutura:

```python
{
    "gid": 123,                        # Identificador global do tile
    "width": 16,                       # Largura do tile em pixels
    "height": 16,                      # Altura do tile em pixels
    "position": [(x1, y1), (x2, y2)],  # Lista de posições no mapa
    "sprites": [sprite1, sprite2],     # Lista de sprites (um ou mais para animação)
    "collidable_horizontal": True,     # Flag de colisão horizontal
    "collidable_vertical": True,       # Flag de colisão vertical
    "can_descend": False,              # Flag para permitir descida
    "type": "Platform"                 # Tipo do tile
}
```

## Dicas para Criar Mapas Compatíveis

Para criar mapas compatíveis com o sistema de assets do 2Do:

1. **Nomeie corretamente os tipos de tiles**:
   - Para o jogador: "Player_idle", "Player_run", "Player_jump"
   - Para plataformas: "Platform"
   - Para itens: "Item"

2. **Configure propriedades de colisão**:
   - Adicione propriedades booleanas `collidable_horizontal` e `collidable_vertical` às plataformas
   - Para plataformas que permitem descida, defina `can_descend` como `true`

3. **Configure animações**:
   - Para tiles animados, configure os frames no Tiled Map Editor
   - O AssetManager carregará automaticamente todos os frames

4. **Organize camadas no Tiled**:
   - Separe diferentes tipos de entidades em camadas distintas para melhor organização

## Próximos Passos

Agora que você entende como o 2Do gerencia recursos, pode explorar:

- [Entidades e Objetos do Jogo](entidades.md) - Como os recursos carregados são utilizados pelas entidades
- [Plano de Fundo e Interface](plano_fundo.md) - Como o sistema de fundo usa recursos de imagem