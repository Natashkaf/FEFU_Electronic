import pygame
from settings import *
from results import Results

class Menu:
    def __init__(self, screen, sound_manager=None):  
        self.screen = screen
        self.sound_manager = sound_manager  
        self.show_results = False
        self.results_manager = Results()
        
        self.BG_COLOR = (250, 240, 230)
        self.PANEL_COLOR = (255, 250, 245)
        self.SHADOW_COLOR = (220, 210, 200)
        self.TEXT_COLOR = (80, 60, 40)
        self.ORANGE_PRIMARY = (255, 140, 0)
        self.ORANGE_LIGHT = (255, 180, 60)
        self.RED_LIGHT = (220, 120, 100)
        
        self.font = pygame.font.SysFont('Arial', 36)
        self.title_font = pygame.font.SysFont('Arial', 72, bold=True)
        self.results_font = pygame.font.SysFont('Arial', 24)
        
        self.buttons = [
            {"rect": pygame.Rect(SCREEN_WIDTH//2 - 150, 250, 300, 60),
             "text": "Старт", "color": self.ORANGE_LIGHT, "action": "start"},
            {"rect": pygame.Rect(SCREEN_WIDTH//2 - 150, 330, 300, 60),
             "text": "Настройки", "color": self.ORANGE_LIGHT, "action": "settings"},
            {"rect": pygame.Rect(SCREEN_WIDTH//2 - 150, 410, 300, 60),
             "text": "Результаты", "color": self.ORANGE_LIGHT, "action": "results"},
            {"rect": pygame.Rect(SCREEN_WIDTH//2 - 150, 490, 300, 60),
             "text": "Выход", "color": self.RED_LIGHT, "action": "exit"}
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
                    if button["action"] == "results":
                        self.show_results = not self.show_results
                        return None
                    return button["action"]
        return None
    
    def draw_results_table(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        panel_width, panel_height = 400, 400
        panel_rect = pygame.Rect(
            SCREEN_WIDTH//2 - panel_width//2,
            SCREEN_HEIGHT//2 - panel_height//2,
            panel_width,
            panel_height
        )
        
        pygame.draw.rect(self.screen, self.SHADOW_COLOR, panel_rect.move(5, 5), border_radius=15)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (200, 180, 160), panel_rect, 3, border_radius=15)
        
        title = self.font.render("Топ 10 результатов", True, self.ORANGE_PRIMARY)
        self.screen.blit(title, (panel_rect.centerx - title.get_width()//2, panel_rect.y + 30))
        
        top_results = self.results_manager.get_top_results(10)
        
        close_rect = pygame.Rect(panel_rect.centerx - 100, panel_rect.y + panel_height - 60, 200, 40)
        pygame.draw.rect(self.screen, self.ORANGE_LIGHT, close_rect, border_radius=10)
        pygame.draw.rect(self.screen, (80, 50, 30), close_rect, 2, border_radius=10)
        close_text = self.results_font.render("Закрыть", True, self.TEXT_COLOR)
        self.screen.blit(close_text, (close_rect.centerx - close_text.get_width()//2, 
                                    close_rect.centery - close_text.get_height()//2))
        
        if not top_results:
            no_results = self.results_font.render("Пока нет результатов", True, self.TEXT_COLOR)
            self.screen.blit(no_results, (panel_rect.centerx - no_results.get_width()//2, panel_rect.centery))
            return close_rect
        
        for i, result in enumerate(top_results):
            pos_text = self.results_font.render(f"{i+1}.", True, self.TEXT_COLOR)
            self.screen.blit(pos_text, (panel_rect.x + 50, panel_rect.y + 80 + i*30))
            
            result_text = self.results_font.render(f"{result:.2f}", True, self.ORANGE_PRIMARY)
            self.screen.blit(result_text, (panel_rect.x + 100, panel_rect.y + 80 + i*30))
        
        return close_rect
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        title_panel_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 50, 400, 120)
        pygame.draw.rect(self.screen, self.SHADOW_COLOR, title_panel_rect.move(5, 5), border_radius=15)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, title_panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (200, 180, 160), title_panel_rect, 3, border_radius=15)
        
        title = self.title_font.render("РАУ", True, self.ORANGE_PRIMARY)
        title_shadow = self.title_font.render("РАУ", True, (40, 30, 20))
        title_x = title_panel_rect.x + (title_panel_rect.width - title.get_width()) // 2
        title_y = title_panel_rect.y + (title_panel_rect.height - title.get_height()) // 2
        self.screen.blit(title_shadow, (title_x + 2, title_y + 2))
        self.screen.blit(title, (title_x, title_y))
        
        for i, button in enumerate(self.buttons):
            pygame.draw.rect(self.screen, self.SHADOW_COLOR, button["rect"].move(3, 3), border_radius=10)
            
            color = button["color"]
            if i == self.hovered_button:
                color = tuple(min(c + 20, 255) for c in color)
            
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, (80, 50, 30), button["rect"], 2, border_radius=10)
            
            text = self.font.render(button["text"], True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
        
        if self.show_results:
            close_rect = self.draw_results_table()
            if close_rect is not None:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] and close_rect.collidepoint(mouse_pos):
                    self.show_results = False