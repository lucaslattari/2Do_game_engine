# Entidades e Objetos do Jogo

Este documento explora o sistema de entidades do 2Do, explicando como objetos do jogo são representados, atualizados e renderizados. O sistema de entidades fornece a base para todos os elementos interativos do jogo, desde o jogador até plataformas e itens.

## Visão Geral do Sistema de Entidades

No 2Do, todas as entidades são construídas a partir de um sistema de classes hierárquico:

- A classe `Tile` representa a unidade básica visual (um ladrilho ou sprite)
- A classe `Entity` atua como base para todos os objetos interativos no jogo
- Classes específicas como `Player`, `Platform` e `Item` estendem a classe `Entity` com comportamentos únicos

Este design orientado a objetos permite reutilização de código e extensibilidade, tornando fácil adicionar novos tipos de entidades ao jogo.

## A Classe Tile

A classe `Tile` (definida em `entity.py`) representa um elemento visual fundamental do jogo. Um tile pode ser uma parte de uma plataforma, um item coletável, ou um quadro de animação do personagem.

### Propriedades Principais

```python
class Tile:
    def __init__(self, tile_data):
        self.current_frame = 0
        self.timer_next_frame = 0.0
        self.id = tile_data.get("id")
        self.width = tile_data.get("width")
        self.height = tile_data.get("height")
        self.position = tile_data.get("position", []).copy()
        self.sprites = tile_data.get("sprites")
        self.collidable_horizontal = tile_data.get("collidable_horizontal", False)
        self.collidable_vertical = tile_data.get("collidable_vertical", False)
        self.can_descend = tile_data.get("can_descend", False)
```

Cada tile possui:

- **Informações de tamanho** (`width`, `height`): dimensões do tile em pixels
- **Posição** (`position`): lista de coordenadas onde este tile aparece no mapa, em unidades de tile (não pixels)
- **Sprites** (`sprites`): imagens que representam o tile (múltiplas para animações)
- **Propriedades de colisão** (`collidable_horizontal`, `collidable_vertical`): determinam como o tile interage com outras entidades
- **Propriedade especial** (`can_descend`): indica se o jogador pode descer por esta plataforma

### Animação de Tiles

A classe `Tile` inclui suporte para animação através de seus métodos `update` e `render`:

```python
def update(self, delta_time, frame_duration=0.1):
    self.timer_next_frame += delta_time
    if self.timer_next_frame >= frame_duration:
        self.current_frame = (self.current_frame + 1) % len(self.sprites)
        self.timer_next_frame -= frame_duration
```

Este método:
1. Acumula o tempo decorrido desde o último quadro
2. Quando o tempo acumulado excede a duração do quadro, avança para o próximo
3. Reinicia o temporizador para o próximo ciclo de animação

A animação funciona avançando ciclicamente pelos sprites disponíveis no array `self.sprites`.

### Renderização de Tiles

```python
def render(self, screen, block_size):
    for pos in self.position:
        screen.blit(
            self.sprites[self.current_frame],
            (
                pos[0] * block_size[0],
                pos[1] * block_size[1],
            ),
        )
```

O método `render`:
1. Percorre todas as posições onde este tile deve aparecer
2. Desenha o sprite atual (determinado por `current_frame`) em cada posição
3. Converte coordenadas de tile para coordenadas de pixel multiplicando pela dimensão do bloco

### Retângulos de Colisão

```python
def get_rect(self, block_size):
    rects = []
    for pos in self.position:
        rect = pygame.Rect(
            pos[0] * block_size[0], pos[1] * block_size[1], self.width, self.height
        )
        rects.append(rect)
    return rects
```

Este método cria retângulos de colisão pygame para cada posição do tile, convertendo coordenadas de tile para coordenadas de pixel.

## A Classe Entity

A classe `Entity` (também em `entity.py`) serve como base para todos os objetos interativos do jogo. Ela gerencia um conjunto de tiles e fornece métodos comuns para atualização, renderização e detecção de colisão.

