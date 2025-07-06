# sound_manager.py
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        
        self.sounds = {
            'background': None,
            'catch': None,
            'game_over': None,
            'pause_open': None,
            'pause_close': None,
        }
        
        try:
            self.sounds['background'] = pygame.mixer.Sound('assets/sounds/background_music.mp3')
            self.sounds['catch'] = pygame.mixer.Sound('assets/sounds/catch_music.mp3')
            self.sounds['game_over'] = pygame.mixer.Sound('assets/sounds/game_over_music.mp3')
            self.sounds['pause_open'] = pygame.mixer.Sound('assets/sounds/pause_to.mp3')
            self.sounds['pause_close'] = pygame.mixer.Sound('assets/sounds/pause_back.mp3')
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")

        self.music_volume = 0.5  
        self.sfx_volume = 0.7    
        self.update_volumes()
    
    def update_volumes(self):
        if self.sounds['background']:
            self.sounds['background'].set_volume(self.music_volume)
        
        for sound_name, sound in self.sounds.items():
            if sound and sound_name != 'background':
                sound.set_volume(self.sfx_volume)
    
    def play_music(self, loop=True):
        if self.sounds['background']:
            self.sounds['background'].play(-1)
    
    def stop_music(self):
        if self.sounds['background']:
            self.sounds['background'].stop()
    
    def pause_music(self):
        if self.sounds['background']:
            self.sounds['background'].set_volume(0)
    
    def resume_music(self):
        if self.sounds['background']:
            self.sounds['background'].set_volume(self.music_volume)
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
    
    def set_music_volume(self, volume):
        self.music_volume = volume / 100
        if self.sounds['background']:
            self.sounds['background'].set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = volume / 100
        self.update_volumes()