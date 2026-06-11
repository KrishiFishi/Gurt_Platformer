"""
GURT PLATFORMER

Student Name: Krishna Binil
Course Code: ICS3U0-2
Teacher Name: Mr Farooqi
Date: June 07, 2026

Gurt Platformer is a game where you are playing as Gurt, and your goal is to get out of the dungeon you
are trapped in as fast as you can. Gurt has the ability to wall jump, dash, and somehow come back to life
infinitely.

"""

import pygame
import sys
import levels

class Player:
    def __init__(self,x,y):
        self.player_size = [32, 32]

        self.sprite_idle = pygame.image.load('data/images/entities/player sprites/gurt_idle.png').convert()
        self.sprite_idle = pygame.transform.scale(self.sprite_idle, (self.player_size[0], self.player_size[1]))

        self.sprite_left = pygame.image.load('data/images/entities/player sprites/gurt_left.png').convert()
        self.sprite_left = pygame.transform.scale(self.sprite_left, (self.player_size[0], self.player_size[1]))

        self.sprite_right = pygame.image.load('data/images/entities/player sprites/gurt_right.png').convert()
        self.sprite_right = pygame.transform.scale(self.sprite_right, (self.player_size[0], self.player_size[1]))

        self.player_sprite = self.sprite_idle

        self.movement_x = [False, False]
        self.player_speed_x = 5
        self.player_pos = [x, y]
        self.player_velocity_y = 0
        self.grounded = False

        self.dash_frames = 0
        self.dash_on_cooldown = False
        self.dash_direction = 1
        self.dash_speed = 20

        self.on_wall = 0
        self.wall_slide_speed = 2
        self.wall_jump_timer = 0

    def dash(self):
        if self.dash_frames == 0 and not self.dash_on_cooldown:
            self.dash_frames = 10
            self.dash_on_cooldown = True

    def reset_position(self,start_x,start_y):
        self.player_pos = [start_x, start_y]
        self.player_velocity_y = 0
        self.dash_frames = 0
        self.dash_on_cooldown = False
        self.wall_jump_timer = 0
        self.on_wall = 0
        self.grounded = False
        self.player_sprite = self.sprite_idle

    def physics(self, block_hitboxes):
        dx = 0

        if self.wall_jump_timer > 0:
            self.wall_jump_timer -= 1

        if self.wall_jump_timer == 0:
            self.player_sprite = self.sprite_idle
            if self.movement_x[0]:
                dx -= self.player_speed_x
                self.dash_direction = -1
                self.player_sprite  = self.sprite_left
            if self.movement_x[1]:
                dx += self.player_speed_x
                self.dash_direction = 1
                self.player_sprite = self.sprite_right
        else:
            if self.player_velocity_y < 0:
                dx = self.dash_direction * self.player_speed_x

        if self.dash_frames > 0:
            self.dash_frames -= 1
            dx = self.dash_direction * self.dash_speed
            self.player_velocity_y = 0

        self.on_wall = 0

        self.player_pos[0] += dx

        player_hitbox = pygame.Rect(self.player_pos[0], self.player_pos[1], self.player_size[0], self.player_size[1])

        if dx < 0:
            for block in block_hitboxes:
                if player_hitbox.colliderect(block):
                    self.player_pos[0] = block.right
                    if not self.grounded:
                        self.on_wall = -1
        if dx > 0:
            for block in block_hitboxes:
                if player_hitbox.colliderect(block):
                    self.player_pos[0] = block.left - self.player_size[0]
                    if not self.grounded:
                        self.on_wall = 1

        if self.dash_frames == 0:
            self.player_velocity_y += 0.5

            if self.on_wall != 0 and self.player_velocity_y > 0:
                if self.player_velocity_y > self.wall_slide_speed:
                    self.player_velocity_y = self.wall_slide_speed
            else:
                if self.player_velocity_y > 10:
                    self.player_velocity_y = 10

        self.player_pos[1] += self.player_velocity_y
        self.grounded = False

        player_hitbox = pygame.Rect(self.player_pos[0], self.player_pos[1], self.player_size[0], self.player_size[1])

        for block in block_hitboxes:
            if player_hitbox.colliderect(block):
                if self.player_velocity_y > 0:
                    self.player_velocity_y = 0
                    self.player_pos[1] = block.top - self.player_size[1]
                    self.grounded = True
                    self.dash_on_cooldown = False
                elif self.player_velocity_y < 0:
                    self.player_velocity_y = 0
                    self.player_pos[1] = block.bottom

