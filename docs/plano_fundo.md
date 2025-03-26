# Plano de Fundo e Parallax Scrolling

Este documento explica como o 2Do gerencia o plano de fundo dos jogos, incluindo como as imagens são carregadas, renderizadas e como o efeito de rolagem paralaxe é implementado para criar uma sensação de profundidade.

## Visão Geral

O sistema de plano de fundo do 2Do é projetado para:

1. Carregar imagens de fundo a partir de configurações
2. Criar uma camada visual que cobre toda a área do jogo
3. Implementar efeito de rolagem (paralaxe) para dar sensação de profundidade
4. Permitir fácil customização através do arquivo de configuração

A classe principal responsável por essa funcionalidade é a `Background`, localizada no arquivo `background.py`.

## A Classe Background

```python
class Background:
    def __init__(self, tiled_level, config_parser):
        self.config_parser = config_parser
        
        # Carrega a imagem de fundo
        bg_path = self.config_parser.get("background", "image", fallback="graphics/Background/Brown.png")
        self.tile_bg = pygame.image.load(bg_path).convert_alpha()
        
        # Limites de blocos para X e Y
        x_bounds = self.config_parser.get("background", "x_block_bounds", fallback="12,62")
        y_bounds = self.config_parser.get("background", "y_block_bounds", fallback="10,37")
        
        self.x_block_bounds = tuple(map(int, x_bounds.split(",")))
        self.y_block_bounds = tuple(map(int, y_bounds.split(",")))
        
        # Velocidade de rolagem (paralaxe)
        self.scroll_speed = float(self.config_parser.get("background", "scroll_speed", fallback="0.6"))
        
        # Posição inicial da câmera
        self.camera_x = 0
        self.camera_y = 0
```

Esta classe é inicializada com dois parâmetros:
- `tiled_level`: O nível carregado do arquivo TMX
- `config_parser`: O parser de configuração que contém as preferências do plano de fundo

Durante a inicialização, a classe:
1. Carrega a imagem de fundo especificada no arquivo de configuração
2. Configura os limites de blocos (quanto do fundo será renderizado)
3. Define a velocidade de rolagem para criar o efeito parallax
4. Inicializa a posição da câmera em (0,0)

## Carregamento e Configuração

### Carregamento da Imagem

O plano de fundo é carregado a partir de um arquivo de imagem especificado no `config.ini`:

```python
bg_path = self.config_parser.get("background", "image", fallback="graphics/Background/Brown.png")
self.tile_bg = pygame.image.load(bg_path).convert_alpha()
```

O método `convert_alpha()` otimiza a imagem para renderização mais rápida, preservando o canal de transparência (alpha).

### Limites de Blocos e Dimensionamento

O plano de fundo é construído repetindo (ou "tilando") uma imagem base. Os parâmetros `x_block_bounds` e `y_block_bounds` definem a área de cobertura:

```python
x_bounds = self.config_parser.get("background", "x_block_bounds", fallback="12,62")
y_bounds = self.config_parser.get("background", "y_block_bounds", fallback="10,37")

self.x_block_bounds = tuple(map(int, x_bounds.split(",")))
self.y_block_bounds = tuple(map(int, y_bounds.split(",")))
```

Por exemplo, com `x_block_bounds = 12,62` e `y_block_bounds = 10,37`:
- O plano de fundo terá 50 blocos de largura (62-12)
- O plano de fundo terá 27 blocos de altura (37-10)

**Por que esses valores são importantes?**

Imagine que cada bloco de fundo tenha dimensões de 64x64 pixels. Com os valores acima:
- A largura total do fundo seria 50 × 64 = 3200 pixels
- A altura total do fundo seria 27 × 64 = 1728 pixels

Esses valores devem ser grandes o suficiente para cobrir a área visível do jogo, mesmo durante a rolagem.

## Renderização do Plano de Fundo

A renderização do plano de fundo acontece no método `render`:

