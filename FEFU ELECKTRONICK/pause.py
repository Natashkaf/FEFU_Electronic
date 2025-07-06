import pygame
from settings import *

class PauseMenu:
    def __init__(self, screen, sound_manager=None):
        self.screen = screen
        self.sound_manager = sound_manager
        
        self.BG_COLOR = (250, 240, 230)
        self.PANEL_COLOR = (255, 250, 245)
        self.SHADOW_COLOR = (220, 210, 200)
        self.TEXT_COLOR = (80, 60, 40)
        self.ORANGE_PRIMARY = (255, 140, 0)
        self.ORANGE_LIGHT = (255, 180, 60)
        self.RED_LIGHT = (220, 120, 100)
        
        self.font = pygame.font.SysFont('Arial', 36)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        
        self.panel_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 175, 400, 350)
        
        button_width, button_height = 300, 60
        start_y = self.panel_rect.y + 100
        
        self.buttons = [
            {
                "rect": pygame.Rect(SCREEN_WIDTH//2 - button_width//2, start_y, button_width, button_height),
                "text": "Продолжить",
                "color": self.ORANGE_LIGHT,
                "action": "resume"
            },
            {
                "rect": pygame.Rect(SCREEN_WIDTH//2 - button_width//2, start_y + 80, button_width, button_height),
                "text": "Настройки",
                "color": self.ORANGE_LIGHT,
                "action": "settings"
            },
            {
                "rect": pygame.Rect(SCREEN_WIDTH//2 - button_width//2, start_y + 160, button_width, button_height),
                "text": "В меню",
                "color": self.RED_LIGHT,
                "action": "menu"
            }
        ]
        self.hovered_button = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered_button = None
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(event.pos):
                    self.hovered_button = i
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None
    
    def update(self):
        pass
    
    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, self.SHADOW_COLOR, self.panel_rect.move(5, 5), border_radius=15)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, self.panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (200, 180, 160), self.panel_rect, 3, border_radius=15)
        
        title = self.title_font.render("Пауза", True, self.ORANGE_PRIMARY)
        title_shadow = self.title_font.render("Пауза", True, (40, 30, 20))
        title_x = self.panel_rect.centerx - title.get_width()//2
        title_y = self.panel_rect.y + 30
        self.screen.blit(title_shadow, (title_x + 2, title_y + 2))
        self.screen.blit(title, (title_x, title_y))
        
        for i, button in enumerate(self.buttons):

            pygame.draw.rect(self.screen, self.SHADOW_COLOR, button["rect"].move(3, 3), border_radius=10)
            
            color = button["color"]

            
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, (80, 50, 30), button["rect"], 2, border_radius=10)
            
            text = self.font.render(button["text"], True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
