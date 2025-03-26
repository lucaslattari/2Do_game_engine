# Sistema de Entrada e Controle

Este documento explica como o 2Do gerencia a entrada do usuário, processa eventos de teclado e mapeia teclas para ações no jogo. O sistema de controle é centralizado na classe `InputHandler`, que fornece uma camada de abstração entre o hardware (teclado) e a lógica do jogo.

## Visão Geral do Sistema de Controle

O 2Do implementa um sistema de controle baseado em mapeamento de teclas para ações, permitindo:

1. Configuração flexível de controles através do arquivo `config.ini`
2. Processamento centralizado de eventos de teclado
3. Verificação simplificada do estado de teclas durante a atualização do jogo
4. Suporte a teclas globais como ESC (sair) e F11 (alternar tela cheia)

A arquitetura do sistema separa claramente a entrada de dados da lógica de jogo, facilitando personalizações e extensões.

## A Classe InputHandler

O arquivo `input_handler.py` contém a classe `InputHandler`, responsável por todo o processamento de entrada do usuário:

```python
class InputHandler:
    def __init__(self, config_parser):
        self.quit_game = False
        self.fullscreen_toggled = False

        # Carregar as teclas de controle do arquivo de configuração
        self.key_map = {}
        self.key_state = {}
        if config_parser.has_section("controls"):
            for action, key_name in config_parser.items("controls"):
                try:
                    key_constant = getattr(pygame, key_name)
                    self.key_map[key_constant] = action
                    self.key_state[action] = False
                except AttributeError:
                    print(f"Tecla inválida no arquivo de configuração: {key_name}")
        else:
            # Valores padrão caso a seção 'controls' não exista
            self.key_map = {
                pygame.K_UP: "up",
                pygame.K_DOWN: "down",
                pygame.K_LEFT: "left",
                pygame.K_RIGHT: "right",
                pygame.K_SPACE: "jump",
                pygame.K_a: "left",
                pygame.K_d: "right",
                pygame.K_w: "up",
                pygame.K_s: "down",
            }
            self.key_state = {action: False for action in self.key_map.values()}
```

O construtor da classe realiza as seguintes tarefas:
1. Inicializa flags de controle (`quit_game`, `fullscreen_toggled`)
2. Tenta carregar mapeamentos de teclas do arquivo de configuração
3. Se a configuração não for encontrada, configura mapeamentos padrão que incluem tanto as setas direcionais quanto WASD
4. Inicializa o estado de cada ação (pressionada ou não)

## Configuração de Controles

O 2Do permite dois métodos para configurar os controles do jogo:

### 1. Através do Arquivo config.ini

Você pode adicionar uma seção `[controls]` ao arquivo `config.ini` para personalizar as teclas:

```ini
[controls]
up = K_UP
down = K_DOWN
left = K_LEFT
right = K_RIGHT
jump = K_SPACE
```

Cada linha mapeia uma ação (como "up" ou "jump") para uma constante de tecla do Pygame (como "K_UP" ou "K_SPACE").

**Importante:** Se você definir controles personalizados no `config.ini`, apenas os controles especificados estarão disponíveis. O suporte automático a WASD não é incluído neste caso, a menos que você adicione explicitamente essas teclas à configuração.

### 2. Controles Padrão

Se o arquivo `config.ini` não contiver uma seção `[controls]`, o sistema ativa automaticamente um conjunto padrão de mapeamentos:

- **Setas direcionais**: Movimentação (cima, baixo, esquerda, direita)
- **WASD**: Controles alternativos para movimentação (W=cima, A=esquerda, S=baixo, D=direita)
- **Barra de espaço**: Pular

Esta configuração padrão é amigável para jogadores destros e canhotos, oferecendo duas opções comuns para controle de movimento sem necessidade de configuração adicional.

## Processamento de Eventos

O método `process_events` é o coração do sistema de controle, processando a fila de eventos do Pygame a cada quadro:

```python
def process_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.quit_game = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit_game = True
            elif event.key == pygame.K_F11:
                self.fullscreen_toggled = True

            key_action = self.key_map.get(event.key)
            if key_action:
                self.key_state[key_action] = True

        elif event.type == pygame.KEYUP:
            key_action = self.key_map.get(event.key)
            if key_action:
                self.key_state[key_action] = False
```

