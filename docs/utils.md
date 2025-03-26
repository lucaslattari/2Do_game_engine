# Utilitários e Funções Auxiliares

Este documento descreve as funções utilitárias que dão suporte ao 2Do, encontradas no arquivo `utils.py`. Estas funções realizam tarefas auxiliares que, embora não façam parte da lógica central do jogo, são essenciais para seu funcionamento adequado.

## Visão Geral

As funções utilitárias no 2Do servem para:

1. Carregar e processar configurações
2. Fornecer ferramentas de depuração e monitoramento de desempenho
3. Simplificar operações comuns e repetitivas
4. Aumentar a legibilidade do código principal

O arquivo `utils.py` centraliza estas funções, mantendo o restante do código limpo e focado em suas responsabilidades específicas.

## Carregamento de Configurações

### A Função read_config_file

```python
def read_config_file(config_path):
    """
    Carrega configurações a partir de um arquivo .ini
    
    Args:
        config_path (str): Caminho para o arquivo de configuração
        
    Returns:
        configparser.ConfigParser: Parser com as configurações carregadas
    """
    config_parser = configparser.ConfigParser()
    
    if os.path.exists(config_path):
        try:
            config_parser.read(config_path)
            print(f"Configurações carregadas de {config_path}")
        except Exception as e:
            print(f"Erro ao ler o arquivo de configuração: {e}")
            print("Usando configurações padrão")
    else:
        print(f"Arquivo de configuração {config_path} não encontrado")
        print("Usando configurações padrão")
        
    return config_parser
```

Esta função é responsável por carregar o arquivo de configuração que personaliza diversos aspectos do 2Do, como gráficos, áudio e comportamento do plano de fundo.

#### Como Funciona

1. **Criação do parser**: Inicializa um objeto `ConfigParser` do módulo `configparser` padrão do Python
2. **Verificação de existência**: Verifica se o arquivo de configuração existe no caminho especificado
3. **Tentativa de leitura**: Se o arquivo existir, tenta carregá-lo
4. **Tratamento de erros**: Caso haja problemas ao ler o arquivo, informa o usuário e usa configurações padrão
5. **Retorno do parser**: Retorna o objeto parser que contém as configurações carregadas

#### Uso no Código Principal

No arquivo `main.py`, esta função é chamada no início do programa:

```python
def main():
    pygame.init()
    pygame.font.init()
    
    config_parser = read_config_file("config.ini")
    
    game = Game(config_parser=config_parser)
    game.load_screen()
    game.load_level("maps/level1.tmx")
    
    # ... resto do código
```

O `config_parser` retornado é então passado para a classe `Game`, que usa as configurações para inicializar diversos componentes, como a tela, o plano de fundo e as entidades.

#### Estrutura do Arquivo de Configuração

O arquivo `config.ini` geralmente contém seções como:

```ini
[graphics]
resolution = 1280x720
fullscreen = no

[audio]
volume = 80

[background]
image = graphics/Background/Brown.png
x_block_bounds = 12,62
y_block_bounds = 10,37
scroll_speed = 0.6
```

Cada seção agrupa configurações relacionadas, facilitando a organização e leitura.

#### Valores Padrão e Fallbacks

Quando as configurações são utilizadas em outras partes do código, valores padrão (fallbacks) são especificados para garantir que o jogo funcione mesmo que certas configurações estejam ausentes:

```python
# Exemplo de uso com fallback em game.py
resolution_str = self.config_parser.get("graphics", "resolution", fallback="1280x720")
self.width, self.height = map(int, resolution_str.split("x"))
```

Isto torna o sistema robusto, pois mesmo que o arquivo de configuração esteja incompleto ou ausente, o jogo ainda terá valores razoáveis para trabalhar.

## Monitoramento de Desempenho

### A Função render_fps

```python
def render_fps(fps, screen, font, color=(255, 255, 255), position=(10, 10)):
    """
    Renderiza a taxa de quadros atual na tela
    
    Args:
        fps (float): Taxa de quadros atual
        screen (pygame.Surface): Superfície onde o texto será renderizado
        font (pygame.font.Font): Fonte a ser usada
        color (tuple): Cor do texto (R, G, B)
        position (tuple): Posição do texto na tela (x, y)
    """
    fps_text = font.render(f"FPS: {int(fps)}", True, color)
    screen.blit(fps_text, position)
```

Esta função exibe a taxa de quadros por segundo (FPS) atual na tela, uma informação crucial para monitorar o desempenho do jogo durante o desenvolvimento.

#### Como Funciona

1. **Renderização de texto**: Converte o valor de FPS em texto usando a fonte fornecida
2. **Desenho na tela**: Desenha o texto renderizado na posição especificada

#### Uso no Ciclo Principal

No arquivo `main.py`, esta função é chamada a cada iteração do ciclo principal:

```python
def main():
    # ... código anterior
    
    # Inicialização da fonte para o FPS
    font = pygame.font.SysFont("Arial", 24)
    
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        # ... atualização e renderização do jogo
        
        render_fps(clock.get_fps(), game.screen, font)
        
        pygame.display.update()
```

#### Customização da Exibição

A função aceita parâmetros para personalizar a aparência do contador de FPS:

- **color**: Define a cor do texto (padrão: branco)
- **position**: Define a posição do texto na tela (padrão: canto superior esquerdo)

## Outras Funções Utilitárias Comuns

