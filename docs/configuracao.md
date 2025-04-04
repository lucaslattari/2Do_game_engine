# Configuração e Setup do 2Do

Este guia apresenta como preparar o ambiente de desenvolvimento do **2Do** e entender as configurações básicas para executar o projeto. Lembre-se de que o **2Do** ainda está em desenvolvimento, então alguns recursos podem mudar ao longo do tempo.

## Requisitos de Sistema

Para executar o 2Do, você precisará de:

- **Python 3.8 ou superior** - [Download Python](https://www.python.org/downloads/)
- **Pygame 2.3.0** - Instalado automaticamente com as dependências
- **PyTMX 3.31** - Instalado automaticamente com as dependências

## Instalação

### 1. Obtendo o Código

Clone o repositório ou baixe os arquivos do projeto para o seu computador.

```bash
git clone https://github.com/seu-usuario/2do.git
cd 2do
```

### 2. Configurando o Ambiente Virtual (Recomendado)

É recomendável usar um ambiente virtual para manter as dependências isoladas:

```bash
python -m venv venv
```

Ativando o ambiente virtual:

**Windows**:
```bash
venv\Scripts\activate
```

**macOS/Linux**:
```bash
source venv/bin/activate
```

### 3. Instalando Dependências

Todas as dependências necessárias estão listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Arquivo de Configuração (config.ini)

O 2Do utiliza um arquivo de configuração no formato INI para personalizar diversos aspectos do jogo. Este arquivo é lido pelo `configparser` do Python e aplicado ao iniciar o jogo.

### Estrutura do Arquivo

O arquivo `config.ini` padrão contém as seguintes seções:

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

[controls]
up = K_UP
down = K_DOWN
left = K_LEFT
right = K_RIGHT
jump = K_SPACE
```

### Configurações Detalhadas

#### Gráficos

Na seção `[graphics]`, você pode configurar:

- **resolution**: Define a resolução da janela do jogo no formato `LARGURAxALTURA`
- **fullscreen**: Ativa (`yes`) ou desativa (`no`) o modo de tela cheia

O código em `game.py` aplica essas configurações durante a inicialização:

```python
resolution_str = self.config_parser.get("graphics", "resolution", fallback="1280x720")
self.width, self.height = map(int, resolution_str.split("x"))
```

#### Áudio

Na seção `[audio]`, você pode configurar:

- **volume**: Define o volume global do jogo (0-100)

#### Plano de Fundo

Na seção `[background]`, você pode personalizar o fundo do jogo:

- **image**: Caminho para a imagem de fundo (relativo à raiz do projeto)
- **x_block_bounds**: Limites horizontais para repetição do plano de fundo (formato `min,max`)
- **y_block_bounds**: Limites verticais para repetição do plano de fundo (formato `min,max`)
- **scroll_speed**: Velocidade de rolagem do plano de fundo (valores maiores = movimento mais rápido)

##### Entendendo os Limites de Blocos

No 2Do, o plano de fundo é construído repetindo (ou "tilando") uma imagem base. Os parâmetros `x_block_bounds` e `y_block_bounds` definem quantos blocos serão usados para criar esse fundo:

- Se um bloco tem 16x16 pixels e você define `x_block_bounds = 12,62`, o plano de fundo terá 50 blocos de largura (62-12)
- Com `y_block_bounds = 10,37`, o plano de fundo terá 27 blocos de altura (37-10)

Esses valores são utilizados na classe `Background` para criar um fundo contínuo que cobre toda a área visível do jogo:

```python
bg_width = (self.x_block_bounds[1] - self.x_block_bounds[0]) * self.tile_bg.get_width()
bg_height = (self.y_block_bounds[1] - self.y_block_bounds[0]) * self.tile_bg.get_height()
```

#### Controles

Na seção `[controls]`, você pode definir as teclas utilizadas para cada ação no jogo:

- **up**: Tecla para mover para cima/pular
- **down**: Tecla para mover para baixo/agachar
- **left**: Tecla para mover para a esquerda
- **right**: Tecla para mover para a direita
- **jump**: Tecla para pular

Os valores correspondem às constantes de tecla do Pygame (ex: `K_SPACE`, `K_UP`, etc.). 

O jogo também tem teclas globais predefinidas:
- **ESC**: Sai do jogo
- **F11**: Alterna entre tela cheia e modo janela

## Dicas para Configuração

### Otimizando o Desempenho

- Para melhor desempenho em dispositivos com recursos limitados, reduza a resolução (ex: `800x600`)
- Mantenha a velocidade de rolagem do fundo (`scroll_speed`) entre 0.3 e 0.8 para um efeito visualmente agradável

### Personalizando Visualmente

- Você pode substituir a imagem de fundo por qualquer arquivo PNG compatível
- Ajuste os limites de blocos para garantir que a área do jogo seja totalmente coberta

### Configuração de Controles

- Adicione teclas alternativas duplicando entradas com o mesmo valor de ação:
```ini
[controls]
up = K_UP
up_alt = K_w
down = K_DOWN
down_alt = K_s
# etc.
```

## Próximos Passos

Após configurar o ambiente e personalizar o arquivo `config.ini`, você pode avançar para a seção [Estrutura Geral do Projeto](estrutura_projeto.md) para entender como o 2Do é organizado, ou pular para [Arquivo Principal e Execução](executando.md) para instruções sobre como executar seu primeiro jogo com o 2Do.