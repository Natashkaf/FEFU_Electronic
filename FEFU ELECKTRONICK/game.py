import pygame
import random
from settings import *
from pause import PauseMenu
from game_over import GameOver
from player import Student
from platform import Platform
from ratings import Grade 
class Game:
    def __init__(self, screen, gender="male", sound_manager=None):
        self.screen = screen
        self.gender = gender
        self.sound_manager = sound_manager
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.SysFont('Arial', 32)
        
        self.ORANGE_TEXT = (255, 165, 0)  
        self.ORANGE_SHADOW = (180, 100, 0)  
        
        try:
            self.background = pygame.image.load('assets/image/background.jpg').convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(LIBRARY_BLUE)
        
        self.grade_types = [
            ("5", GREEN, 5), ("4", BLUE, 4),
            ("3", YELLOW, 3), ("2", RED, 2)
        ]
        
        self.pause_menu = PauseMenu(screen)
        self.reset()
       
    
    def reset(self):
        self.playing = True
        self.paused = False
        self.game_over = False
        self.rau = 5.0
        self.grades_caught = 0
        self.commissions_caught = 0
        
        self.all_sprites.empty()
        
        self.platform = Platform()
        self.all_sprites.add(self.platform)
        
        self.student = Student(self.gender)
        self.all_sprites.add(self.student)
        
        self.grades = pygame.sprite.Group()
        self.grade_timer = 0
        self.grade_interval = 1500
        self.game_over_screen = None
    
    def spawn_grade(self):
        last_spawns = [s.rect.x for s in self.grades if not s.is_commission][-5:]
        
        for _ in range(20):
            x = random.randint(50, SCREEN_WIDTH - 70)
            
            if all(abs(x - pos) > 120 for pos in last_spawns) or not last_spawns:
                grade_type, color, grade_value = random.choice(self.grade_types)
                grade = Grade(x, -100, grade_type, color, grade_value, False)
                
                if 40 <= grade.rect.x <= SCREEN_WIDTH - 40 - grade.rect.width:
                    self.grades.add(grade)
                    return
        
        x = random.choice([random.randint(50, 150), random.randint(SCREEN_WIDTH - 200, SCREEN_WIDTH - 70)])
        grade_type, color, grade_value = random.choice(self.grade_types)
        self.grades.add(Grade(x, -100, grade_type, color, grade_value, False))

    def spawn_commission(self):
        occupied = [s.rect.x for s in self.grades]
        commission_width = 160 
        
        for _ in range(10):
            x = random.randint(80, SCREEN_WIDTH - 80 - commission_width)
            
            if all(abs(x - pos) > 180 for pos in occupied) or not occupied:
                commission = Grade(x, -120, "", (255, 80, 40), 0, True)
                commission.speed = 2.2
                self.grades.add(commission)
                return
        
        x = 80 if random.random() < 0.5 else SCREEN_WIDTH - 80 - commission_width
        commission = Grade(x, -120, "", (255, 80, 40), 0, True)
        commission.speed = 2.2
        self.grades.add(commission)
    
    def handle_event(self, event):
        if self.game_over and self.game_over_screen:
            action = self.game_over_screen.handle_event(event)
            if action == "restart":
                self.reset()
                return None
            elif action == "menu":
                return "menu"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
        
        if self.paused:
            action = self.pause_menu.handle_event(event)
            if action == "resume":
                self.paused = False
            elif action == "menu":
                return "menu"
        
        return None
    
    def update(self):
        if not self.playing or self.paused or self.game_over:
            return
        
        now = pygame.time.get_ticks()
        if now - self.grade_timer > self.grade_interval:
            self.grade_timer = now
            if random.random() < 0.15:
                self.spawn_commission()
            else:
                self.spawn_grade()
        
        self.all_sprites.update()
        self.student.update()
        self.grades.update()
        
        hits = pygame.sprite.spritecollide(self.student, self.grades, True)
        for hit in hits:
            if hit.is_commission:
                self.commissions_caught += 1
                if self.commissions_caught >= 4:
                    self.playing = False
                    self.game_over = True
                    self.game_over_screen = GameOver(self.screen, self.rau, self.commissions_caught)
            else:
                self.grades_caught += 1
                self.rau = (self.rau * (self.grades_caught - 1) + hit.grade_value) / self.grades_caught
                if self.sound_manager:
                    self.sound_manager.play_sound('catch')
            
            if self.grades_caught % 5 == 0 and self.grade_interval > 600:
                self.grade_interval -= 100
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        self.all_sprites.draw(self.screen)
        self.grades.draw(self.screen)
        
        if self.playing:
            comm_shadow = self.font.render(f"Комиссии: {self.commissions_caught}/4", True, self.ORANGE_SHADOW)
            comm_text = self.font.render(f"Комиссии: {self.commissions_caught}/4", True, self.ORANGE_TEXT)
            self.screen.blit(comm_shadow, (12, 12))
            self.screen.blit(comm_text, (10, 10))
            
            rau_text = f"РАУ: {self.rau:.2f}"
            rau_shadow = self.font.render(rau_text, True, self.ORANGE_SHADOW)
            rau_main = self.font.render(rau_text, True, self.ORANGE_TEXT)
            
            rau_x = SCREEN_WIDTH - rau_main.get_width() - 10
            self.screen.blit(rau_shadow, (rau_x+2, 12))
            self.screen.blit(rau_main, (rau_x, 10))
            
            if self.paused:
                self.pause_menu.draw()
        elif self.game_over and self.game_over_screen:
            self.game_over_screen.draw()