# Lógica de Jogo e Jogador

Este documento explora a lógica central do 2Do, focando em como o jogo é inicializado, gerenciado e como o jogador interage com o mundo do jogo. Entender estes aspectos é fundamental para quem deseja personalizar ou expandir o motor.

## Arquitetura da Lógica de Jogo

O 2Do implementa um modelo clássico de jogo de plataforma 2D, com estes componentes principais:

1. **Ciclo de jogo**: Mantém o jogo em execução, sincronizando atualizações e renderização
2. **Sistema de física**: Implementa gravidade, movimento e colisões 
3. **Máquina de estados**: Gerencia os diferentes estados do jogador (parado, correndo, pulando)
4. **Controle do jogador**: Processa entrada do usuário e atualiza o estado do jogador

Estes sistemas trabalham juntos para criar a experiência de jogo, com código distribuído principalmente entre os arquivos `game.py` e `player.py`.

## Inicialização e Ciclo do Jogo

### Ponto de Entrada

A inicialização do 2Do começa no arquivo `main.py`, que configura o ambiente e inicia o ciclo principal:

```python
pygame.init()
pygame.font.init()

config_parser = read_config_file("config.ini")

game = Game(config_parser=config_parser)
game.load_screen()
game.load_level("maps/level1.tmx")

input_handler = InputHandler(config_parser)

clock = pygame.time.Clock()
running = True

while running:
    delta_time = clock.tick(60) / 1000.0
    
    input_handler.process_events()
    if input_handler.quit_game:
        running = False
        
    game.update(delta_time, input_handler)
    game.screen.fill((0, 0, 0))
    game.render(game.screen)
    render_fps(clock.get_fps(), game.screen, font)
    
    pygame.display.update()
```

Este código:
1. Inicializa o Pygame e seus subsistemas
2. Carrega as configurações do arquivo `config.ini`
3. Cria uma instância da classe `Game`
4. Configura a tela e carrega o nível inicial
5. Cria um manipulador de entrada para processar as ações do jogador
6. Inicia o ciclo principal (game loop) que executará até o jogo ser encerrado

### Compreendendo o Delta

Uma parte crucial do ciclo de jogo é o cálculo do `delta_time`:

```python
delta_time = clock.tick(60) / 1000.0
```

O delta representa o tempo real decorrido (em segundos) desde o último quadro de animação (frame). Este conceito é fundamental para criar movimentos consistentes independentemente da velocidade do hardware.

**Por que o delta é importante?**

Sem usar o delta, o movimento seria baseado em quadros, não em tempo real:

- Em um computador potente executando a 120 FPS: uma animação ocorreria duas vezes mais rápido
- Em um computador lento executando a 30 FPS: a mesma animação seria duas vezes mais lenta

**Como o 2Do utiliza o delta:**

No 2Do, todas as atualizações de movimento e física recebem o delta como parâmetro:

```python
# No método update do player
def update(self, delta_time, input_handler, tiles):
    self.update_state_and_velocity(input_handler, delta_time, tiles)
    self.update_position(delta_time, tiles)
    self.update_animation_frames(delta_time)
```

Internamente, o delta é aplicado nas operações de movimento:

```python
# Trecho real da atualização de posição no 2Do
new_x = self.x + self.velocity * delta_time
new_y = self.y + self.vertical_velocity * delta_time
```

**Exemplo ilustrativo:**

Para entender o conceito, considere dois cenários hipotéticos:

1. **Sem delta (incorreto)**:
   ```python
   # A cada frame, o personagem sempre se move 5 pixels
   position_x += 5
   ```

2. **Com delta (como no 2Do)**:
   ```python
   # O personagem se move a uma velocidade constante de 300 pixels por segundo
   position_x += 300 * delta_time
   ```

No segundo caso:
- Em um frame que leva 1/60s (0.0167s): `position_x += 300 * 0.0167 = 5 pixels`
- Em um frame que leva 1/30s (0.0333s): `position_x += 300 * 0.0333 = 10 pixels`

