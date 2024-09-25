import pygame


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

    def update(self):
        pass  # Mantido para compatibilidade, caso precise de atualizações futuras

    def is_pressed(self, action):
        return self.key_state.get(action, False)

    def reset_toggle_fullscreen(self):
        self.fullscreen_toggled = False
