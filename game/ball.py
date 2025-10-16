import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, sound_manager=None):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if sound_manager:
                sound_manager.play_sound('wall_bounce')

    def check_collision(self, player, ai, sound_manager=None):
        # Check collision with player paddle
        if self.rect().colliderect(player.rect()) and self.velocity_x < 0:
            # Ensure ball doesn't get stuck inside paddle
            self.x = player.x + player.width
            self.velocity_x *= -1
            if sound_manager:
                sound_manager.play_sound('paddle_hit')
            
        # Check collision with AI paddle  
        elif self.rect().colliderect(ai.rect()) and self.velocity_x > 0:
            # Ensure ball doesn't get stuck inside paddle
            self.x = ai.x - self.width
            self.velocity_x *= -1
            if sound_manager:
                sound_manager.play_sound('paddle_hit')

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