Isto garante que, independentemente da taxa de quadros, o personagem sempre se move à mesma velocidade real, criando uma experiência consistente em diferentes hardwares.

### A Classe Game

A classe `Game` (no arquivo `game.py`) gerencia o estado global do jogo:

```python
class Game:
    def __init__(self, config_parser, width=800, height=600):
        self.config_parser = config_parser
        resolution_str = self.config_parser.get("graphics", "resolution", fallback="1280x720")
        self.width, self.height = map(int, resolution_str.split("x"))
        self.is_fullscreen = self.config_parser.get("graphics", "fullscreen", fallback="no").lower() == "yes"
        self.screen = None
        self.background = None
        self.screen_needs_update = True
```

Durante a inicialização, esta classe:
1. Carrega as configurações de resolução e modo de exibição
2. Configura a tela com base nessas configurações
3. Prepara variáveis para armazenar o estado do jogo (fundo, entidades)

### Carregamento de Níveis

O método `load_level` é responsável por carregar os arquivos TMX (criados com o Tiled Map Editor) e inicializar as entidades do jogo:

```python
def load_level(self, level_filename):
    try:
        self.tiled_level = pytmx.load_pygame(level_filename)
        self.load_assets()
        self.background = Background(self.tiled_level, self.config_parser)
    except Exception as e:
        print(f"Erro ao carregar o nível: {e}")

def load_assets(self):
    self.asset_manager = AssetManager(self.tiled_level)
    self.player = Player(self.asset_manager.get_asset("Player"))
    self.item = Item(self.asset_manager.get_asset("Item"))
    self.platform = Platform(self.asset_manager.get_asset("Platform"))
```

Este processo:
1. Carrega o arquivo de mapa usando PyTMX
2. Cria um gerenciador de assets para extrair recursos do mapa
3. Inicializa as entidades do jogo (jogador, itens, plataformas)
4. Configura o plano de fundo com base no mapa e configurações

## O Jogador e sua Interação com o Mundo

A classe `Player` (arquivo `player.py`) é o coração da jogabilidade, gerenciando o personagem controlável.

### Inicialização do Jogador

```python
class Player(Entity):
    def __init__(self, data):
        super().__init__(data)
        
        self.state = "idle"
        self.face_direction = "right"
        self.x = self.tiles[0].position[0][0]
        self.y = self.tiles[0].position[0][1]
        
        self.width = self.tiles[0].width
        self.height = self.tiles[0].height
        
        self.velocity = 0.0
        self.max_velocity = 12.0
        self.acceleration = 1.0
        self.deceleration = 8.0
        
        self.vertical_velocity = 0.0
        self.jump_acceleration = -24.0
        self.gravity = 35
        self.on_ground = True
        
        self.jump_time_max = 0.2
        self.jump_time_current = 0
        
        self.descend_time_max = 0.12
        self.descend_time_current = 0
```

Esta inicialização configura:
1. **Estado inicial**: Começa no estado "idle" (parado), virado para a direita
2. **Posição**: Definida pela posição do primeiro tile do jogador no mapa
3. **Tamanho**: Largura e altura para detecção de colisão
4. **Parâmetros de movimento horizontal**: Velocidade, aceleração e desaceleração
5. **Parâmetros de movimento vertical**: Gravidade, força de salto e detecção de chão
6. **Parâmetros de tempo**: Duração máxima do salto e do tempo de descida

### Ciclo de Atualização do Jogador

O método `update` do jogador é chamado a cada quadro, coordenando toda a lógica do personagem:

```python
def update(self, delta_time, input_handler, tiles):
    self.update_state_and_velocity(input_handler, delta_time, tiles)
    self.update_position(delta_time, tiles)
    self.update_animation_frames(delta_time)
```

