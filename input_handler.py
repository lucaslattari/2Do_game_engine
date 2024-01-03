import pygame


class InputHandler:
    def __init__(self):
        self.fullscreen_toggled = False

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

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_F11:
                    self.fullscreen_toggled = True

                key_action = self.key_map.get(event.key)
                if key_action:
                    self.key_state[key_action] = True

            elif event.type == pygame.KEYUP:
                key_action = self.key_map.get(event.key)
                if key_action:
                    self.key_state[key_action] = False

    def is_pressed(self, action):
        return self.key_state.get(action, False)

    def reset_toggle_fullscreen(self):
        self.fullscreen_toggled = False
