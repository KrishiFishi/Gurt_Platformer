import pygame

level_1 = [
    "                                    ",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "G                                  W",
    "G                                  W",
    "G                                  W",
    "G            XXXXXXX               W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW       W",
    " W                         W      LW",
    " W                         W      LW",
    " W                         W      WW",
    " W                         W      WW",
    " W                                WW",
    " W                                WW",
    " W                                WW",
    " W                         W      LW",
    " W                         W      LW",
    " W                    W    W      LW",
    " W                    W    W      LW",
    " W               W    W    W      LW",
    " W         X     WXXXXWXXXXWXXXXXXXW",
    " WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

level_2 = [
    "                                    ",
    " WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    " WR                                W",
    " WR                        R       W",
    " WR                        R       W",
    " WR          X             R       W",
    " WR L    W       W         WWWWWWWWW",
    " WR L                              W",
    " WR LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXW",
    " WR WW                             W",
    " WR WW            V                W",
    " WR      W                         W",
    " WR      W                         W",
    " WR    LXW        W                W",
    " WVWXXXWWWWWWWXXXXWXXXXXXXXXXXX    W",
    "WWWWWW        WWWW                 W",
    "G         W   VVVV                 W",
    "G         W                        W",
    "WXXXXX    W   XXXXWWWWWWWWWR       W",
    " WWWWWXXXXXXXXWWWWWWWWWWWWWXXXXXXXXW",
    " WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

level_list = [level_1, level_2]

class LevelManager:
    def __init__(self, player_size):
        self.sprite_block = pygame.image.load('data/images/square_white.png').convert()
        self.sprite_block = pygame.transform.scale(self.sprite_block, (32, 32))

        self.sprite_spike_up = pygame.image.load('data/images/spike.png').convert()
        self.sprite_spike_up = pygame.transform.scale(self.sprite_spike_up, (player_size[0], player_size[1]))

        self.sprite_spike_down = pygame.image.load('data/images/spike.png').convert()
        self.sprite_spike_down = pygame.transform.scale(self.sprite_spike_down, (player_size[0], player_size[1]))
        self.sprite_spike_down = pygame.transform.rotate(self.sprite_spike_down, 180)

        self.sprite_spike_right = pygame.image.load('data/images/spike.png').convert()
        self.sprite_spike_right = pygame.transform.scale(self.sprite_spike_right, (player_size[0], player_size[1]))
        self.sprite_spike_right = pygame.transform.rotate(self.sprite_spike_right, 270)

        self.sprite_spike_left = pygame.image.load('data/images/spike.png').convert()
        self.sprite_spike_left = pygame.transform.scale(self.sprite_spike_left, (player_size[0], player_size[1]))
        self.sprite_spike_left = pygame.transform.rotate(self.sprite_spike_left, 90)

        self.block_hitboxes = []
        self.spike_up_hitboxes = []
        self.spike_down_hitboxes = []
        self.spike_right_hitboxes = []
        self.spike_left_hitboxes = []
        self.goal_hitboxes = []

        self.level_creation(level_1)

    def level_creation(self, map_grid):
        self.block_hitboxes.clear()
        self.spike_up_hitboxes.clear()
        self.spike_down_hitboxes.clear()
        self.spike_right_hitboxes.clear()
        self.spike_left_hitboxes.clear()
        self.goal_hitboxes.clear()

        hitbox_size = 28
        offset = (32 - hitbox_size) // 2

        for row_index, row in enumerate(map_grid):
            for col_index, char in enumerate(row):
                x = col_index * 32
                y = row_index * 32

                if char == "W":
                    tile = pygame.Rect(x, y, 32, 32)
                    self.block_hitboxes.append(tile)
                elif char == "X":
                    spike = pygame.Rect(x + offset, y + 4, hitbox_size, hitbox_size)
                    self.spike_up_hitboxes.append(spike)
                elif char == "V":
                    spike = pygame.Rect(x + offset, y, hitbox_size, hitbox_size)
                    self.spike_down_hitboxes.append(spike)
                elif char == "R":
                    spike = pygame.Rect(x, y + offset, hitbox_size, hitbox_size)
                    self.spike_right_hitboxes.append(spike)
                elif char == "L":
                    spike = pygame.Rect(x + 4, y + offset, hitbox_size, hitbox_size)
                    self.spike_left_hitboxes.append(spike)
                elif char == "G":
                    tile = pygame.Rect(x, y, 32, 32)
                    self.goal_hitboxes.append(tile)

    def draw(self, screen):
        for block in self.block_hitboxes:
            screen.blit(self.sprite_block, (block.x, block.y))
        for spike in self.spike_up_hitboxes:
            screen.blit(self.sprite_spike_up, (spike.x - 2, spike.y - 4))
        for spike in self.spike_down_hitboxes:
            screen.blit(self.sprite_spike_down, (spike.x - 2, spike.y))
        for spike in self.spike_right_hitboxes:
            screen.blit(self.sprite_spike_right, (spike.x, spike.y - 2))
        for spike in self.spike_left_hitboxes:
            screen.blit(self.sprite_spike_left, (spike.x - 4, spike.y - 2))