import pygame


class InputHandler:
    def __init__(self):
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

            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                key_action = self.key_map.get(event.key)

                if key_action:
                    self.key_state[key_action] = event.type == pygame.KEYDOWN

    def is_pressed(self, action):
        return self.key_state.get(action, False)


"""
pygame.init()
input_handler = InputHandler()

while True:
    input_handler.update()

    if input_handler.is_pressed("up"):
        print("Moving Up!")
    if input_handler.is_pressed("down"):
        print("Moving Down!")
    if input_handler.is_pressed("left"):
        print("Moving Left!")
    if input_handler.is_pressed("right"):
        print("Moving Right!")
    if input_handler.is_pressed("jump"):
        print("Jumping!")
"""
