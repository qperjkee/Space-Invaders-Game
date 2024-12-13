import pygame, pygame_widgets, sys, json, os
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle
from .constants import WIDTH, HEIGHT, COLOR_ACTIVE, COLOR_INACTIVE, COLOR_LIST_ACTIVE, COLOR_LIST_INACTIVE, SOUND_ON_ICON, SOUND_OFF_ICON, SETTINGS_ICON, RED_SPACE_SHIP, BLUE_SPACE_SHIP, GREEN_SPACE_SHIP, ORANGE_SPACE_SHIP, PINK_SPACE_SHIP, HEALTH_BONUS, LIVES_BONUS, SHIELD_BONUS, SLOW_BONUS, ALIEN, SCENE, BG, AWARD, ROCKET, PLANET, WIN, GAME_MUSIC
from .button import Button
from .game import Game
from .dropdown import DropDown


class Menu:
    def __init__(self):
        self.init_pygame()
        self.load_fonts()
        self.bg_y = 0
    
    def init_pygame(self):
        pygame.mixer.init()
        pygame.display.set_caption("Space Invaders")
        self.GAME_MUSIC = pygame.mixer.Sound("sfx/game_sound.mp3")
        self.WIN = WIN

    def load_fonts(self):
        self.info_font = pygame.font.Font('font/my_font.ttf', 30)
        self.end_font = pygame.font.Font('font/my_font.ttf', 110)
        self.top_font = pygame.font.Font('font/my_font.ttf', 65)
        self.result_font = pygame.font.Font('font/my_font.ttf', 75)
        self.info_font2 = pygame.font.SysFont('comicsans', 20)
        self.settings_font = pygame.font.SysFont('comicsans', 30)
        self.result_font2 = pygame.font.Font('font/my_font.ttf', 45)

    def read_top_scores(self):
        if not os.path.exists('data/scores.txt'):
            open('data/scores.txt', 'w').close()
            return []
        return self.get_top_n_scores(5)

    def get_top_n_scores(self, n):
        with open('data/scores.txt', 'r') as file:
            return [int(line.strip()) for line in file if line][:n]

    def find_score_row(self, score):
        with open('data/scores.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if int(line.strip()) == score:
                    return i + 1

    def get_font(self, size): 
        return pygame.font.Font("font/font.ttf", size)

    def main_menu(self, music_off=False):
        self.load_saved_game_settings_from_file()
        if not music_off:
            self.start_music()
        self.setup_menu_elements()
        self.main_menu_loop()

    def start_music(self):
        pygame.mixer.Channel(0).set_volume(0.1)
        pygame.mixer.Channel(0).play(self.GAME_MUSIC)

    def setup_menu_elements(self, ):
        self.sound_icon_rect = SOUND_ON_ICON.get_rect(topleft=(WIDTH - 100, HEIGHT - 100))
        self.sound_icon = SOUND_ON_ICON

        self.settings_icon_rect = SETTINGS_ICON.get_rect(topleft=(WIDTH - 1190, HEIGHT - 740))
        self.settings_icon = SETTINGS_ICON

    def main_menu_loop(self):
        run = True
        while run:
            self.move_bg()
            self.draw_menu_elements()
            self.handle_menu_events()
            pygame.display.update()

    def draw_menu_elements(self):
        self.PLAY_BUTTON = Button(pos=(WIDTH/2, HEIGHT-450), text_input="PLAY", font=self.get_font(75), base_color="White", hovering_color="Green")
        self.INFO_BUTTON = Button(pos=(WIDTH-150, HEIGHT-50), text_input="INFO", font=self.get_font(25), base_color="White", hovering_color="Green")
        self.LOAD_BUTTON = Button(pos=(WIDTH/2, HEIGHT-100), text_input="Load Saved Game", font=self.end_font, base_color=(153,0,153), hovering_color="Green")
        
        for button in [self.PLAY_BUTTON, self.INFO_BUTTON, self.LOAD_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.WIN)
        
        self.WIN.blit(self.sound_icon, (WIDTH - 100, HEIGHT - 100))
        self.WIN.blit(self.settings_icon, (WIDTH - 1190, HEIGHT - 740))
        self.draw_title()
        self.draw_scores()

    def draw_title(self):
        title_label = self.end_font.render("Space Invaders", 1, (118, 12, 139))
        result_label = self.result_font2.render("Top Results ", 1, (0,255,0))
        self.WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 10))
        self.WIN.blit(result_label, (WIDTH - 1190, HEIGHT-280))

    def draw_scores(self):
        font = pygame.font.Font('font/my_font.ttf', 40)
        top_scores = self.read_top_scores()
        for i, score in enumerate(top_scores):
            text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
            self.WIN.blit(text, (20, 520 + i*40))

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_menu_click(event)

    def handle_menu_click(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.PLAY_BUTTON.checkForInput(mouse_pos):
            pygame.mixer.Channel(0).stop()
            game = Game(settings=self.game_settings)
            game.run_game()
        elif self.LOAD_BUTTON.checkForInput(mouse_pos):
            self.load_previous_game()
        elif self.sound_icon_rect.collidepoint(event.pos):
            self.toggle_sound()
        elif self.settings_icon_rect.collidepoint(event.pos):
            self.settings_menu()
        elif self.INFO_BUTTON.checkForInput(mouse_pos):
            self.info_menu()

    def load_previous_game(self):
        try:
            with open('data/game_phase.txt') as f:
                data = json.load(f)
                pygame.mixer.Channel(0).stop()
                game = Game(data, self.game_settings, True)
                game.run_game()
        except json.JSONDecodeError:
            data = {}
        except FileNotFoundError:
            with open('data/game_phase.txt', 'w') as _:
                pass

    def toggle_sound(self):
        if self.sound_icon == SOUND_ON_ICON:
            self.sound_icon = SOUND_OFF_ICON
            pygame.mixer.Channel(0).stop()
        else:
            self.sound_icon = SOUND_ON_ICON
            pygame.mixer.Channel(0).play(self.GAME_MUSIC)

    def settings_menu(self):
        self.create_sliders()
        self.create_dropdowns()
        self.create_toggles()
        self.init_settings_labels()
        self.apply_game_settings()

        run = True
        while run:
            self.move_bg()
            self.draw_settings_menu()
            self.handle_settings_menu_events()
            self.update_slider_values()

            pygame_widgets.update(pygame.event.get())
            self.draw_dropdowns()
            pygame.display.update()
    
    def load_saved_game_settings_from_file(self):
        try:
            with open('data/game_settings.txt', 'r') as f:
                self.game_settings = json.load(f)
        except json.JSONDecodeError:
            self.game_settings = {}
        except FileNotFoundError:
            with open('data/game_settings.txt', 'w') as _:
                pass
            self.game_settings = {}
    
    def apply_game_settings(self):
        if len(self.game_settings) != 0:
            self.hp_slider.setValue(self.game_settings.get('player.hp'))
            self.lives_slider.setValue(self.game_settings.get('lives'))
            self.enemy_speed_dropdown.set_selected(self.game_settings.get('enemy.speed'))
            self.enemy_bullet_speed_dropdown.set_selected(self.game_settings.get('enemy.bullet.speed'))
            self.player_speed_dropdown.set_selected(self.game_settings.get('player.speed'))
            self.player_bullet_speed_dropdown.set_selected(self.game_settings.get('player.bullet.speed'))
            self.enemy_spawn_slider.setValue(self.game_settings.get('enemy.spawn'))
            self.player_heal_amount_slider.setValue(self.game_settings.get('player.heal'))
            self.set_toggle_state(self.health_bonus_toggle, self.game_settings.get('bonus.health'))
            self.set_toggle_state(self.lives_bonus_toggle, self.game_settings.get('bonus.lives'))
            self.set_toggle_state(self.shield_bonus_toggle, self.game_settings.get('bonus.shield'))
            self.set_toggle_state(self.slow_bonus_toggle, self.game_settings.get('bonus.slow'))
 
    def create_sliders(self):
        self.hp_slider, self.hp_output = self.create_slider(WIDTH-1000, HEIGHT-580, 10, 150, 10, 100)
        self.lives_slider, self.lives_output = self.create_slider(WIDTH-1000, HEIGHT-530, 1, 15, 1, 10)
        self.enemy_spawn_slider, self.enemy_spawn_output = self.create_slider(WIDTH-900, HEIGHT-280, 1, 10, 1, 3)
        self.player_heal_amount_slider, self.player_heal_amount_output = self.create_slider(WIDTH-930, HEIGHT-230, 0, 40, 10, 20)
    
    def update_slider_values(self):
        self.hp_output.setText(self.hp_slider.getValue())
        self.lives_output.setText(self.lives_slider.getValue())
        self.enemy_spawn_output.setText(self.enemy_spawn_slider.getValue())
        self.player_heal_amount_output.setText(self.player_heal_amount_slider.getValue())
    
    def create_slider(self, x, y, min_val, max_val, step, default_val):
        slider = Slider(self.WIN, x, y, 300, 20, min=min_val, max=max_val, step=step,
                        colour=(50, 50, 50), handleColour=(255, 0, 0), handleRadius=10)
        slider.setValue(default_val)
        output = TextBox(self.WIN, x + 320, y - 10, 50, 40, fontSize=20, borderColour=(200, 200, 200), textColour=(0, 0, 0), radius=10)
        output.disable()
          
        return slider, output
    
    def create_dropdowns(self):
        self.enemy_speed_dropdown = self.create_dropdown([COLOR_INACTIVE, COLOR_ACTIVE], [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], WIDTH-1000, HEIGHT-495, 290, 40, 
                                                         self.info_font, "Select Enemy Speed", ['Slow', 'Medium', 'Fast'])
        
        self.enemy_bullet_speed_dropdown = self.create_dropdown([COLOR_INACTIVE, COLOR_ACTIVE], [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], WIDTH-950, HEIGHT-445, 290, 40, 
                                                         self.info_font, "Select Enemy Bullet Speed", ['Slow', 'Medium', 'Fast'])
        
        self.player_speed_dropdown = self.create_dropdown([COLOR_INACTIVE, COLOR_ACTIVE], [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], WIDTH-1000, HEIGHT-395, 290, 40, 
                                                         self.info_font, "Select Player Speed", ['Slow', 'Medium', 'Fast'])
        
        self.player_bullet_speed_dropdown = self.create_dropdown([COLOR_INACTIVE, COLOR_ACTIVE], [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], WIDTH-950, HEIGHT-345, 290, 40, 
                                                         self.info_font, "Select Player Bullet Speed", ['Slow', 'Medium', 'Fast'])
        
    def create_dropdown(self, color_menu, color_option, x, y, width, height, font, text, options):
        dropdown = DropDown(color_menu, color_option, x, y, width, height, font=font, selected=text, options=options)

        return dropdown
    
    def draw_dropdowns(self):
        self.player_bullet_speed_dropdown.draw(self.WIN)
        self.player_speed_dropdown.draw(self.WIN)
        self.enemy_bullet_speed_dropdown.draw(self.WIN)
        self.enemy_speed_dropdown.draw(self.WIN)

    def create_toggles(self):
        self.health_bonus_toggle = self.create_toggle(WIDTH-963, HEIGHT-135, 35, 10)
        self.lives_bonus_toggle = self.create_toggle(WIDTH-893, HEIGHT-135, 38, 10)
        self.shield_bonus_toggle = self.create_toggle(WIDTH-827, HEIGHT-135, 40, 10)
        self.slow_bonus_toggle = self.create_toggle(WIDTH-753, HEIGHT-135, 38, 10)
    
    def create_toggle(self, x, y, width, height, on_color=pygame.Color('lightgreen'), off_color=pygame.Color('lightcoral'), border_color=pygame.Color('black')):
        toggle = Toggle(
            self.WIN, x, y, width, height,
            colour=off_color, borderColour=border_color,
            onColour=on_color, startOn=True
        )

        return toggle

    def init_settings_labels(self):
        self.title_label = self.result_font.render("Settings", 1, (255,255,255))
        self.hp_label = self.info_font.render("Max HP:", 1, (255,255,255))
        self.lives_label = self.info_font.render("Max Lives:", 1, (255,255,255))
        self.enemy_vel_label = self.info_font.render("Enemy Speed:", 1, (255,255,255))
        self.enemy_shoot_vel_label = self.info_font.render("Enemy Bullet Speed:", 1, (255,255,255))
        self.player_vel_label = self.info_font.render("Player Speed:", 1, (255,255,255))
        self.player_shoot_vel_label = self.info_font.render("Player Bullet Speed:", 1, (255,255,255))
        self.enemy_spawn_label = self.info_font.render("Enemy Spawn Increase:", 1, (255,255,255))
        self.heal_amount_label = self.info_font.render("Player Heal Amount:", 1, (255,255,255))
        self.bonuses_label = self.info_font.render("Avaliable Bonuses:", 1, (255,255,255))
        self.leave_label = self.info_font2.render("Press ESC to return to main menu and save settings", 1, (128,128,128))
    
    def draw_settings_menu(self):
        self.WIN.blit(self.title_label, (WIDTH/2 - self.title_label.get_width()/2, 0))
        self.WIN.blit(self.hp_label, (WIDTH - 1160, HEIGHT - 590))
        self.WIN.blit(self.lives_label, (WIDTH - 1160, HEIGHT - 540))
        self.WIN.blit(self.enemy_vel_label, (WIDTH - 1160, HEIGHT - 490))
        self.WIN.blit(self.enemy_shoot_vel_label, (WIDTH - 1160, HEIGHT - 440))
        self.WIN.blit(self.player_vel_label, (WIDTH - 1160, HEIGHT - 390))
        self.WIN.blit(self.player_shoot_vel_label, (WIDTH - 1160, HEIGHT - 340))
        self.WIN.blit(self.enemy_spawn_label, (WIDTH - 1160, HEIGHT - 290))
        self.WIN.blit(self.heal_amount_label, (WIDTH - 1160, HEIGHT - 240))
        self.WIN.blit(self.bonuses_label, (WIDTH - 1160, HEIGHT - 190))
        self.WIN.blit(self.leave_label, (WIDTH/2 - self.leave_label.get_width()/2, 710))
        self.WIN.blit(HEALTH_BONUS, (WIDTH - 970, HEIGHT - 195))
        self.WIN.blit(LIVES_BONUS, (WIDTH - 900, HEIGHT - 195))
        self.WIN.blit(SHIELD_BONUS, (WIDTH - 830, HEIGHT - 195))
        self.WIN.blit(SLOW_BONUS, (WIDTH - 760, HEIGHT - 195))

        self.draw_settings_buttons()
    
    def draw_settings_buttons(self):
        self.EASY_BUTTON = Button(pos=(WIDTH-1000, HEIGHT-640), text_input="EASY", font=self.get_font(35), base_color="#2590c4", hovering_color="Green")
        self.MEDIUM_BUTTON = Button(pos=(WIDTH/2, HEIGHT-640), text_input="MEDIUM", font=self.get_font(35), base_color="#2590c4", hovering_color="Green")
        self.HARD_BUTTON = Button(pos=(WIDTH-200, HEIGHT-640), text_input="HARD", font=self.get_font(35), base_color="#2590c4", hovering_color="Green")
        self.RESET_BUTTON = Button(pos=(WIDTH-100, HEIGHT-30), text_input="RESET", font=self.get_font(35), base_color="#2590c4", hovering_color="Green")
        
        for button in [self.EASY_BUTTON, self.MEDIUM_BUTTON, self.HARD_BUTTON, self.RESET_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.WIN)
    
    def change_values(self, hp_value, lives_value, enemy_spawn_value, player_heal_value, hp_bonus, lives_bonus, shield_bonus, slow_bonus, 
                      enemy_speed_value, enemy_bullet_value, player_speed_value, player_bullet_value):
        self.hp_slider.setValue(hp_value)
        self.lives_slider.setValue(lives_value)
        self.enemy_spawn_slider.setValue(enemy_spawn_value)
        self.player_heal_amount_slider.setValue(player_heal_value)
        self.set_toggle_state(self.health_bonus_toggle, hp_bonus)
        self.set_toggle_state(self.lives_bonus_toggle, lives_bonus)
        self.set_toggle_state(self.shield_bonus_toggle, shield_bonus)
        self.set_toggle_state(self.slow_bonus_toggle, slow_bonus)
        self.enemy_speed_dropdown.set_selected(enemy_speed_value)
        self.enemy_bullet_speed_dropdown.set_selected(enemy_bullet_value)
        self.player_speed_dropdown.set_selected(player_speed_value)
        self.player_bullet_speed_dropdown.set_selected(player_bullet_value)

    def set_toggle_state(self, toggle, state):
        current_state = toggle.getValue()
        if state and not current_state:
            toggle.toggle()
        elif not state and current_state:
            toggle.toggle()

    def handle_settings_menu_events(self):
        for event in pygame.event.get():
            self.handle_dropdown_events(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_settings()
                    GAME_MUSIC.stop()
                    self.main_menu(music_off=True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_settigns_click()
    
    def save_settings(self):
        self.game_settings = {
            'player.hp': self.hp_slider.getValue(),
            'lives': self.lives_slider.getValue(),
            'enemy.speed': "Medium" if self.enemy_speed_dropdown.get_selected() not in ["Slow", "Medium", "Fast"] else self.enemy_speed_dropdown.get_selected(),
            'enemy.bullet.speed': "Medium" if self.enemy_bullet_speed_dropdown.get_selected() not in ["Slow", "Medium", "Fast"] else self.enemy_bullet_speed_dropdown.get_selected(),
            'player.speed': "Medium" if self.player_speed_dropdown.get_selected() not in ["Slow", "Medium", "Fast"] else self.player_speed_dropdown.get_selected(),
            'player.bullet.speed': "Medium" if self.player_bullet_speed_dropdown.get_selected() not in ["Slow", "Medium", "Fast"] else self.player_bullet_speed_dropdown.get_selected(),
            'enemy.spawn': self.enemy_spawn_slider.getValue(),
            'player.heal': self.player_heal_amount_slider.getValue(),
            'bonus.health': self.health_bonus_toggle.value,
            'bonus.lives': self.lives_bonus_toggle.value,
            'bonus.shield': self.shield_bonus_toggle.value,
            'bonus.slow': self.slow_bonus_toggle.value
        }
    
        with open('data/game_settings.txt', 'w') as f:
            json.dump(self.game_settings, f)
    
    def handle_dropdown_events(self, event):
        dropdowns = [
            self.enemy_speed_dropdown,
            self.enemy_bullet_speed_dropdown,
            self.player_speed_dropdown,
            self.player_bullet_speed_dropdown
        ]

        for dropdown in dropdowns:
            selected_option = dropdown.update(event)
            if selected_option is not None and selected_option >= 0:
                dropdown.set_selected(dropdown.options[selected_option])
    
    def handle_settigns_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.EASY_BUTTON.checkForInput(mouse_pos):
            self.change_values(150, 15, 2, 40, True, True, True, True, "Slow", "Slow", "Fast", "Fast")
        elif self.MEDIUM_BUTTON.checkForInput(mouse_pos):
            self.change_values(100, 10, 4, 20, True, False, True, True, "Medium", "Medium", "Medium", "Medium")
        elif self.HARD_BUTTON.checkForInput(mouse_pos):
            self.change_values(100, 5, 7, 10, False, False, False, False, "Fast", "Fast", "Slow","Slow")
        elif self.RESET_BUTTON.checkForInput(mouse_pos):
            self.change_values(100, 10, 3, 20, True, True, True, True, "Medium", "Medium", "Medium", "Medium")

    def info_menu(self):
        run = True
        while run:
            self.move_bg()
            self.draw_info_menu()
            self.handle_info_menu_events()
            pygame.display.update()

    def draw_info_menu(self):
        self.draw_info_menu_images()
        self.draw_info_text()

    def draw_info_menu_images(self):
        self.WIN.blit(RED_SPACE_SHIP, (WIDTH - 1250, HEIGHT-650))
        self.WIN.blit(BLUE_SPACE_SHIP, (WIDTH - 1190, HEIGHT - 550))
        self.WIN.blit(GREEN_SPACE_SHIP, (WIDTH - 1190, HEIGHT - 500))
        self.WIN.blit(ORANGE_SPACE_SHIP, (WIDTH - 1178, HEIGHT - 445))
        self.WIN.blit(PINK_SPACE_SHIP, (WIDTH - 1230, HEIGHT - 405))
        self.WIN.blit(HEALTH_BONUS, (WIDTH - 1190, HEIGHT - 160))
        self.WIN.blit(LIVES_BONUS, (WIDTH - 990, HEIGHT - 155))
        self.WIN.blit(SHIELD_BONUS, (WIDTH - 780, HEIGHT - 160))
        self.WIN.blit(SLOW_BONUS, (WIDTH - 480, HEIGHT - 160))
        self.WIN.blit(ALIEN, (WIDTH - 210, HEIGHT-200))
        self.WIN.blit(SCENE, (WIDTH - 250, 0))
        
    def draw_info_text(self):
        title_label = self.end_font.render("About the game", 1, (255,255,255))
        red_inv_info_label = self.info_font2.render("- HP: 1 hit to destroy, SPAWN: from 1 level, HIT PROBABILITY: Low, POINTS: 150", 1, (255,0,0))
        blue_inv_info_label = self.info_font2.render("- HP: 2 hits to destroy, SPAWN: from 2 level, HIT PROBABILITY: High, POINTS: 200", 1, (0,0,255))
        green_inv_info_label = self.info_font2.render("- HP: 1 hit to destroy, SPAWN: from 3 level, HIT PROBABILITY: High, POINTS: 250", 1, (0,255,0))
        orange_inv_info_label = self.info_font2.render("- HP: 2 hits to destroy, SPAWN: from 4 level, HIT PROBABILITY: Medium, POINTS: 300", 1, (255,102,0))
        pink_inv_info_label = self.info_font2.render("- HP: 3 hits to destroy, SPAWN: from 5 level, HIT PROBABILITY: Medium, POINTS: 350", 1, (252,15,192))
        score_info_label = self.info_font2.render("• Score - player earns points for each level complete based on its difficulty and for every destroyed enemy", 1, (231,232,228))
        lives_info_label = self.info_font2.render("• Lives - player lose one of his lives each time enemy gets to your base(bottom screen)", 1, (231,232,228))
        hp_info_label = self.info_font2.render("• HP - player loses health each time when players ship gets hit based on enemy's damage", 1, (231,232,228))
        saving_info_label = self.info_font2.render("• Saving Game - player can save his full game state by pressing ESC and choosing 'Save Game' option", 1, (231,232,228))
        settings_info_label = self.info_font2.render("• Game Settings - player can customize game proccess by clicking Settings icon in Main Menu", 1, (231,232,228))
        hp_bonus_info_label = self.info_font2.render(" - heals 20 hp", 1, (237,238,224))
        lives_bonus_info_label = self.info_font2.render(" - adds 1 lives", 1, (237,238,224))
        shield_bonus_info_label = self.info_font2.render(" - protects from 1 shot", 1, (237,238,224))
        slow_bonus_info_label = self.info_font2.render(" - slows game for 10 sec", 1, (237,238,224))
        game_info_label = self.info_font2.render("=> Defend your base from different waves of space invaders by shooting them(SPACE button) <= ", 1, (226,228,208))
        game_info_label2 = self.info_font2.render("Avoid their lasers(w/a/s/d) unless your ship will be destroyed. Good luck!:) P.S ESC - Pause", 1, (226,228,208))
        leave_info_label = self.info_font2.render("Press ESC to return to main menu :)", 1, (128,128,128))
        
        self.WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 10))
        self.WIN.blit(leave_info_label, (WIDTH/2 - leave_info_label.get_width()/2 - 50, 710))
        self.WIN.blit(red_inv_info_label, (WIDTH - 1100, HEIGHT - 590))
        self.WIN.blit(blue_inv_info_label, (WIDTH - 1100, HEIGHT - 540))
        self.WIN.blit(green_inv_info_label, (WIDTH - 1100, HEIGHT - 490))
        self.WIN.blit(orange_inv_info_label, (WIDTH - 1100, HEIGHT - 435))
        self.WIN.blit(pink_inv_info_label, (WIDTH - 1100, HEIGHT - 380))
        self.WIN.blit(score_info_label, (WIDTH - 1190, HEIGHT - 330))
        self.WIN.blit(lives_info_label, (WIDTH - 1190, HEIGHT - 297))
        self.WIN.blit(hp_info_label, (WIDTH - 1190, HEIGHT - 262))
        self.WIN.blit(saving_info_label, (WIDTH - 1190, HEIGHT - 228))
        self.WIN.blit(settings_info_label, (WIDTH - 1190, HEIGHT - 195))
        self.WIN.blit(hp_bonus_info_label, (WIDTH - 1140, HEIGHT - 152))
        self.WIN.blit(lives_bonus_info_label, (WIDTH - 930, HEIGHT - 152))
        self.WIN.blit(shield_bonus_info_label, (WIDTH - 720, HEIGHT - 152))
        self.WIN.blit(slow_bonus_info_label, (WIDTH - 420, HEIGHT - 152))
        self.WIN.blit(game_info_label, (WIDTH - 1190, HEIGHT - 100))
        self.WIN.blit(game_info_label2, (WIDTH - 1170, HEIGHT - 70))

    def handle_info_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GAME_MUSIC.stop()
                    self.main_menu(music_off=True)

    def end_menu(self, score):
        player_score = score
        top_scores = self.read_top_scores()
        rank = self.find_score_row(score)
        self.end_menu_loop(player_score, top_scores, rank)

    def end_menu_loop(self, player_score, top_scores, rank):
        run = True
        while run:
            self.WIN.blit((BG), (0,0))
            self.draw_end_menu(player_score, top_scores, rank)
            self.handle_end_menu_events()
            pygame.display.update()

    def draw_end_menu(self, player_score, top_scores, rank):
        labels = [
            (self.info_font, "Press ENTER to play", (128,128,128), (WIDTH/2, 680)),
            (self.info_font, "Press ESC for Main Menu", (128,128,128), (WIDTH/2, 710)),
            (self.end_font, "Game Over", (255,0,0), (WIDTH/2, 10)),
            (self.top_font, f"Your rank: {rank}", (0,255,0), (WIDTH/2, 580)),
            (self.result_font, f"Your Score: {player_score}", (255,255,255), (WIDTH/2, 170)),
            (self.top_font, "Top Scores ", (255,255,255), (WIDTH/2, 240))
        ]
        
        for font, text, color, pos in labels:
            label = font.render(text, 1, color)
            self.WIN.blit(label, (pos[0] - label.get_width()/2, pos[1]))

        self.WIN.blit(AWARD, (WIDTH - 740, HEIGHT - 425))
        self.WIN.blit(PLANET, (WIDTH - 1150, HEIGHT - 620))
        self.WIN.blit(ROCKET, (WIDTH - 300, HEIGHT - 300))
        
        font = pygame.font.Font('font/my_font.ttf', 50)
        for i, score in enumerate(top_scores):
            text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
            self.WIN.blit(text, (WIDTH/2-80, 320 + i*50)) 

    def handle_end_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main_menu()
                elif event.key == pygame.K_RETURN: 
                    game = Game()
                    game.run_game()

    def move_bg(self):
        self.bg_y
        self.WIN.blit(BG, (0, self.bg_y))
        self.WIN.blit(BG, (0, self.bg_y - HEIGHT)) 

        self.bg_y += 0.25

        if self.bg_y >= HEIGHT:
            self.bg_y = 0