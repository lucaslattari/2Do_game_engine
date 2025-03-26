# Executando o 2Do

Este guia explica como configurar o ambiente de desenvolvimento, executar o jogo e entender o fluxo básico de funcionamento do 2Do.

## Pré-requisitos

Antes de executar o 2Do, certifique-se de que seu sistema atende aos seguintes requisitos:

- **Python 3.8 ou superior**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Dependências do Projeto**: Instale as bibliotecas necessárias listadas no arquivo `requirements.txt`.

## Configurando o Ambiente

### 1. Clonar o Repositório

Para começar, clone o repositório do 2Do para o seu ambiente local:

```bash
git clone https://github.com/seu-usuario/2Do.git
cd 2Do
```

### 2. Instalar Dependências

Instale as dependências do projeto usando o `pip`:

```bash
pip install -r requirements.txt
```

Isso garantirá que todas as bibliotecas necessárias, como Pygame e PyTMX, estejam instaladas.

## Executando o Jogo

### 1. Iniciar o Jogo

Para executar o jogo, navegue até o diretório do projeto e execute o arquivo `main.py`:

```bash
python main.py
```

Isso iniciará o jogo e exibirá a tela inicial.

### 2. Controles do Jogo

O jogo utiliza os seguintes controles padrão:

- **Movimentação**:
  - **Setas direcionais** ou **WASD**: Movimentar o personagem.
  - **Espaço**: Pular.
- **Tela Cheia**:
  - **F11**: Alternar entre tela cheia e modo janela.
- **Sair do Jogo**:
  - **ESC**: Fechar o jogo.

### 3. Configurações Personalizadas

Você pode personalizar os controles e outras configurações editando o arquivo `config.ini`. Para mais detalhes, consulte o guia [Configuração do Jogo](configuracao.md).

## Fluxo de Execução

O fluxo básico de execução do 2Do é o seguinte:

1. **Inicialização**:
   - O jogo carrega o arquivo de configuração (`config.ini`) e inicializa o Pygame.
   - O `AssetManager` carrega os recursos do jogo, como sprites, tiles e mapas.

2. **Carregamento do Nível**:
   - O jogo carrega o nível a partir de um arquivo TMX (gerado pelo Tiled Map Editor).
   - As entidades do jogo (player, itens, plataformas) são inicializadas.

3. **Loop Principal**:
   - O `InputHandler` processa a entrada do usuário.
   - O `Game` atualiza o estado do jogo (física, colisões, animações).
   - O `Background` atualiza e renderiza o plano de fundo.
   - Todas as entidades são renderizadas na tela.

4. **Finalização**:
   - Quando o jogo é encerrado, o Pygame é finalizado e os recursos são liberados.

## Solução de Problemas

### 1. Erro ao Executar o Jogo

Se o jogo não iniciar, verifique se todas as dependências foram instaladas corretamente. Execute o seguinte comando para garantir:

```bash
pip install -r requirements.txt
```

### 2. Problemas com Assets

Se os assets (sprites, tiles, etc.) não forem carregados corretamente, verifique se os caminhos no arquivo `config.ini` estão corretos e se os arquivos existem no diretório especificado.

### 3. Erros de Renderização

Se houver problemas de renderização, como telas em branco ou elementos faltando, verifique se o arquivo TMX do nível está configurado corretamente e se todas as camadas estão visíveis.

## Próximos Passos

Agora que você sabe como executar o 2Do, explore outros tópicos da documentação para aprofundar seu conhecimento:

- [Gerenciamento de Assets](assets.md)
- [Controles do Jogo](controle.md)
- [Entidades do Jogo](entidades.md)