Além das funções principais descritas acima, o arquivo `utils.py` contém outras funções auxiliares que simplificam tarefas comuns em jogos 2D.

### Cálculo de Distância

```python
def distance(point1, point2):
    """
    Calcula a distância euclidiana entre dois pontos
    
    Args:
        point1 (tuple): Coordenadas (x, y) do primeiro ponto
        point2 (tuple): Coordenadas (x, y) do segundo ponto
        
    Returns:
        float: Distância entre os pontos
    """
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
```

Esta função calcula a distância entre dois pontos no plano, útil para verificar proximidade entre entidades.

### Conversão de Coordenadas

```python
def world_to_screen(x, y, camera_x, camera_y, block_size):
    """
    Converte coordenadas do mundo para coordenadas da tela
    
    Args:
        x (float): Coordenada X no mundo
        y (float): Coordenada Y no mundo
        camera_x (float): Posição X da câmera
        camera_y (float): Posição Y da câmera
        block_size (tuple): Tamanho do bloco (width, height)
        
    Returns:
        tuple: Coordenadas (x, y) na tela
    """
    screen_x = (x - camera_x) * block_size[0]
    screen_y = (y - camera_y) * block_size[1]
    return (screen_x, screen_y)
```

Esta função converte coordenadas do mundo do jogo para coordenadas da tela, essencial para renderização correta.

### Conversão de Tempo

```python
def format_time(milliseconds):
    """
    Formata um valor em milissegundos para um formato legível (MM:SS.mmm)
    
    Args:
        milliseconds (int): Tempo em milissegundos
        
    Returns:
        str: Tempo formatado
    """
    seconds = milliseconds / 1000
    minutes = int(seconds / 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:05.2f}"
```

Esta função converte um tempo em milissegundos para um formato legível de minutos e segundos, útil para temporizadores de jogo.

## Integração com o Restante do Motor

As funções utilitárias são integradas ao restante do motor de formas diversas:

### No Arquivo Principal (main.py)

```python
def main():
    # Inicialização
    pygame.init()
    pygame.font.init()
    
    # Carrega configurações
    config_parser = read_config_file("config.ini")
    
    # Inicializa o jogo
    game = Game(config_parser=config_parser)
    game.load_screen()
    game.load_level("maps/level1.tmx")
    
    # Configuração da interface
    font = pygame.font.SysFont("Arial", 24)
    input_handler = InputHandler(config_parser)
    
    # Inicialização do relógio
    clock = pygame.time.Clock()
    running = True
    game_time = 0
    
    # Ciclo principal
    while running:
        # Calcula o delta time
        delta_time = clock.tick(60) / 1000.0
        game_time += delta_time * 1000  # Converte para milissegundos
        
        # Processa eventos
        input_handler.process_events()
        if input_handler.quit_game:
            running = False
        
        # Atualiza o jogo
        game.update(delta_time, input_handler)
        
        # Limpa a tela
        game.screen.fill((0, 0, 0))
        
        # Renderiza o jogo
        game.render(game.screen)
        
        # Renderiza informações de depuração
        render_fps(clock.get_fps(), game.screen, font)
        time_text = font.render(f"Tempo: {format_time(game_time)}", True, (255, 255, 255))
        game.screen.blit(time_text, (10, 40))
        
        # Atualiza a tela
        pygame.display.update()
```

Este exemplo expandido mostra como várias funções utilitárias trabalham juntas no ciclo principal do jogo.

## Extendendo as Funções Utilitárias

O sistema de utilitários do 2Do é projetado para ser facilmente expandido. Você pode adicionar suas próprias funções auxiliares ao arquivo `utils.py` para atender às necessidades específicas do seu jogo.

### Exemplos de Extensões Úteis

#### Salvamento Automático de Configurações

```python
def save_config_file(config_parser, config_path):
    """
    Salva as configurações atuais em um arquivo .ini
    
    Args:
        config_parser (configparser.ConfigParser): Parser com as configurações
        config_path (str): Caminho para o arquivo de configuração
    """
    try:
        with open(config_path, 'w') as config_file:
            config_parser.write(config_file)
        print(f"Configurações salvas em {config_path}")
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
```

Esta função permite salvar as configurações atuais, útil para preservar as preferências do jogador.

#### Carregamento de Recursos Genéricos

```python
def load_image(path, convert_alpha=True):
    """
    Carrega uma imagem com tratamento de erros
    
    Args:
        path (str): Caminho para o arquivo de imagem
        convert_alpha (bool): Se deve converter a imagem para formato com transparência
        
    Returns:
        pygame.Surface: Imagem carregada ou None se falhar
    """
    try:
        if convert_alpha:
            return pygame.image.load(path).convert_alpha()
        else:
            return pygame.image.load(path).convert()
    except Exception as e:
        print(f"Erro ao carregar imagem {path}: {e}")
        return None
```

Esta função padroniza o carregamento de imagens com tratamento adequado de erros.

## Próximos Passos

Agora que você compreende as funções utilitárias do 2Do, pode explorar:

- [Lógica de Jogo e Jogador](logica_jogo.md) - Como a lógica central do jogo utiliza estes utilitários
- [Configuração e Setup](executando.md) - Mais detalhes sobre o sistema de configuração
- [Plano de Fundo e Interface](plano_fundo.md) - Como o sistema de fundo usa as utilidades