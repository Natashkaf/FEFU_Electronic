import pygame
from settings import *

class Student(pygame.sprite.Sprite):
    def __init__(self, gender="male"):
        super().__init__()
        self.gender = gender
        self.load_images()
        self.image = self.stand_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 80  
        self.speed = 8
        self.walk_animation_timer = 0
        self.walk_animation_delay = 200
        self.current_walk_frame = 0
        self.walking = False
        self.facing_right = True
        
    def load_images(self):
        TARGET_WIDTH = 70
        TARGET_HEIGHT = 100
        
        if self.gender == "male":
            stand = pygame.image.load('assets/image/boy_stand.png').convert_alpha()
            left = pygame.image.load('assets/image/boy_left.png').convert_alpha()
            right = pygame.image.load('assets/image/boy_right.png').convert_alpha()
        else:
            stand = pygame.image.load('assets/image/girl_stand.png').convert_alpha()
            left = pygame.image.load('assets/image/girl_left.png').convert_alpha()
            right = pygame.image.load('assets/image/girl_right.png').convert_alpha()
        
        self.stand_img = pygame.transform.scale(stand, (TARGET_WIDTH, TARGET_HEIGHT))
        self.left_img = pygame.transform.scale(left, (TARGET_WIDTH, TARGET_HEIGHT))
        self.right_img = pygame.transform.scale(right, (TARGET_WIDTH, TARGET_HEIGHT))
        
        self.stand_img_flipped = pygame.transform.flip(self.stand_img, True, False)
        self.left_img_flipped = pygame.transform.flip(self.left_img, True, False)
        self.right_img_flipped = pygame.transform.flip(self.right_img, True, False)
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.walking = False
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.walking = True
            self.facing_right = False
            
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.walking = True
            self.facing_right = True
            
        if self.walking:
            now = pygame.time.get_ticks()
            if now - self.walk_animation_timer > self.walk_animation_delay:
                self.walk_animation_timer = now
                self.current_walk_frame = 1 - self.current_walk_frame
                
            if self.current_walk_frame == 0:
                current_img = self.left_img
                current_img_flipped = self.left_img_flipped
            else:
                current_img = self.right_img
                current_img_flipped = self.right_img_flipped
                
            self.image = current_img if self.facing_right else current_img_flipped
        else:
            self.image = self.stand_img if self.facing_right else self.stand_img_flipped