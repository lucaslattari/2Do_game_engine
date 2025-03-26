# Estrutura do Projeto 2Do

Este documento apresenta a estrutura de diretórios e arquivos do projeto, explicando a função de cada componente e como eles se integram para formar o motor de jogos de plataforma 2D.

## Visão Geral da Estrutura

O 2Do é organizado seguindo um design modular, onde cada arquivo tem uma responsabilidade específica. Esta abordagem facilita a manutenção e expansão do código. A estrutura básica do projeto é a seguinte:

```
2Do/
├── asset_manager.py       # Gerenciamento de recursos
├── background.py          # Sistema de plano de fundo
├── config.ini             # Configurações do jogo
├── entity.py              # Classes base para entidades
├── game.py                # Núcleo do motor de jogo
├── input_handler.py       # Processamento de entrada
├── item.py                # Sistema de itens 
├── main.py                # Ponto de entrada
├── platformer.py          # Sistema de plataformas
├── player.py              # Implementação do jogador
├── readme.md              # Documentação geral
├── requirements.txt       # Dependências do projeto
├── utils.py               # Funções utilitárias
├── docs/                  # Documentação detalhada
└── site/                  # Documentação compilada
```

## Componentes Principais

### Arquivos Essenciais

#### main.py
Este é o ponto de entrada do jogo. Suas principais responsabilidades são:

- Inicializar a biblioteca Pygame
- Carregar as configurações do arquivo `config.ini`
- Criar a instância do jogo e configurar a tela
- Implementar o loop principal que mantém o jogo em execução
- Gerenciar o tempo entre frames (delta)
- Finalizar o Pygame ao encerrar o jogo

```python
# Trecho de exemplo do main.py
pygame.init()
pygame.font.init()

config_parser = read_config_file("config.ini")

game = Game(config_parser=config_parser)
game.load_screen()
game.load_level("maps/level1.tmx")

# Loop principal
while running:
    delta_time = clock.tick(60) / 1000.0
    input_handler.process_events()
    game.update(delta_time, input_handler)
    game.render(game.screen)
    pygame.display.update()
```

#### game.py
A classe `Game` atua como o controlador central do motor, responsável por:

- Carregar e gerenciar os níveis do jogo (usando PyTMX)
- Coordenar a atualização e renderização de todas as entidades
- Gerenciar a tela do jogo e o modo de exibição
- Intermediar a comunicação entre os diferentes subsistemas

#### config.ini
Este arquivo de configuração em formato INI permite personalizar vários aspectos do jogo sem modificar o código:

- Configurações gráficas (resolução, modo de tela)
- Configurações de áudio
- Definições do plano de fundo
- Mapeamento de controles

### Sistemas Principais

#### asset_manager.py
O `AssetManager` é responsável por carregar e organizar todos os recursos do jogo, como sprites, tiles e mapas. Ele:

- Carrega tiles e sprites a partir de arquivos TMX (formato Tiled Map Editor)
- Organiza os recursos por tipo (Player, Item, Platform)
- Extrai propriedades dos tiles (colisão, animação)
- Fornece métodos para acessar os recursos carregados

#### entity.py
Este módulo define as classes base para todos os objetos interativos do jogo:

- `Tile`: Representa um único tile com propriedades como posição, sprites e colisão
- `Entity`: Classe base que representa objetos interativos no mundo do jogo (como personagens, plataformas e itens), gerenciando seu comportamento, estado e interações

#### player.py
Implementa o personagem controlado pelo jogador, estendendo a classe `Entity` com:

- Movimentação completa (horizontal e vertical)
- Sistema de física (gravidade, salto, queda)
- Animações baseadas no estado atual (idle, run, jump)
- Detecção de colisão com plataformas
- Capacidade de descer através de plataformas específicas

#### input_handler.py
Gerencia a entrada do usuário, abstraindo o mapeamento entre teclas físicas e ações no jogo:

