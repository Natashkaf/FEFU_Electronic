import pygame
from menu import Menu
from game import Game
from settings_game import SettingsGame
from pause import PauseMenu
from sound_manager import SoundManager
from settings import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("FEFU_Electronic")
    clock = pygame.time.Clock()
    

    sound_manager = SoundManager()
    sound_manager.play_music()  
    
    current_music_volume = 50 
    current_sfx_volume = 70    
    current_gender = "male"
    
    menu = Menu(screen, sound_manager)
    settings = SettingsGame(screen, current_gender, current_music_volume, current_sfx_volume)
    pause_menu = PauseMenu(screen, sound_manager)
    game = None
    
    current_screen = "menu"
    running = True
    previous_screen = "menu"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if current_screen == "game":
                    sound_manager.play_sound('pause_open')
                    current_screen = "pause"
                elif current_screen == "pause":
                    sound_manager.play_sound('pause_close')
                    current_screen = "game"
                continue
            
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "start":
                    game = Game(screen, current_gender, sound_manager)
                    current_screen = "game"
                elif action == "settings":
                    settings = SettingsGame(screen, current_gender, current_music_volume, current_sfx_volume)
                    previous_screen = "menu"
                    current_screen = "settings"
                elif action == "exit":
                    running = False
            
            elif current_screen == "game" and game:
                action = game.handle_event(event)
                if action == "menu":
                    current_screen = "menu"
                elif action == "catch":
                    sound_manager.play_sound('catch')
                elif action == "game_over":
                    sound_manager.play_sound('game_over')
            
            elif current_screen == "settings":
                action, gender, music_vol, sfx_vol = settings.handle_event(event)
                if action == "back":
                    current_screen = previous_screen
                    if gender is not None:
                        current_gender = gender
                    if music_vol is not None:
                        current_music_volume = music_vol
                        sound_manager.set_music_volume(music_vol)
                    if sfx_vol is not None:
                        current_sfx_volume = sfx_vol
                        sound_manager.set_sfx_volume(sfx_vol)
                    if previous_screen == "pause" and game is not None:
                        game = Game(screen, current_gender, sound_manager)
            
            elif current_screen == "pause":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = pause_menu.handle_event(event)
                    if action == "resume":
                        sound_manager.play_sound('pause_close')
                        current_screen = "game"
                    elif action == "settings":
                        settings = SettingsGame(screen, current_gender, current_music_volume, current_sfx_volume)
                        previous_screen = "pause"
                        current_screen = "settings"
                    elif action == "menu":
                        current_screen = "menu"
        
        if current_screen == "menu":
            menu.update()
            menu.draw()
        elif current_screen == "game" and game:
            game.update()
            game.draw()
        elif current_screen == "settings":
            settings.update()
            settings.draw()
        elif current_screen == "pause":
            if game:
                game.draw()
            pause_menu.update()
            pause_menu.draw()
            
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