Este método divide a atualização em três etapas:
1. **Atualização de estado e velocidade**: Determina a máquina de estados e como o jogador deve mover com base em entrada do usuário
2. **Atualização de posição**: Aplica física e detecta colisões para determinar a posição final
3. **Atualização de animação**: Atualiza os quadros de animação com base no estado atual

### Máquina de Estados do Jogador

O jogador pode estar em diferentes estados, cada um com comportamento específico:

- **"idle"**: Parado, sem movimento horizontal
- **"run"**: Movendo-se horizontalmente
- **"jump"**: Subindo após um salto
- **"fall"**: Caindo após atingir o ápice do salto ou cair de uma plataforma
- **"descend"**: Estado especial para descer através de plataformas atravessáveis

A transição entre estados acontece em `update_state_and_velocity`:

```python
def update_state_and_velocity(self, input_handler, delta_time, tiles):
    state = self.state
    
    # Lógica de descida
    if input_handler.is_pressed("down") and self.on_ground and (state == "idle" or state == "run"):
        # Verifica se está sobre uma plataforma atravessável e inicia descida
        
    # Lógica de movimento horizontal
    if input_handler.is_pressed("left"):
        self.face_direction = "left"
        if self.on_ground:
            self.state = "run"
        self.velocity = max(-self.max_velocity, self.velocity - self.acceleration)
    elif input_handler.is_pressed("right"):
        self.face_direction = "right"
        if self.on_ground:
            self.state = "run"
        self.velocity = min(self.max_velocity, self.velocity + self.acceleration)
    else:
        if self.on_ground and (state == "run" or state == "idle"):
            self.state = "idle"
            self.apply_deceleration()
    
    # Lógica de salto
    if state != "jump" and input_handler.is_pressed("up") and self.on_ground:
        self.state = "jump"
        self.on_ground = False
        self.vertical_velocity = self.jump_acceleration
        self.jump_time_current = 0
    
    # Lógica de pulo sustentado
    if state == "jump":
        if input_handler.is_pressed("up"):
            self.jump_time_current += delta_time
            if self.jump_time_current >= self.jump_time_max:
                self.state = "fall"
        else:
            self.state = "fall"
    
    # Lógica de queda
    if not self.on_ground and state != "jump" and state != "descend":
        self.state = "fall"
    
    # Verificação de colisão vertical
    if self.on_ground and (self.state == "fall" or self.state == "descend"):
        self.state = "idle"
```

**Descrição da Máquina de Estados:**

O jogador no 2Do transita entre cinco estados principais, com regras específicas para cada transição:

1. De **IDLE** (parado):
   - Ao pressionar esquerda/direita: transita para **RUN**
   - Ao pressionar cima: transita para **JUMP**
   - Ao pressionar baixo sobre plataforma atravessável: transita para **DESCEND**
   - Ao perder contato com o solo: transita para **FALL**

2. De **RUN** (correndo):
   - Ao soltar as teclas de direção: retorna para **IDLE**
   - Ao pressionar cima: transita para **JUMP**
   - Ao pressionar baixo sobre plataforma atravessável: transita para **DESCEND**
   - Ao perder contato com o solo: transita para **FALL**

3. De **JUMP** (saltando):
   - Ao soltar a tecla de cima: transita para **FALL**
   - Ao atingir o tempo máximo de salto: transita para **FALL**

4. De **FALL** (caindo):
   - Ao colidir com uma plataforma por cima: transita para **IDLE**

5. De **DESCEND** (descendo através de plataforma):
   - Ao terminar o tempo de descida: transita para **FALL**
   - Ao atingir uma plataforma sólida: transita para **IDLE**

As animações e comportamentos físicos mudam com cada estado, criando uma experiência de controle fluida e responsiva.

**TODO:** No futuro, adicionar um diagrama visual da máquina de estados para facilitar a compreensão das transições entre estados do jogador.

### Física de Movimento

