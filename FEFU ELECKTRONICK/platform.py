import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.PLATFORM_HEIGHT = 80  
        
        try:
            self.original_image = pygame.image.load('assets/image/platform.png').convert_alpha()
            
            orig_width, orig_height = self.original_image.get_size()
            scale_factor = self.PLATFORM_HEIGHT / orig_height
            new_width = int(orig_width * scale_factor)
            
            self.image = pygame.Surface((SCREEN_WIDTH, self.PLATFORM_HEIGHT), pygame.SRCALPHA)
            for x in range(0, SCREEN_WIDTH, new_width):
                scaled_segment = pygame.transform.scale(self.original_image, (new_width, self.PLATFORM_HEIGHT))
                self.image.blit(scaled_segment, (x, 0))
            
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = SCREEN_HEIGHT - self.PLATFORM_HEIGHT  
            
            self.mask = pygame.mask.from_surface(self.image)
            
        except pygame.error as e:
            print(f"Ошибка загрузки изображения платформы: {e}")
            self.image = pygame.Surface((SCREEN_WIDTH, self.PLATFORM_HEIGHT))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = SCREEN_HEIGHT - self.PLATFORM_HEIGHT
            self.mask = pygame.mask.from_surface(self.image)