Este método:
1. Itera por todos os eventos pendentes no Pygame
2. Processa eventos de saída (fechar janela)
3. Verifica teclas especiais (ESC para sair, F11 para tela cheia)
4. Atualiza o estado de ações mapeadas conforme teclas são pressionadas ou liberadas

## Verificação de Estado de Teclas

A classe fornece um método simples para verificar se uma ação está ativa:

```python
def is_pressed(self, action):
    return self.key_state.get(action, False)
```

Este método é usado em todo o código do jogo para verificar entradas do usuário, como no trecho de `player.py`:

```python
# Exemplo de uso em Player.update_state_and_velocity
if input_handler.is_pressed("left"):
    self.face_direction = "left"
    if self.on_ground:
        self.state = "run"
    self.velocity = max(-self.max_velocity, self.velocity - self.acceleration)
```

A abordagem baseada em ações (em vez de teclas específicas) torna o código mais limpo e facilita a personalização dos controles sem modificar a lógica do jogo.

## Controle de Modo de Tela

O `InputHandler` também gerencia a alternância entre tela cheia e modo janela:

```python
def reset_toggle_fullscreen(self):
    self.fullscreen_toggled = False
```

Quando a tecla F11 é pressionada, a flag `fullscreen_toggled` é definida. A classe `Game` verifica esta flag durante sua atualização:

```python
# Em Game.update
if input_handler.fullscreen_toggled:
    self.toggle_fullscreen()
    input_handler.reset_toggle_fullscreen()
```

Este padrão evita que a mesma tecla F11 alterne o modo repetidamente em um único pressionamento.

## Ações Suportadas

O 2Do atualmente suporta as seguintes ações de jogo:

| Ação   | Descrição                                  | Teclas Padrão (sem configuração personalizada) |
|--------|--------------------------------------------|-----------------------------|
| `up`   | Mover para cima / Pular                    | Seta para cima, W           |
| `down` | Mover para baixo / Descer por plataformas  | Seta para baixo, S          |
| `left` | Mover para a esquerda                      | Seta para a esquerda, A     |
| `right`| Mover para a direita                       | Seta para a direita, D      |
| `jump` | Pular (alias para `up` em alguns contextos)| Barra de espaço             |

Além disso, as seguintes teclas globais são sempre processadas independentemente da configuração:

| Tecla | Função                     |
|-------|----------------------------|
| `ESC` | Sair do jogo               |
| `F11` | Alternar modo tela cheia   |

## Expandindo o Sistema de Controle

O sistema de controle foi projetado para ser facilmente extensível. Aqui estão algumas maneiras de expandir sua funcionalidade:

### 1. Adicionar Novas Ações

Para adicionar uma nova ação (como "atacar" ou "usar item"):

1. Adicione a nova ação ao arquivo `config.ini`:
   ```ini
   [controls]
   up = K_UP
   down = K_DOWN
   left = K_LEFT
   right = K_RIGHT
   jump = K_SPACE
   attack = K_LCTRL
   ```

2. Verifique a nova ação em seu código:
   ```python
   if input_handler.is_pressed("attack"):
       player.attack()
   ```

### 2. Suporte a Controles Alternativos

Você pode adicionar controles alternativos usando nomes de ação com sufixos diferentes:

```ini
[controls]
up = K_UP
up_alt = K_w
down = K_DOWN
down_alt = K_s
left = K_LEFT
left_alt = K_a
right = K_RIGHT
right_alt = K_d
jump = K_SPACE
```

Em seguida, verifique as ações no código como faria normalmente:
```python
if input_handler.is_pressed("up"):
    # Lógica para movimento para cima (acionado por seta para cima OU tecla W)
```

O sistema de mapeamento de teclas garante que quaisquer teclas mapeadas para a mesma ação acionarão o mesmo comportamento.

### 3. Suporte a Gamepad

Uma extensão natural seria adicionar suporte a gamepad, estendendo o `InputHandler` para processar eventos de joystick do Pygame.

## Próximos Passos

Agora que você compreende o sistema de controle do 2Do, pode explorar:

- [Lógica de Jogo e Jogador](logica_jogo.md) - Como o jogador responde às entradas do usuário
- [Utilitários e Configuração](utils.md) - Mais opções de configuração disponíveis
- [Plano de Fundo e Interface](plano_fundo.md) - Como a interface do jogo é renderizada