```python
def render(self, screen, block_size):
    # Calcula o tamanho total do plano de fundo
    bg_width = (self.x_block_bounds[1] - self.x_block_bounds[0]) * self.tile_bg.get_width()
    bg_height = (self.y_block_bounds[1] - self.y_block_bounds[0]) * self.tile_bg.get_height()
    
    # Calcula quantos blocos são visíveis na tela
    screen_width, screen_height = screen.get_size()
    visible_width = screen_width / block_size[0]
    visible_height = screen_height / block_size[1]
    
    # Calcula a posição da câmera aplicando o efeito parallax
    camera_x = self.camera_x * self.scroll_speed
    camera_y = self.camera_y * self.scroll_speed
    
    # Calcula a posição de início da renderização
    start_x = int(camera_x) % self.tile_bg.get_width()
    start_y = int(camera_y) % self.tile_bg.get_height()
    
    # Renderiza os blocos visíveis
    for y in range(-1, int(visible_height) + 2):
        for x in range(-1, int(visible_width) + 2):
            # Posição do bloco na tela
            draw_x = (x * self.tile_bg.get_width()) - start_x
            draw_y = (y * self.tile_bg.get_height()) - start_y
            
            # Desenha o bloco
            screen.blit(self.tile_bg, (draw_x, draw_y))
```

Este método implementa um sistema de renderização eficiente:

1. **Cálculo de dimensões**:
   - Determina o tamanho total do plano de fundo com base nos limites de blocos
   - Calcula quantos blocos são visíveis na tela atual

2. **Posicionamento da câmera com parallax**:
   - Aplica a velocidade de rolagem à posição da câmera para criar o efeito paralaxe
   - O efeito paralaxe faz com que o fundo se mova mais lentamente que os elementos do jogo

3. **Tiling eficiente**:
   - Calcula a posição inicial de desenho com base na posição da câmera
   - Renderiza apenas os blocos visíveis na tela, mais uma margem de segurança (-1 e +2)
   - Usa a operação de módulo (%) para criar um padrão de repetição infinita

4. **Desenho dos blocos**:
   - Posiciona cada bloco no local correto da tela
   - Usa `screen.blit()` para desenhar a imagem na superfície da tela

A imagem abaixo ilustra como funciona a renderização do plano de fundo por tiling:

```
+---+---+---+---+---+  
| 1 | 2 | 3 | 4 | 5 |  → Blocos de imagem repetidos horizontalmente
+---+---+---+---+---+
| 6 | 7 | 8 | 9 |10 |
+---+---+---+---+---+  → Área visível da tela
|11 |12 |13 |14 |15 |     (pode mostrar apenas uma parte do padrão)
+---+---+---+---+---+
|16 |17 |18 |19 |20 |
+---+---+---+---+---+
```

## Efeito de Rolagem (Paralaxe)

O efeito de parallax é o que dá profundidade ao jogo, fazendo com que o plano de fundo se mova mais lentamente que os elementos em primeiro plano. Isto simula o fenômeno do mundo real onde objetos distantes parecem se mover mais devagar quando nos deslocamos.

### Atualização da Posição da Câmera

```python
def update(self, player_x, player_y):
    # Atualiza a posição da câmera com base na posição do jogador
    self.camera_x = player_x - (self.x_block_bounds[1] - self.x_block_bounds[0]) / 2
    self.camera_y = player_y - (self.y_block_bounds[1] - self.y_block_bounds[0]) / 2
    
    # Limita a câmera aos limites do mundo do jogo
    self.camera_x = max(self.x_block_bounds[0], min(self.camera_x, self.x_block_bounds[1]))
    self.camera_y = max(self.y_block_bounds[0], min(self.camera_y, self.y_block_bounds[1]))
```

O método `update` é chamado a cada frame do jogo e realiza estas operações:

1. **Centraliza a câmera no jogador**:
   - Calcula a posição ideal da câmera para manter o jogador no centro da tela
   - Subtrai metade da largura/altura visível para centralizar

2. **Limita os limites da câmera**:
   - Impede que a câmera se mova além dos limites do mundo do jogo
   - Usa `max` e `min` para restringir os valores dentro dos limites definidos

### Aplicação do Efeito Paralaxe

O efeito paralaxe propriamente dito é aplicado durante a renderização:

```python
# No método render
camera_x = self.camera_x * self.scroll_speed
camera_y = self.camera_y * self.scroll_speed
```

O `scroll_speed` controla quão rapidamente o fundo se move em relação aos elementos do jogo:

