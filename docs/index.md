
# 2Do - Motor de Jogos 2D

---

## Visão Geral

O **2Do** é um motor gráfico (engine) para desenvolvimento de jogos de plataforma 2D, escrito em **Python** e criado por **Lucas Lattari** para fins educacionais. Projetado com foco em **simplicidade** e **extensibilidade**, o 2Do oferece uma abordagem modular e intuitiva para a criação de jogos de plataforma.

O framework está sendo desenvolvido com ênfase em **boas práticas de programação** e **arquitetura limpa**, tornando-o ideal tanto para iniciantes que desejam aprender sobre desenvolvimento de jogos quanto para desenvolvedores experientes que buscam uma base sólida para seus projetos. Com suporte nativo a recursos como **animações baseadas em sprites**, **sistema de física para plataformas** e **integração com o formato TMX do Tiled Map Editor**, o 2Do almeja simplificar o processo de criação de jogos 2D, mantendo a flexibilidade para personalização.

---

## Arquitetura

O 2Do segue uma **arquitetura modular** com componentes bem definidos:

- **Asset Manager**: Centraliza o carregamento e gerenciamento de recursos do jogo, como sprites, tiles e mapas.
- **Entity System**: Fornece a base para todos os objetos do jogo, como personagens, itens e plataformas.
- **Input Handler**: Gerencia a entrada do usuário de forma configurável, permitindo mapear teclas para ações específicas.
- **Physics System**: Implementa colisões e movimentação para jogos de plataforma, incluindo gravidade e detecção de colisões.
- **Background Manager**: Controla elementos de plano de fundo, como rolagem em paralaxe e camadas de fundo.
- **Configuration System**: Permite personalização do jogo via arquivos `.ini`, como resolução, volume de áudio e controles.

---

## Funcionalidades Principais

- **Sistema de Física para Jogos de Plataforma**:
  - Implementa **gravidade**, **colisões** e **movimentação** dos personagens.
  - Suporta **plataformas atravessáveis**, permitindo que o jogador passe por certas plataformas ao pular ou cair.

---

- **Gerenciamento de Assets Baseado em Tiles**:
  - Organiza e carrega recursos gráficos usando mapas no formato **TMX** (Tiled Map Editor).
  - Facilita a criação de níveis com tilesets e camadas.

---

- **Sistema de Animação por Sprites**:
  - Suporta animações fluidas para personagens e objetos, com controle de frames e durações.

---

- **Colisões Precisas**:
  - Detecta e gerencia colisões entre diferentes entidades do jogo, como personagens, plataformas e itens.

---

- **Parallax Scrolling para Planos de Fundo**:
  - Cria uma sensação de profundidade movendo camadas de fundo a diferentes velocidades.

---

- **Sistema de Configuração Flexível**:
  - Permite personalizar configurações de jogo através de arquivos `.ini`, como resolução, volume de áudio e controles.

---

- **Controles Personalizáveis**:
  - Mapeia entradas de teclado conforme a preferência do usuário, com suporte a teclas configuráveis.

---

- **Suporte a Tela Cheia**:
  - Alterna entre modos de tela cheia e janela com um simples comando.

---

- **Sistema de Logging Integrado**:
  - Facilita o rastreamento e depuração durante o desenvolvimento, com logs detalhados.

---

## Tecnologias Utilizadas

O 2Do é construído utilizando as seguintes tecnologias:

- **[Python](https://www.python.org/)**: Linguagem de programação base do projeto, conhecida por sua simplicidade e legibilidade.
- **[Pygame](https://www.pygame.org/news)**: Framework para desenvolvimento de jogos 2D, fornecendo ferramentas para gráficos, som e entrada de usuário.
- **[PyTMX](https://github.com/bitcraft/PyTMX)**: Biblioteca para carregamento e manipulação de mapas no formato TMX, criado pelo Tiled Map Editor.
- **[ConfigParser](https://docs.python.org/3/library/configparser.html)**: Módulo para leitura e gerenciamento de arquivos de configuração `.ini`.

---

## Requisitos do Sistema

Para executar o 2Do, você precisará:

1. **Python 3.x** instalado.
2. **Dependências** listadas em `requirements.txt`:
   ```plaintext
   pygame==2.3.0
   PyTMX==3.31
   autopep8==2.0.2
   pycodestyle==2.10.0
   tomli==2.0.1
   ```

---

## Começando

### Instalação

1. Clone o repositório:
   ```bash
   git clone [URL_DO_REPOSITORIO]
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

### Executando o Projeto

1. Navegue até o diretório do projeto:
   ```bash
   cd 2Do
   ```

2. Execute o arquivo principal:
   ```bash
   python main.py
   ```

---

## Próximos Passos

Para começar a desenvolver com o 2Do, recomenda-se seguir esta documentação na ordem:

1. **Configuração e Setup**: Como configurar o ambiente de desenvolvimento.
2. **Estrutura Geral do Projeto**: Entenda a organização dos arquivos e diretórios.
3. **Sistema de Gerenciamento de Recursos**: Aprenda a carregar e gerenciar assets.
4. **Entidades e Objetos do Jogo**: Como criar e manipular personagens, itens e plataformas.

---

## Contribuições

Contribuições são bem-vindas! Por favor, sinta-se à vontade para:

- **Abrir uma issue** para reportar bugs.
- **Propor novas funcionalidades**.
- **Enviar pull requests**.
- **Melhorar a documentação**.

---

## Contato

**Lucas Lattari**  
📧 Email: [lucas.lattari@ifsudestemg.edu.br](mailto:lucas.lattari@ifsudestemg.edu.br)  
🐱 GitHub: [@lucaslattari](https://github.com/lucaslattari)

---

## Agradecimentos

Agradecimentos especiais a todos que contribuíram com o projeto, seja através de código, sugestões ou reportando problemas. Um agradecimento especial ao time de desenvolvimento do **Pygame** e **PyTMX** por fornecerem ferramentas que tornaram este projeto possível.
