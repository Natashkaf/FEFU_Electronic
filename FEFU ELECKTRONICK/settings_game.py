import pygame
from settings import *

class SettingsGame:
    def __init__(self, screen, gender="male", music_volume=50, sfx_volume=70):
        self.screen = screen
        self.gender = gender
        self.music_volume = music_volume  
        self.sfx_volume = sfx_volume      
        self.font = pygame.font.SysFont('Arial', 32)
        self.title_font = pygame.font.SysFont('Arial', 56, bold=True)
        
        self.ORANGE_PRIMARY = (255, 140, 0)
        self.ORANGE_BRIGHT = (255, 165, 0)
        self.ORANGE_DARK = (200, 90, 0)
        self.BG_COLOR = (250, 240, 230)
        self.PANEL_COLOR = (255, 250, 245)
        self.SHADOW_COLOR = (220, 210, 200)
        self.TEXT_COLOR = (80, 60, 40)
        
        original_boy = pygame.image.load('assets/image/boy_static.png').convert_alpha()
        original_girl = pygame.image.load('assets/image/girl_static.png').convert_alpha()
        
        button_width = 90
        button_height = 160
        
        def create_wide_image(original_img, width, height):
            orig_width, orig_height = original_img.get_size()
            scale = min(width/orig_width, height/orig_height) * 0.8
            scaled_img = pygame.transform.scale(original_img, 
                                             (int(orig_width*scale), 
                                             int(orig_height*scale)))
            result = pygame.Surface((width, height), pygame.SRCALPHA)
            x_pos = (width - scaled_img.get_width()) // 2
            y_pos = (height - scaled_img.get_height()) // 2
            result.blit(scaled_img, (x_pos, y_pos))
            return result
            
        self.boy_img = create_wide_image(original_boy, button_width, button_height)
        self.girl_img = create_wide_image(original_girl, button_width, button_height)
        
        self.back_button = {
            "rect": pygame.Rect(30, 30, 120, 45),
            "text": "← Назад",
            "color": self.ORANGE_DARK,
            "hover_color": self.ORANGE_PRIMARY
        }
        
        self.music_volume_slider = {
            "rect": pygame.Rect(SCREEN_WIDTH//2 - 150, 200, 300, 10),
            "handle_rect": pygame.Rect(SCREEN_WIDTH//2 - 5 + (self.music_volume * 3 - 150), 200 - 5, 10, 20),
            "color": self.ORANGE_PRIMARY,
            "bg_color": (230, 220, 210),
            "dragging": False
        }
        
        self.sfx_volume_slider = {
            "rect": pygame.Rect(SCREEN_WIDTH//2 - 150, 300, 300, 10),
            "handle_rect": pygame.Rect(SCREEN_WIDTH//2 - 5 + (self.sfx_volume * 3 - 150), 300 - 5, 10, 20),
            "color": self.ORANGE_PRIMARY,
            "bg_color": (230, 220, 210),
            "dragging": False
        }
        
        self.gender_buttons = [
            {
                "rect": pygame.Rect(SCREEN_WIDTH//2 - button_width - 20, 400, button_width, button_height),
                "image": self.boy_img,
                "selected": self.gender == 'male',
                "gender": "male"
            },
            {
                "rect": pygame.Rect(SCREEN_WIDTH//2 + 20, 400, button_width, button_height),
                "image": self.girl_img,
                "selected": self.gender == 'female',
                "gender": "female"
            }
        ]
        
        self.selection_color = (0, 200, 0, 150)
        self.selection_width = 4
        self.back_hovered = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.back_hovered = self.back_button["rect"].collidepoint(event.pos)
            
            if self.music_volume_slider["dragging"]:
                mouse_x = max(self.music_volume_slider["rect"].left, 
                            min(event.pos[0], self.music_volume_slider["rect"].right))
                self.music_volume = int((mouse_x - self.music_volume_slider["rect"].x) / 3)
                self.music_volume = max(0, min(100, self.music_volume))
                self.music_volume_slider["handle_rect"].x = self.music_volume_slider["rect"].x + self.music_volume * 3 - 5
            
            if self.sfx_volume_slider["dragging"]:
                mouse_x = max(self.sfx_volume_slider["rect"].left, 
                            min(event.pos[0], self.sfx_volume_slider["rect"].right))
                self.sfx_volume = int((mouse_x - self.sfx_volume_slider["rect"].x) / 3)
                self.sfx_volume = max(0, min(100, self.sfx_volume))
                self.sfx_volume_slider["handle_rect"].x = self.sfx_volume_slider["rect"].x + self.sfx_volume * 3 - 5
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button["rect"].collidepoint(event.pos):
                selected_gender = next((btn["gender"] for btn in self.gender_buttons if btn["selected"]), 'male')
                return ("back", selected_gender, self.music_volume, self.sfx_volume)
            
            if (self.music_volume_slider["handle_rect"].collidepoint(event.pos) or 
                self.music_volume_slider["rect"].collidepoint(event.pos)):
                self.music_volume_slider["dragging"] = True
                mouse_x = max(self.music_volume_slider["rect"].left, 
                            min(event.pos[0], self.music_volume_slider["rect"].right))
                self.music_volume = int((mouse_x - self.music_volume_slider["rect"].x) / 3)
                self.music_volume = max(0, min(100, self.music_volume))
                self.music_volume_slider["handle_rect"].x = self.music_volume_slider["rect"].x + self.music_volume * 3 - 5
            
            if (self.sfx_volume_slider["handle_rect"].collidepoint(event.pos) or 
                self.sfx_volume_slider["rect"].collidepoint(event.pos)):
                self.sfx_volume_slider["dragging"] = True
                mouse_x = max(self.sfx_volume_slider["rect"].left, 
                            min(event.pos[0], self.sfx_volume_slider["rect"].right))
                self.sfx_volume = int((mouse_x - self.sfx_volume_slider["rect"].x) / 3)
                self.sfx_volume = max(0, min(100, self.sfx_volume))
                self.sfx_volume_slider["handle_rect"].x = self.sfx_volume_slider["rect"].x + self.sfx_volume * 3 - 5
            
            for button in self.gender_buttons:
                if button["rect"].collidepoint(event.pos):
                    for btn in self.gender_buttons:
                        btn["selected"] = False
                    button["selected"] = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            self.music_volume_slider["dragging"] = False
            self.sfx_volume_slider["dragging"] = False
        
        return (None, self.gender, self.music_volume, self.sfx_volume)
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        panel_rect = pygame.Rect(50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100)
        pygame.draw.rect(self.screen, self.SHADOW_COLOR, panel_rect.move(5, 5), border_radius=15)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (200, 180, 160), panel_rect, 2, border_radius=15)
        
        title_shadow = self.title_font.render("Настройки", True, (180, 100, 0))
        self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_shadow.get_width()//2 + 3, 83))
        title = self.title_font.render("Настройки", True, self.ORANGE_BRIGHT)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        back_color = self.back_button["hover_color"] if self.back_hovered else self.back_button["color"]
        pygame.draw.rect(self.screen, back_color, self.back_button["rect"], border_radius=8)
        pygame.draw.rect(self.screen, (180, 70, 0), self.back_button["rect"], 2, border_radius=8)
        text_shadow = self.font.render(self.back_button["text"], True, (0, 0, 0, 150))
        text = self.font.render(self.back_button["text"], True, (255, 255, 255))
        text_rect = text.get_rect(center=self.back_button["rect"].center)
        self.screen.blit(text_shadow, (text_rect.x+2, text_rect.y+2))
        self.screen.blit(text, text_rect)
        
        pygame.draw.rect(self.screen, self.music_volume_slider["bg_color"], self.music_volume_slider["rect"], border_radius=5)
        pygame.draw.rect(self.screen, self.music_volume_slider["color"], self.music_volume_slider["handle_rect"], border_radius=5)
        music_text = self.font.render(f"Громкость музыки: {self.music_volume}%", True, self.ORANGE_DARK)
        self.screen.blit(music_text, (SCREEN_WIDTH//2 - music_text.get_width()//2, 170))
        
        pygame.draw.rect(self.screen, self.sfx_volume_slider["bg_color"], self.sfx_volume_slider["rect"], border_radius=5)
        pygame.draw.rect(self.screen, self.sfx_volume_slider["color"], self.sfx_volume_slider["handle_rect"], border_radius=5)
        sfx_text = self.font.render(f"Громкость эффектов: {self.sfx_volume}%", True, self.ORANGE_DARK)
        self.screen.blit(sfx_text, (SCREEN_WIDTH//2 - sfx_text.get_width()//2, 270))
        
        gender_text = self.font.render("Выберите пол:", True, self.ORANGE_PRIMARY)
        self.screen.blit(gender_text, (SCREEN_WIDTH//2 - gender_text.get_width()//2, 370))
        
        for button in self.gender_buttons:
            pygame.draw.rect(self.screen, self.ORANGE_PRIMARY, button["rect"], 3, border_radius=10)
            self.screen.blit(button["image"], button["rect"])
            
            if button["selected"]:
                selection_surface = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
                pygame.draw.rect(selection_surface, self.selection_color, 
                              (0, 0, button["rect"].width, button["rect"].height), 
                              self.selection_width, border_radius=10)
                self.screen.blit(selection_surface, button["rect"])