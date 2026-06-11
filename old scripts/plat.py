import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("2D Platformer")
        self.screen = pygame.display.set_mode((1200,700))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]
        self.player_speed_x = 5

        self.player_pos = [100,100]
        self.player_size = [32,32]
        self.player_velocity_y = 0
        self.grounded = False

        self.block = pygame.image.load('../data/images/square_white.png').convert()
        self.block.set_colorkey((0,0,0))
        self.block = pygame.transform.scale(self.block, (32,32))

        self.floor_hitboxes = []
        self.lwall_hitboxes = []
        self.rwall_hitboxes = []
        self.roof_hitboxes = []

        # Floor
        for x in range(24, 1176, 32):
            tile = pygame.Rect(x, 622, 32, 32)
            self.floor_hitboxes.append(tile)

        # Ceiling
        for x in range(24, 1176, 32):
            tile = pygame.Rect(x, 46, 32, 32)
            self.roof_hitboxes.append(tile)

        # Left Wall
        for y in range (78, 622, 32):
            tile = pygame.Rect(24, y, 32, 32)
            self.lwall_hitboxes.append(tile)

        # Right Wall
        for y in range(78, 622, 32):
            tile = pygame.Rect(1144, y, 32, 32)
            self.rwall_hitboxes.append(tile)

    def run(self):
        while True:
            self.screen.fill((0,0,0))

            for block in self.lwall_hitboxes:
                self.screen.blit(self.block, (block.x, block.y))
            for block in self.rwall_hitboxes:
                self.screen.blit(self.block, (block.x, block.y))
            for block in self.floor_hitboxes:
                self.screen.blit(self.block, (block.x, block.y))
            for block in self.roof_hitboxes:
                self.screen.blit(self.block, (block.x, block.y))

            dx = 0
            if self.movement[0]:
                dx -= self.player_speed_x
            if self.movement[1]:
                dx += self.player_speed_x

            self.player_pos[0] += dx

            player_hitbox = pygame.Rect(self.player_pos[0], self.player_pos[1], self.player_size[0], self.player_size[1])

            for block in self.lwall_hitboxes + self.rwall_hitboxes:
                if player_hitbox.colliderect(block):
                    if dx > 0:
                        self.player_pos[0] = block.left - self.player_size[0]
                    if dx < 0:
                        self.player_pos[0] = block.right

            self.player_velocity_y += 0.5

            if self.player_velocity_y > 10:
                self.player_velocity_y = 10

            self.player_pos[1] += self.player_velocity_y

            self.grounded = False

            player_hitbox = pygame.Rect(self.player_pos[0],self.player_pos[1],self.player_size[0],self.player_size[1])

            for block in self.floor_hitboxes:
                if player_hitbox.colliderect(block):
                    self.player_velocity_y = 0
                    self.player_pos[1] = block.top - self.player_size[1]
                    self.grounded = True

            for block in self.roof_hitboxes:
                if player_hitbox.colliderect(block):
                    self.player_velocity_y = 0
                    self.player_pos[1] = block.bottom

            pygame.draw.rect(self.screen, (255,0,0), (self.player_pos[0], self.player_pos[1], self.player_size[0], self.player_size[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]:
                if self.grounded:
                    self.player_velocity_y = -10

            pygame.display.update()
            self.clock.tick(60)

Game().run()