```python
class Entity:
    def __init__(self, tile_data):
        self.tiles = []
        self.parse(tile_data)

    def parse(self, tile_data):
        for t in tile_data:
            tile = Tile(t)
            self.tiles.append(tile)
```

Uma `Entity` é essencialmente uma coleção de `Tile`s que são tratados como um único objeto lógico. Por exemplo:
- Um `Player` pode ter diferentes conjuntos de tiles para estados como "idle", "running" e "jumping"
- Uma `Platform` pode consistir de múltiplos tiles conectados

### Métodos Principais

```python
def render(self, screen, block_size):
    for tile in self.tiles:
        tile.render(screen, block_size)

def update(self, delta_time):
    for tile in self.tiles:
        tile.update(delta_time)

def check_collision(self, rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
```

Estes métodos:
1. `render`: Desenha todos os tiles da entidade na tela
2. `update`: Atualiza o estado de todos os tiles (animação, etc.)
3. `check_collision`: Verifica se dois retângulos estão colidindo

## Entidades Específicas

### A Classe Platform

Definida em `platformer.py`, a classe `Platform` representa superfícies onde o jogador pode andar, pular ou se mover:

```python
from entity import Entity

class Platform(Entity):
    def __init__(self, data):
        super().__init__(data)
```

Embora simples em sua implementação, as plataformas têm propriedades importantes que são definidas nos dados de seus tiles:

- `collidable_horizontal`: Se verdadeiro, o jogador não pode passar horizontalmente através da plataforma
- `collidable_vertical`: Se verdadeiro, o jogador não pode passar verticalmente através da plataforma
- `can_descend`: Se verdadeiro, o jogador pode descer pela plataforma pressionando a tecla para baixo

Estas propriedades permitem criar diversos tipos de plataformas:
- **Plataformas sólidas**: Bloqueiam movimento em todas as direções (`collidable_horizontal` e `collidable_vertical` são `True`)
- **Plataformas de mão única**: Permitem que o jogador pule através delas de baixo, mas fornecem suporte quando atingidas por cima (apenas `collidable_vertical` é `True`)
- **Plataformas atravessáveis**: Permitem que o jogador desça através delas pressionando para baixo (`can_descend` é `True`)

### A Classe Item

Definida em `item.py`, a classe `Item` representa objetos coletáveis ou interativos no jogo:

```python
from entity import Entity

class Item(Entity):
    def __init__(self, data):
        super().__init__(data)
```

A implementação da classe `Item` está em desenvolvimento, servindo como base para expansão futura. Possíveis extensões incluem:
- Adicionar lógica para coletar itens
- Implementar efeitos para diferentes tipos de itens
- Criar animações para itens

## Sistema de Colisões

Atualmente, a detecção de colisão no 2Do é implementada principalmente na classe `Player` (em `player.py`), utilizando o módulo `pygame.Rect`.

### Verificação Básica de Colisão

```python
def check_collision(self, rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
```

Este método simples verifica se dois retângulos se sobrepõem, sendo a base para todas as colisões no jogo.

### Colisão Horizontal

```python
def handle_horizontal_collision(self, new_x, current_y, tiles):
    player_rect = (
        new_x * SPRITE_BLOCK_SIZE,
        current_y * SPRITE_BLOCK_SIZE,
        self.width,
        self.height,
    )
    for tile in tiles:
        if tile.collidable_horizontal:
            for position in tile.position:
                tile_rect = (
                    position[0] * SPRITE_BLOCK_SIZE,
                    position[1] * SPRITE_BLOCK_SIZE,
                    tile.width,
                    tile.height,
                )
                if self.check_collision(player_rect, tile_rect):
                    return self.x  # Reset x position if collision detected
    return new_x  # Otherwise, return new x position
```

Este método verifica colisões horizontais:
1. Cria um retângulo representando o jogador na nova posição horizontal
2. Verifica colisões com todos os tiles marcados como `collidable_horizontal`
3. Se uma colisão for detectada, mantém a posição X atual do jogador
4. Caso contrário, permite o movimento para a nova posição X

### Colisão Vertical

