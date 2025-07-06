import pygame
import random
from settings import *

class Grade(pygame.sprite.Sprite):
    def __init__(self, x, y, grade_type, color, value, is_commission):
        super().__init__()
        self.is_commission = is_commission
        self.grade_value = value
        self.type = grade_type
        
        self.base_speed = 3
        self.amplitude = random.uniform(0.3, 1.5)  
        self.frequency = random.uniform(0.03, 0.08)
        self.initial_x = x
        self.frame = 0
        self.spawn_time = pygame.time.get_ticks()
        
        self.orange_palette = {
            "5": (255, 200, 100),  
            "4": (255, 160, 60),   
            "3": (255, 120, 40),   
            "2": (255, 80, 30)     
        }
        
        self.color = self.orange_palette.get(grade_type, color)
        self.create_sprite()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.uniform(2.0, 3.5)  
    
    def create_sprite(self):
        if self.is_commission:
            width = 160  
            height = 70
            
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            
            for i in range(height):
                r = 255 - int(i * 1.2)
                g = 80 - int(i * 0.8)
                b = 60 - int(i * 0.6)
                pygame.draw.line(self.image, (r, g, b, 255), (0, i), (width, i))
            
            font_size = 28
            font = None
            text_width = width + 1 
            
            while text_width > width - 20 and font_size > 16:
                font = pygame.font.SysFont('Arial', font_size, bold=True)
                text = font.render("КОМИССИЯ", True, (255, 255, 255))
                text_width = text.get_width()
                font_size -= 1
            
            shadow = font.render("КОМИССИЯ", True, (0, 0, 0, 150))
            text_rect = text.get_rect(center=(width//2, height//2))
            
            self.image.blit(shadow, (text_rect.x+2, text_rect.y+2))
            self.image.blit(text, text_rect)
            
            pygame.draw.rect(self.image, (255, 215, 0), (0, 0, width, height), 3, border_radius=10)
        else:
            size = 40 + int(self.grade_value * 5)  
            
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            
            for r in range(size//2, size//2 - 5, -1):
                alpha = 255 - (size//2 - r) * 30
                color = (*self.color, alpha)
                pygame.draw.circle(self.image, color, (size//2, size//2), r)
            
            inner_color = tuple(min(c + 40, 255) for c in self.color)
            pygame.draw.circle(self.image, inner_color, (size//2, size//2), size//2 - 8)
            
            font_size = max(20, 30 - len(self.type) * 2)
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text = font.render(self.type, True, (255, 255, 240))
            shadow = font.render(self.type, True, (100, 50, 0, 150))
            
            text_rect = text.get_rect(center=(size//2, size//2))
            self.image.blit(shadow, (text_rect.x+1, text_rect.y+1))
            self.image.blit(text, text_rect)
    
    def update(self):
        current_time = pygame.time.get_ticks()
        self.frame += 1
        
        if current_time - self.spawn_time < 500:
            progress = (current_time - self.spawn_time) / 500
            current_speed = self.speed * min(progress * 2, 1.0)
        else:
            current_speed = self.speed
            
        self.rect.y += current_speed
        
        if current_time - self.spawn_time > 300:
            new_x = self.initial_x + self.amplitude * pygame.math.Vector2(1, 0).rotate(self.frame * self.frequency).x

            if self.is_commission:
                margin = 80  
            else:
                margin = 40  
                
            self.rect.x = max(margin, min(SCREEN_WIDTH - margin - self.rect.width, new_x))
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()