class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load('data/sfx/aotl.mp3')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.05)

        pygame.display.set_caption("Gurt Platformer")
        self.screen = pygame.display.set_mode((1185, 700))
        self.clock = pygame.time.Clock()
        self.current_level = 0
        self.spawn_points = [
            (100, 600),
            (1050, 150)
        ]

        self.game_timer = 0.0
        self.final_time = 0.0
        self.timer_font = pygame.font.SysFont("Arial", 15)

        self.player = Player(self.spawn_points[0][0], self.spawn_points[0][1])

        self.state = "MENU"
        self.top_button_name = "Start"
        self.large_text_name = "Gurt"
        self.font = pygame.font.SysFont("Arial", 40)
        self.title_font = pygame.font.SysFont("Impact", 200)

        self.start_button = pygame.Rect(500,400,200,50)
        self.quit_button = pygame.Rect(500,500,200,50)

        self.level_manager = levels.LevelManager(self.player.player_size)

    def menu(self, mouse_pos):
        self.screen.fill((0, 0, 0))

        title = self.title_font.render(self.large_text_name, True, (255, 255, 255))
        title_box = title.get_rect(center=(600, 220))
        self.screen.blit(title, title_box)

        if self.start_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (170, 170, 170), self.start_button)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), self.start_button)

        if self.quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (170, 170, 170), self.quit_button)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), self.quit_button)

        start_text = self.font.render(self.top_button_name, True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)

        quit_text = self.font.render("Quit", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)
        self.screen.blit(quit_text, quit_text_rect)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            left_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_click = True
                if self.state == "GAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.large_text_name = "Paused"
                            self.top_button_name = "Continue"
                            self.state = "MENU"
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.player.movement_x[0] = True
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.player.movement_x[1] = True
                        if event.key == pygame.K_SPACE or event.key == pygame.K_LSHIFT:
                            self.player.dash()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.player.movement_x[0] = False
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.player.movement_x[1] = False
            if self.state == "GAME":
                key = pygame.key.get_pressed()
                if key[pygame.K_UP] or key[pygame.K_w]:
                    if self.player.grounded:
                        self.player.player_velocity_y = -10
                    elif self.player.on_wall != 0:
                        self.player.player_velocity_y = -9

                        self.player.dash_direction = -self.player.on_wall
                        self.player.wall_jump_timer = 10
                        self.player.dash_on_cooldown = False

            if self.state == "MENU":
                self.menu(mouse_pos)

                if left_click:
                    if self.start_button.collidepoint(mouse_pos):
                        if self.top_button_name == "Start" or self.top_button_name == "Play Again":
                            self.game_timer = 0.0
                            self.large_text_name = "Gurt"
                            self.top_button_name = "Start"
                        self.state = "GAME"
                    elif self.quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            elif self.state == "GAME":
                self.game_timer += 1 / 60

                self.player.physics(self.level_manager.block_hitboxes)

                player_rect = pygame.Rect(self.player.player_pos[0], self.player.player_pos[1],self.player.player_size[0], self.player.player_size[1])

                current_spawn = self.spawn_points[self.current_level]

                for spike in self.level_manager.spike_up_hitboxes:
                    if player_rect.colliderect(spike):
                        self.player.reset_position(current_spawn[0], current_spawn[1])
                        break
                for spike in self.level_manager.spike_down_hitboxes:
                    if player_rect.colliderect(spike):
                        self.player.reset_position(current_spawn[0], current_spawn[1])
                        break
                for spike in self.level_manager.spike_right_hitboxes:
                    if player_rect.colliderect(spike):
                        self.player.reset_position(current_spawn[0], current_spawn[1])
                        break
                for spike in self.level_manager.spike_left_hitboxes:
                    if player_rect.colliderect(spike):
                        self.player.reset_position(current_spawn[0], current_spawn[1])
                        break

                for goal in self.level_manager.goal_hitboxes:
                    if player_rect.colliderect(goal):
                        self.current_level += 1

                        try:
                            self.level_manager.level_creation(levels.level_list[self.current_level])
                            next_spawn = self.spawn_points[self.current_level]
                            self.player.reset_position(next_spawn[0], next_spawn[1])

                        except IndexError:
                            self.final_time = self.game_timer
                            self.current_level = 0
                            self.level_manager.level_creation(levels.level_list[self.current_level])

                            start_spawn = self.spawn_points[0]
                            self.player.reset_position(start_spawn[0], start_spawn[1])

                            v_mins = int(self.final_time // 60)
                            v_secs = int(self.final_time % 60)
                            v_cents = int((self.final_time * 100) % 100)

                            self.large_text_name = f"Time: {v_mins:02d}:{v_secs:02d}:{v_cents:02d}"
                            self.top_button_name = "Play Again"
                            self.state = "MENU"
                        break

                self.screen.fill((0, 0, 0))
                self.level_manager.draw(self.screen)

                ppos = self.player.player_pos
                self.screen.blit(self.player.player_sprite, (ppos[0], ppos[1]))

                minutes = int(self.game_timer // 60)
                seconds = int(self.game_timer % 60)
                centiseconds = int((self.game_timer * 100) % 100)

                time_string = f"{minutes:02d}:{seconds:02d}:{centiseconds:02d}"

                time_taken = self.timer_font.render(time_string, True, (255, 255, 255))
                timer_rect = time_taken.get_rect(center=(1185 // 2, 15))
                self.screen.blit(time_taken, timer_rect)

            pygame.display.update()
            self.clock.tick(60)

Game().run()
