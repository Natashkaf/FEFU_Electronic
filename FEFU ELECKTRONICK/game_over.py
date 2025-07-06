import pygame
from settings import *
from results import Results
class GameOver:
    def __init__(self, screen, rau, commissions_caught):
        self.screen = screen
        self.rau = rau
        self.commissions_caught = commissions_caught
        self.results_manager = Results()
        self.results_manager.add_result(rau)
        
        self.ORANGE_PRIMARY = (255, 140, 0)
        self.ORANGE_DARK = (200, 90, 0)
        self.ORANGE_LIGHT = (255, 180, 60)
        self.ORANGE_WARNING = (255, 100, 50)
        self.BG_COLOR = (250, 240, 230)
        self.PANEL_COLOR = (255, 250, 245)
        self.SHADOW_COLOR = (220, 210, 200)
        self.TEXT_COLOR = (80, 60, 40)
        

        self.font_large = pygame.font.SysFont('Arial', 56, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 42)
        self.font_small = pygame.font.SysFont('Arial', 36)
        

        self.panel_rect = pygame.Rect(50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100)
        

        button_width = 300
        button_height = 60
        self.buttons = [
            {
                "rect": pygame.Rect(
                    self.panel_rect.centerx - button_width//2,
                    self.panel_rect.centery + 100,
                    button_width,
                    button_height
                ),
                "text": "Ещё раз",
                "color": self.ORANGE_LIGHT,
                "hover_color": self.ORANGE_PRIMARY,
                "action": "restart"
            },
            {
                "rect": pygame.Rect(
                    self.panel_rect.centerx - button_width//2,
                    self.panel_rect.centery + 180,
                    button_width,
                    button_height
                ),
                "text": "В меню",
                "color": (220, 120, 100),
                "hover_color": (200, 90, 80),
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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None
    
    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, self.SHADOW_COLOR, self.panel_rect.move(5, 5), border_radius=15)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, self.panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (200, 180, 160), self.panel_rect, 3, border_radius=15)
        
        title = self.font_large.render("Игра Окончена", True, self.ORANGE_PRIMARY)
        title_pos = (self.panel_rect.centerx - title.get_width()//2, self.panel_rect.top + 70)
        self.screen.blit(title, title_pos)
        
        if self.commissions_caught >= 4:
            reason_text = self.font_medium.render("Вы получили 4 комиссии!", True, self.ORANGE_WARNING)
            rau_text = self.font_medium.render(f"Ваш РАУ: {self.rau:.2f}", True, self.ORANGE_PRIMARY)
            
            max_width = max(reason_text.get_width(), rau_text.get_width())
            total_height = reason_text.get_height() + rau_text.get_height() + 30  # 30px - отступ между текстами
            
            combined_bg = pygame.Surface((max_width + 60, total_height + 40), pygame.SRCALPHA)
            combined_bg.fill((*self.ORANGE_LIGHT[:3], 50))
            pygame.draw.rect(combined_bg, (200, 150, 100), (0, 0, combined_bg.get_width(), combined_bg.get_height()), 1, border_radius=10)
            
            combined_bg_pos = (self.panel_rect.centerx - combined_bg.get_width()//2, self.panel_rect.centery - 120)
            self.screen.blit(combined_bg, combined_bg_pos)
            
            reason_pos = (self.panel_rect.centerx - reason_text.get_width()//2, self.panel_rect.centery - 100)
            rau_pos = (self.panel_rect.centerx - rau_text.get_width()//2, self.panel_rect.centery - 50)
            
            self.screen.blit(reason_text, reason_pos)
            self.screen.blit(rau_text, rau_pos)
        else:
            reason_text = self.font_medium.render("Игра завершена", True, self.TEXT_COLOR)
            rau_text = self.font_medium.render(f"Ваш РАУ: {self.rau:.2f}", True, self.ORANGE_PRIMARY)
            
            max_width = max(reason_text.get_width(), rau_text.get_width())
            total_height = reason_text.get_height() + rau_text.get_height() + 30
            
            combined_bg = pygame.Surface((max_width + 60, total_height + 40), pygame.SRCALPHA)
            combined_bg.fill((*self.ORANGE_LIGHT[:3], 50))
            pygame.draw.rect(combined_bg, (200, 150, 100), (0, 0, combined_bg.get_width(), combined_bg.get_height()), 1, border_radius=10)
            
            combined_bg_pos = (self.panel_rect.centerx - combined_bg.get_width()//2, self.panel_rect.centery - 120)
            self.screen.blit(combined_bg, combined_bg_pos)
            
            reason_pos = (self.panel_rect.centerx - reason_text.get_width()//2, self.panel_rect.centery - 100)
            rau_pos = (self.panel_rect.centerx - rau_text.get_width()//2, self.panel_rect.centery - 50)
            
            self.screen.blit(reason_text, reason_pos)
            self.screen.blit(rau_text, rau_pos)
        
        for i, button in enumerate(self.buttons):
            color = button["hover_color"] if i == self.hovered_button else button["color"]
            
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=12)
            pygame.draw.rect(self.screen, (80, 50, 30), button["rect"], 2, border_radius=12)
            
            text = self.font_small.render(button["text"], True, (40, 30, 20))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
            
            if i == self.hovered_button:
                glow = pygame.Surface((button["rect"].width + 10, button["rect"].height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*color[:3], 50), (0, 0, glow.get_width(), glow.get_height()), border_radius=15)
                self.screen.blit(glow, (button["rect"].x - 5, button["rect"].y - 5))