- Processa eventos do Pygame (teclado, saída)
- Mapeia teclas para ações (movimento, pulo)
- Fornece métodos para verificar quais teclas estão pressionadas
- Permite alternar entre modo janela e tela cheia

#### background.py
Gerencia o plano de fundo do jogo, incluindo:

- Carregamento e ajuste de imagens de fundo
- Rolagem paralaxe (efeito de profundidade)
- Repetição (tiling) para cobrir toda a área visível

#### platformer.py e item.py
Implementam os sistemas de plataformas e itens do jogo, estendendo a classe `Entity` com comportamentos específicos para:

- Plataformas: superfícies que o jogador pode andar
- Itens: objetos coletáveis ou interativos

#### utils.py
Contém funções utilitárias usadas em vários módulos:

- Renderização de informações de depuração (FPS)
- Leitura de arquivos de configuração
- Outras funções auxiliares

## Fluxo de Execução

O fluxo típico do 2Do segue esta sequência:

1. **Inicialização** (`main.py`):
   - Inicializa o Pygame e suas dependências
   - Carrega as configurações do `config.ini`
   - Cria a instância do jogo e configura a tela

2. **Carregamento do Jogo** (`game.py`):
   - Carrega o nível usando o `AssetManager`
   - Inicializa o plano de fundo
   - Cria as entidades (jogador, plataformas, itens)

3. **Loop Principal** (`main.py`):
   - Captura o tempo entre frames (delta)
   - Processa eventos de entrada do usuário (`InputHandler`)
   - Atualiza o estado do jogo (`Game.update()`)
   - Renderiza todos os elementos na tela (`Game.render()`)
   - Atualiza a exibição

4. **Atualização de Estado** (`game.py` → vários componentes):
   - Atualiza o plano de fundo (rolagem)
   - Atualiza as plataformas e itens (animações)
   - Atualiza o jogador (física, colisões, animações)

5. **Renderização** (`game.py` → vários componentes):
   - Renderiza o plano de fundo
   - Renderiza as plataformas e itens
   - Renderiza o jogador
   - Renderiza informações de depuração (FPS)

## Dependências entre Componentes

O 2Do foi projetado com uma clara separação de responsabilidades, mas seus componentes precisam colaborar para formar um sistema coeso:

- **Dependências Verticais**:
  - `main.py` → `game.py` → entidades específicas (`player.py`, `item.py`, etc.)
  - Componentes de mais alto nível coordenam os de nível inferior

- **Dependências Horizontais**:
  - `player.py` depende de `platformer.py` para detecção de colisão
  - Todas as entidades dependem de `entity.py` para funcionalidade base
  - Vários componentes dependem de `utils.py` para funções auxiliares

- **Ponto Central**:
  - `game.py` atua como o "maestro" que coordena todos os outros componentes
  - `asset_manager.py` fornece recursos para vários componentes

Esta estrutura facilita a expansão do motor, permitindo adicionar novos tipos de entidades ou sistemas com impacto mínimo no código existente.

## Ferramentas de Desenvolvimento

- **Documentação**: O 2Do usa [MkDocs](https://www.mkdocs.org/) com o tema Material para gerar documentação a partir de arquivos Markdown
- **Estrutura de Diretórios**: 
  - `docs/`: Contém os arquivos Markdown da documentação
  - `site/`: Contém a documentação HTML gerada pelo MkDocs

## Próximos Passos

Agora que você compreende a estrutura do projeto, pode explorar:

- [Sistema de Gerenciamento de Recursos](assets.md) - Como o 2Do carrega e gerencia sprites e tiles
- [Entidades e Objetos do Jogo](entidades.md) - Detalhes sobre o sistema de entidades 
- [Sistema de Entrada e Controle](controle.md) - Como personalizar os controles do jogo
- [Lógica de Jogo e Jogador](logica_jogo.md) - Física e mecânicas do jogador