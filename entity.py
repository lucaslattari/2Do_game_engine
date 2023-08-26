class Entity:
    def __init__(self, data):
        self.parse(data)

    def parse(self, data):
        self.entities = []
        for d in data:
            entity = {}
            entity["current_frame"] = 0
            entity["timer_next_frame"] = 0.0

            entity["id"] = d["id"]
            entity["width"] = d["width"]
            entity["height"] = d["height"]
            entity["position"] = []

            for position in d["position"]:
                entity["position"].append(position)

            entity["sprites"] = d["sprites"]

            self.entities.append(entity)

    def render(self, screen, block_size):
        for entity in self.entities:
            for position in entity["position"]:
                screen.blit(
                    entity["sprites"][entity["current_frame"]],
                    (
                        position[0] * block_size[0],
                        position[1] * block_size[1],
                    ),
                )

    def update(self, delta_time):
        for entity in self.entities:
            if entity["timer_next_frame"] > delta_time:
                entity["current_frame"] = (entity["current_frame"] + 1) % len(
                    entity["sprites"]
                )
                entity["timer_next_frame"] -= delta_time
            else:
                entity["timer_next_frame"] += delta_time