A física do jogador é implementada em `update_position`, que calcula a nova posição com base nas velocidades e verifica colisões:

```python
def update_position(self, delta_time, tiles):
    new_x, new_y = self.calculate_new_positions(delta_time)
    new_x = self.handle_horizontal_collision(new_x, self.y, tiles)

    # Atualiza a posição Y e a velocidade vertical
    if self.state == "jump":
        if self.jump_time_current < self.jump_time_max:
            additional_jump_force = -2 * (self.jump_time_max - self.jump_time_current) / self.jump_time_max
            self.vertical_velocity += additional_jump_force * self.gravity * delta_time
    else:
        self.vertical_velocity += self.gravity * delta_time

    new_y = self.y + self.vertical_velocity * delta_time

    # Descida através de plataformas
    if self.state == "descend":
        self.descend_time_current += delta_time
        if self.descend_time_current >= self.descend_time_max:
            self.state = "fall"

    new_y = self.handle_vertical_collision(new_x, new_y, tiles, delta_time)

    self.x = new_x
    self.y = new_y
```

Este método segue estes passos:
1. Calcula posições provisórias com base nas velocidades atuais
2. Verifica e resolve colisões horizontais
3. Aplica gravidade e forças adicionais ao movimento vertical
4. Gerencia o estado de descida através de plataformas
5. Verifica e resolve colisões verticais
6. Atualiza as posições finais

### Conceitos de Física no Jogo

#### Movimento Horizontal

O movimento horizontal segue um modelo de aceleração e desaceleração para criar uma sensação de inércia:

```python
# Aceleração quando uma tecla de direção é pressionada
self.velocity = min(self.max_velocity, self.velocity + self.acceleration)

# Desaceleração quando nenhuma tecla é pressionada
def apply_deceleration(self):
    if self.velocity > 0:
        self.velocity = max(0, self.velocity - self.deceleration)
    elif self.velocity < 0:
        self.velocity = min(0, self.velocity + self.deceleration)
```

Este sistema cria um movimento mais natural do que simplesmente definir uma velocidade constante quando uma tecla é pressionada.

#### Gravidade e Salto

O sistema de gravidade é baseado em aceleração constante, assim como na física do mundo real:

```python
# Aplica gravidade
self.vertical_velocity += self.gravity * delta_time

# Inicia um salto
self.vertical_velocity = self.jump_acceleration
```

O salto usa um valor negativo de aceleração (para cima, na coordenada Y do Pygame), enquanto a gravidade constantemente puxa o jogador para baixo.

#### Salto Variável

Um detalhe interessante é o "salto variável", onde a duração do pressionamento da tecla afeta a altura do salto:

```python
if self.state == "jump":
    if input_handler.is_pressed("up"):
        self.jump_time_current += delta_time
        if self.jump_time_current >= self.jump_time_max:
            self.state = "fall"
    else:
        self.state = "fall"
```

Se o jogador soltar a tecla de salto rapidamente, o personagem começará a cair mais cedo, resultando em um salto mais curto. Isto adiciona mais controle e nuance ao movimento.

#### Força de Salto Adicional

O jogador recebe uma força de salto adicional enquanto está subindo:

```python
if self.state == "jump":
    if self.jump_time_current < self.jump_time_max:
        additional_jump_force = -2 * (self.jump_time_max - self.jump_time_current) / self.jump_time_max
        self.vertical_velocity += additional_jump_force * self.gravity * delta_time
```

Esta força diminui gradualmente conforme o jogador se aproxima da duração máxima do salto, criando uma trajetória mais natural para o usuário.

### Sistema de Colisão

O jogador interage com o mundo através de colisões, implementadas em dois métodos principais:

#### Colisões Horizontais

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
                    return self.x  # Mantém posição X atual
    return new_x  # Permite movimento para nova posição X