- `scroll_speed = 1.0`: O fundo se move na mesma velocidade que o jogador (sem efeito parallax)
- `scroll_speed = 0.5`: O fundo se move na metade da velocidade do jogador (paralaxe moderado)
- `scroll_speed = 0.2`: O fundo se move muito mais lentamente que o jogador (paralaxe intenso)

Quanto menor o valor, mais distante o fundo parece estar, criando uma impressão de profundidade maior.

### Como o Paralaxe Cria Profundidade

Para entender como o paralaxe cria profundidade, imagine um cenário com três camadas:

1. **Jogador e plataformas** - Movem-se 1:1 com a câmera (primeiro plano)
2. **Montanhas** - Movem-se a 0.6x da velocidade da câmera (plano médio)
3. **Céu estrelado** - Move-se a 0.2x da velocidade da câmera (plano de fundo distante)

Quando o jogador se move 100 pixels para a direita:
- O jogador e as plataformas se movem 100 pixels na tela
- As montanhas se movem apenas 60 pixels (0.6 × 100)
- O céu estrelado se move apenas 20 pixels (0.2 × 100)

Este efeito imita o que vemos no mundo real: quando nos movemos, objetos próximos parecem passar mais rapidamente que objetos distantes. Dirigindo em uma estrada, as árvores próximas passam rapidamente, enquanto as montanhas distantes parecem se mover muito lentamente.

## Customização do Plano de Fundo

O sistema de plano de fundo do 2Do é altamente customizável através do arquivo `config.ini`:

```ini
[background]
image = graphics/Background/Brown.png
x_block_bounds = 12,62
y_block_bounds = 10,37
scroll_speed = 0.6
```

Você pode modificar:

1. **`image`**: Caminho para qualquer imagem PNG compatível
   - Recomenda-se usar imagens que possam ser repetidas naturalmente (tilable)
   - Imagens pequenas (64x64 ou 128x128) funcionam bem para padrões repetitivos

2. **`x_block_bounds` e `y_block_bounds`**: Define o tamanho do mundo do jogo
   - Valores maiores criam mundos mais amplos
   - Deve ser grande o suficiente para acomodar todos os elementos do jogo

3. **`scroll_speed`**: Controla o efeito de parallax
   - Valores entre 0.3 e 0.8 geralmente funcionam bem
   - Valores mais baixos criam uma sensação de maior profundidade

### Dicas para Criar Planos de Fundo Eficazes

1. **Use imagens tilable**: Imagens que se repetem naturalmente sem bordas visíveis
   - Texturas como grama, terra, céu, tijolos funcionam bem
   - Evite elementos únicos que criariam repetição óbvia

2. **Considere múltiplas camadas**: Para jogos mais complexos, pode-se implementar várias camadas
   - Céu (mais distante, scroll_speed baixo)
   - Montanhas ou nuvens (distância média, scroll_speed médio)
   - Árvores ou arbustos (mais próximo, scroll_speed mais alto)

3. **Otimize o desempenho**:
   - Use imagens de tamanho razoável (evite texturas gigantes)
   - Certifique-se de que sua imagem use `convert_alpha()` para melhor desempenho

### Exemplo: Criando um Efeito de Céu Estrelado

```ini
[background]
image = graphics/Background/NightSky.png
x_block_bounds = 10,70
y_block_bounds = 5,45
scroll_speed = 0.2
```

Com este exemplo:
- Uma imagem de céu estrelado será usada como fundo
- O mundo do jogo será grande (60 blocos de largura por 40 de altura)
- O efeito parallax será intenso (0.2), fazendo com que o céu pareça muito distante

## Conclusão

O sistema de plano de fundo do 2Do oferece uma solução simples mas eficaz para criar cenários visualmente interessantes com efeito de profundidade. Através da técnica de tiling e do efeito paralaxe, o motor consegue criar a ilusão de um mundo maior e mais profundo, mesmo com recursos gráficos limitados.

A facilidade de configuração permite que desenvolvedores personalizem rapidamente a aparência de seus jogos sem precisar modificar o código-fonte.

## Próximos Passos

Agora que você entende como funciona o sistema de plano de fundo, pode explorar:

- [Entidades e Objetos do Jogo](entidades.md) - Como objetos são posicionados neste mundo
- [Configuração e Setup](executando.md) - Mais opções de configuração para personalizar seu jogo
- [Sistema de Gerenciamento de Recursos](assets.md) - Como outros recursos gráficos são gerenciados