```python
def handle_vertical_collision(self, current_x, new_y, tiles, delta_time):
    player_rect = (
        current_x * SPRITE_BLOCK_SIZE,
        new_y * SPRITE_BLOCK_SIZE,
        self.width,
        self.height,
    )
    for tile in tiles:
        if tile.collidable_vertical:
            for position in tile.position:
                tile_rect = (
                    position[0] * SPRITE_BLOCK_SIZE,
                    position[1] * SPRITE_BLOCK_SIZE,
                    tile.width,
                    tile.height,
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
```

Este método lida com colisões verticais com mais detalhe:
1. Verifica colisões com tiles marcados como `collidable_vertical`
2. Distingue entre colisões por cima (jogador aterrissando na plataforma) e por baixo (jogador batendo a cabeça)
3. Quando o jogador atinge uma plataforma por cima:
   - Define `on_ground` como verdadeiro
   - Zera a velocidade vertical
   - Mantém a posição Y atual
4. Se não houver colisão e o jogador não estiver no chão, aplica gravidade
5. Retorna a nova posição Y (ajustada devido à colisão)

### Descida através de Plataformas

```python
# Lógica de descida
if (
    input_handler.is_pressed("down")
    and self.on_ground
    and (state == "idle" or state == "run")
):
    for tile in tiles:
        if tile.can_descend:
            for position in tile.position:
                tile_rect = (
                    position[0] * SPRITE_BLOCK_SIZE,
                    position[1] * SPRITE_BLOCK_SIZE,
                    tile.width,
                    tile.height,
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
                    self.descend_time_current = 0
                    return
```

Esta lógica permite que o jogador desça através de plataformas atravessáveis:
1. Verifica se o jogador está pressionando para baixo, está no chão e em um estado apropriado
2. Verifica se o jogador está sobre uma plataforma com `can_descend` ativado
3. Se verdadeiro, altera o estado para "descend", permite a queda e inicia um temporizador de descida

## Ciclo de Atualização de Entidades

O processo de atualização de entidades ocorre a cada quadro do jogo:

1. **Game Loop** (em `main.py`):
   ```python
   while running:
       delta_time = clock.tick(60) / 1000.0
       input_handler.process_events()
       game.update(delta_time, input_handler)
       game.render(game.screen)
       pygame.display.update()
   ```

2. **Game Update** (em `game.py`):
   ```python
   def update(self, delta_time, input_handler):
       if self.background:
           self.background.update(delta_time)
       if self.item:
           self.item.update(delta_time)
       if self.platform:
           self.platform.update(delta_time)
       if self.player:
           self.player.update(delta_time, input_handler, self.platform.tiles)
   ```

3. **Entity Update** (em `entity.py` e classes derivadas):
   - Entidades básicas apenas atualizam animações
   - O jogador tem lógica adicional para movimento, física e colisões

Este padrão de atualização em cascata garante que todas as entidades sejam processadas a cada quadro, com lógica específica implementada nas subclasses conforme necessário.

## Resumo do Sistema de Entidades

O sistema de entidades do 2Do fornece:

1. **Abstração flexível**: A classe `Entity` serve como base para todos os objetos interativos
2. **Animação simples**: Suporte incorporado para animar sprites através da classe `Tile`
3. **Detecção de colisão**: Métodos para verificar e responder a colisões entre entidades
4. **Física básica**: Implementação de gravidade, salto e movimento para o jogador
5. **Extensibilidade**: Facilidade para adicionar novos tipos de entidades herdando da classe base

Esta arquitetura torna o 2Do adequado para desenvolver jogos de plataforma 2D com diversos tipos de objetos interativos, mantendo o código organizado e modular.

## Próximos Passos

Agora que você compreende o sistema de entidades, pode explorar:

- [Lógica de Jogo e Jogador](logica_jogo.md) - Detalhes sobre a implementação do personagem jogável
- [Sistema de Entrada e Controle](controle.md) - Como o jogo processa entrada do usuário
- [Sistema de Gerenciamento de Recursos](assets.md) - Como os recursos são carregados e utilizados pelas entidades