```

Este método verifica se o movimento horizontal levaria a uma colisão com alguma plataforma. Se houver colisão, o jogador mantém sua posição atual.

#### Colisões Verticais

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
                    # Verifica se está caindo sobre a plataforma
                    if self.vertical_velocity > 0 and self.state != "descend":
                        self.on_ground = True
                        self.vertical_velocity = 0
                        return round(self.y)
    
    # Se não houver colisão, continua aplicando gravidade
    if not self.on_ground:
        self.vertical_velocity += self.gravity * delta_time
    
    return new_y
```

A detecção de colisão vertical verifica principalmente quando o jogador está caindo sobre uma plataforma:

1. Verifica se o jogador está em rota de colisão com um tile que tenha a propriedade `collidable_vertical`
2. Quando há colisão, verifica se o jogador está caindo (`vertical_velocity > 0`) e não está no estado de descida deliberada
3. Se essas condições forem atendidas, o jogador é definido como "no chão" (`on_ground = True`)
4. A velocidade vertical é zerada, interrompendo a queda
5. O jogador mantém sua posição Y atual, evitando penetrar na plataforma

Se nenhuma colisão for detectada e o jogador não estiver no chão, a gravidade continua sendo aplicada, aumentando a velocidade vertical (acelerando a queda).

Esta implementação prioriza o caso mais comum em jogos de plataforma: detectar quando o jogador aterrissa em uma superfície após um salto ou queda.

## Renderização e Animação

Após toda a lógica de atualização, o jogo renderiza o estado atual na tela:

```python
# Em Game.render
def render(self, screen):
    block_size = self.get_block_size()
    
    if self.background:
        self.background.render(screen, block_size)
    
    if self.item:
        self.item.render(screen, block_size)
    
    if self.platform:
        self.platform.render(screen, block_size)
    
    if self.player:
        self.player.render(screen, block_size)
```

O jogador escolhe qual animação mostrar com base em seu estado atual:

```python
# Em Player.render
def render(self, screen, block_size):
    for tile in self.tiles:
        if self.state == tile.animation_name:
            sprite_to_draw = tile.sprites[tile.current_frame]
            
            if self.face_direction == "left":
                sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
                
            screen.blit(
                sprite_to_draw,
                (self.x * block_size[0], self.y * block_size[1]),
            )
```

Este método:
1. Encontra o tile com a animação correspondente ao estado atual (mesmo nome)
2. Espelha o sprite se o jogador estiver virado para a esquerda
3. Desenha o sprite na posição atual do jogador

## Ajustando a Física do Jogo

Os parâmetros de física no 2Do podem ser facilmente ajustados para criar diferentes sensações de jogo:

```python
# Movimento horizontal
self.max_velocity = 12.0     # Velocidade máxima de corrida
self.acceleration = 1.0      # Quão rápido o jogador acelera
self.deceleration = 8.0      # Quão rápido o jogador desacelera

# Movimento vertical
self.jump_acceleration = -24.0  # Força do salto (negativo para cima)
self.gravity = 35               # Força da gravidade
self.jump_time_max = 0.2        # Duração máxima do salto
```

Modificando estes valores, você pode criar diversas "sensações" para o jogo:
- Aumentar `max_velocity` e reduzir `acceleration` cria um personagem que demora para atingir velocidade máxima
- Aumentar `gravity` e `jump_acceleration` cria saltos mais curtos e rápidos
- Reduzir `gravity` e `jump_acceleration` cria saltos mais altos e flutuantes
- Aumentar `jump_time_max` permite ao jogador controlar mais a altura do salto

## Próximos Passos

Agora que você compreende a lógica central do 2Do, pode explorar:

- [Sistema de Entrada e Controle](controle.md) - Como personalizar controles e processar entrada
- [Plano de Fundo e Interface](plano_fundo.md) - Como o plano de fundo é gerenciado
- [Utilitários e Configuração](utils.md) - Funções auxiliares e opções de configuração