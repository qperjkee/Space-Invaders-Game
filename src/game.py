import pygame, sys, random, json, time
from .constants import WIDTH, HEIGHT, BG, PAUSE_ICON, SHOOT_TIMING, COLLIDE_DAMAGE, ENEMY_SPEED_VALUES, ENEMY_BULLET_SPEED_VALUES, PLAYER_SPEED_VALUES, PLAYER_BULLET_SPEED_VALUES
from .utils import collide
from .entities import Player, Enemy
from .level import Level
from .laser import Laser
from .button import Button
from .menu_handler import MenuHandler
from .bonus import Bonus


class Game:
    def __init__(self, data = {}, settings = {}, load = False):
        pygame.init()
        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.run = True
        self.lives = self.max_lives = 10
        self.score = 0
        self.bg_y = 0
        self.lost = False
        self.data = data
        self.load = load

        self.enemies = []
        self.normal_enemy_vel = self.enemy_vel = 1
        self.normal_enemy_laser_vel = self.enemy_laser_vel = 5

        self.player_vel = 4.25
        self.player_laser_vel = 5

        self.player = Player(WIDTH / 2, 630)
        self.level = Level()

        self.bonus = Bonus()
        self.bonus.set_bonuses()

        self.init_game()
        self.menu_handler = MenuHandler()

        self.load_ui()

        self.normal_bonus_vel = self.bonus_vel = self.enemy_vel + 0.3
        self.remaining_slow_time = 0

        self.init_enemies_options()

        if self.load:
            self.load_game()
            self.redraw_window()
            self.pause_game()

        if not self.load:
            self.game_settings = settings
            self.load_game_settings()
    
    def init_enemies_options(self):
        self.LASERS_SPEED = {
            "orange": self.enemy_laser_vel + 1.5,
            "default": self.enemy_laser_vel
        }
    
    def load_ui(self):
        self.main_font = pygame.font.SysFont("comicsans", 50)
        self.end_font = pygame.font.Font('font/my_font.ttf', 60)

        self.SAVE_BUTTON = Button(pos=(WIDTH/2, 30), text_input="Save Game", font=self.end_font, base_color=(153,0,153), hovering_color="Green")
        self.MENU_BUTTON = Button(pos=(WIDTH/2, HEIGHT-35), text_input="Main Menu", font=self.end_font, base_color=(153,0,153), hovering_color="Green")
    
    def update_scores(self, score):
        with open('data/scores.txt', 'a') as file:
            file.write(str(score) + '\n')
        self.sort_and_save_scores()

    def sort_and_save_scores(self):
        with open('data/scores.txt', 'r') as file:
            scores = sorted([int(line.strip()) for line in file], reverse=True)
        with open('data/scores.txt', 'w') as file:
            for score in scores:
                file.write(str(score) + '\n')
    
    def load_game_settings(self):  
        if self.game_settings is not None and len(self.game_settings) != 0:
            self.player.health = self.player.max_health = self.game_settings.get('player.hp')

            self.lives = self.max_lives = self.game_settings.get('lives')

            self.normal_enemy_vel = self.enemy_vel = ENEMY_SPEED_VALUES.get(self.game_settings.get('enemy.speed'), 1)
            self.normal_enemy_laser_vel = self.enemy_laser_vel = ENEMY_BULLET_SPEED_VALUES.get(self.game_settings.get('enemy.bullet.speed'), 5)
            
            self.player_vel = PLAYER_SPEED_VALUES.get(self.game_settings.get('player.speed'), 4.25)
            self.player_laser_vel = PLAYER_BULLET_SPEED_VALUES.get(self.game_settings.get('player.bullet.speed'), 5)

            self.level.wave_growth = self.game_settings.get('enemy.spawn')
            
            self.player.heal_amount = self.game_settings.get('player.heal')

            self.bonus.set_bonuses(self.game_settings.get('bonus.health'), self.game_settings.get('bonus.lives'), 
                                   self.game_settings.get('bonus.shield'), self.game_settings.get('bonus.slow'))
            
            self.normal_bonus_vel = self.bonus_vel = self.enemy_vel + 0.3
    
    def load_game(self):
        self.game_settings = self.data.get('game.settings')
        self.load_game_settings()

        self.level.level = self.data.get('level', 1)
        self.level.wave_length = self.data.get('level.wave', 5)

        if self.lives >= self.data.get('lives', 10):
            self.lives = self.data.get('lives')

        self.score = self.data.get('score')
        self.player.x = self.data.get('player.x')
        self.player.y = self.data.get('player.y')

        if self.player.health >= self.data.get('player.health', 100):
            self.player.health = self.data.get('player.health', 100)

        self.player.has_shield = self.data.get('player.shield', False)

        for laser_pos in self.data.get('player.lasers', []):
            x, y = laser_pos
            laser = Laser(x, y, self.player.laser_img)
            self.player.lasers.append(laser)
        
        for enemy_data in self.data.get('enemies', []):
            enemy = Enemy(enemy_data['x'], enemy_data['y'], enemy_data['color'])
            enemy.health = enemy_data['health']
            enemy.lasers = [Laser(x, y, enemy.laser_img) for x, y in enemy_data['lasers']]
            self.enemies.append(enemy)
        
        self.bonus = Bonus(self.data.get('bonus.x', 0), self.data.get('bonus.y', 0), self.data.get('bonus.type'), self.bonus.avaliable_bonuses)
        self.remaining_slow_time = self.data.get('slow.effect.time.remain', 0)
        self.bonus.show_bonus = self.data.get('show.bonus', False)
        
        if self.remaining_slow_time > 0:
                self.apply_slow_effect(self.remaining_slow_time)

    def init_game(self):
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
    
    def save_game_data(self):
        self.enemies_data = []
        for enemy in self.enemies:
            enemy_data = {
                'x': enemy.x,
                'y': enemy.y,
                'color': enemy.color,
                'health': enemy.health,
                'lasers': [(laser.x, laser.y) for laser in enemy.lasers]
            }
            self.enemies_data.append(enemy_data)
        
        self.data = {
            'level': self.level.level,
            'level.wave': self.level.wave_length,
            'score': self.score,
            'lives': self.lives,
            'player.x': self.player.x,
            'player.y': self.player.y,
            'player.shield': self.player.has_shield,
            'player.health': self.player.health,
            'player.lasers': [(laser.x, laser.y) for laser in self.player.lasers],
            'enemies': self.enemies_data,
            'bonus.x': self.bonus.x,
            'bonus.y': self.bonus.y,
            'bonus.type': self.bonus.bonus_type,
            'show.bonus': self.bonus.show_bonus,
            'slow.effect.time.remain': self.remaining_slow_time,
            'game.settings': self.game_settings
        }

    def pause_game(self):
        paused = True

        while paused:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.SAVE_BUTTON.checkForInput(mouse_pos):
                        self.save_game_data()
                        with open('data/game_phase.txt', 'w') as f:
                            json.dump(self.data, f)
                    elif self.MENU_BUTTON.checkForInput(mouse_pos):
                        self.menu_handler.show_main_menu()
                        

            for button in [self.SAVE_BUTTON, self.MENU_BUTTON]:
                button.changeColor(pygame.mouse.get_pos())
                button.update(self.WIN)

            self.WIN.blit(PAUSE_ICON, (WIDTH / 2 - 100, HEIGHT / 2 - 100))
            pygame.display.update()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def redraw_window(self):
        self.WIN.blit(BG, (0, self.bg_y))
        self.WIN.blit(BG, (0, self.bg_y - HEIGHT))

        self.bg_y += 0.25

        if self.bg_y >= HEIGHT:
            self.bg_y = 0

        lives_label = self.main_font.render(f"Lives: {self.lives}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"Level: {self.level.level}", 1, (255, 255, 255))

        self.WIN.blit(lives_label, (WIDTH - 1190, HEIGHT - 740))
        self.WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, HEIGHT - 740))

        for enemy in self.enemies:
            enemy.draw(self.WIN)
            enemy.draw_health(self.WIN)

        if self.bonus.show_bonus:        
            self.bonus.draw(self.WIN)

        self.player.draw(self.WIN)

        if self.lost:
            self.update_scores(round(self.score))
            self.menu_handler.show_end_menu(self.score)
        pygame.display.update()
    
    def update_level(self):
        self.level.increase_level()
        self.player.add_hp()
        self.score = self.level.add_score(self.score)
        self.enemies = self.level.create_enemies(self.enemies, WIDTH)
        if self.bonus.avaliable_bonuses:
            self.bonus = self.level.create_bonus(WIDTH, self.bonus)
    
    def proccess_keys(self):
        if (self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]) and self.player.x > -30:  # left
            self.player.x -= self.player_vel
        if (self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]) and self.player.x + self.player_vel + self.player.get_width() < WIDTH + 30:  # right
            self.player.x += self.player_vel
        if (self.keys[pygame.K_w] or self.keys[pygame.K_UP]) and self.player.y - self.player_vel > 0:  # up
            self.player.y -= self.player_vel
        if (self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]) and self.player.y + self.player_vel + self.player.get_height() + 15 < HEIGHT + 15:  # down
            self.player.y += self.player_vel
        if self.keys[pygame.K_SPACE]:
            self.player.shoot()
    
    def process_enemy(self, enemy):
        self.ENEMIES_SPEED = {
            "default": self.enemy_vel,
            "green": self.enemy_vel - 0.1,
            "orange": self.enemy_vel - 0.1,
            "pink": self.enemy_vel - 0.2
        }
        
        speed = self.ENEMIES_SPEED.get(enemy.color, self.ENEMIES_SPEED["default"])

        enemy.move(speed)

        self.laser_speed = self.LASERS_SPEED.get(enemy.color, self.LASERS_SPEED["default"])

        enemy.move_lasers(self.laser_speed, self.player)

        self.multiplier, self.fps_bonus = SHOOT_TIMING.get(enemy.color, (1, 0))

        if random.randrange(0, self.multiplier * (self.FPS + self.fps_bonus)) == 1:
            enemy.shoot()

        if collide(enemy, self.player):
            if self.player.has_shield == False:
                damage = COLLIDE_DAMAGE.get(enemy.color, COLLIDE_DAMAGE["default"])
                self.player.health -= damage
                self.enemies.remove(enemy)
                self.score += enemy.points
            else:
                self.player.deactivate_shield()
                self.enemies.remove(enemy)
                self.score += enemy.points

        elif enemy.y + enemy.get_height() > HEIGHT + 30:
            self.lives -= 1
            self.enemies.remove(enemy)
    
    def process_bonus(self):
        self.bonus.move(self.bonus_vel)

        if self.bonus.y + self.bonus.get_height() > HEIGHT + 30:
            self.bonus.show_bonus = False
        
        if self.bonus.show_bonus:
            if collide(self.player, self.bonus):
                self.bonus.apply_bonus(self.player, self, self.max_lives)
                self.bonus.show_bonus = False
    
    def apply_slow_effect(self, remaining_time=None):
        if remaining_time is None:
            self.remaining_slow_time = 10
        else:
            self.remaining_slow_time = remaining_time

        self.enemy_vel = self.normal_enemy_vel * 0.5
        self.enemy_laser_vel = self.normal_enemy_laser_vel * 0.5
        self.bonus_vel = self.normal_bonus_vel * 0.5
        self.update_lasers_speed()
        self.slow_effect_start = time.time()

    def check_slow_effect(self):
        if self.remaining_slow_time > 0:
            elapsed_time = time.time() - self.slow_effect_start
            self.remaining_slow_time -= elapsed_time
            self.slow_effect_start = time.time() 

        if self.remaining_slow_time <= 0:
            self.enemy_vel = self.normal_enemy_vel
            self.enemy_laser_vel = self.normal_enemy_laser_vel
            self.bonus_vel = self.normal_bonus_vel
            self.update_lasers_speed()
            self.remaining_slow_time = 0
    
    def update_lasers_speed(self):
        self.LASERS_SPEED = {
            "orange": self.enemy_laser_vel + 1.5,
            "default": self.enemy_laser_vel
        }

    def run_game(self):
        while self.run:
            self.clock.tick(self.FPS)
            self.redraw_window()

            if self.lives <= 0 or self.player.health <= 0:
                self.lost = True
                self.run = False
                self.redraw_window()

            if len(self.enemies) == 0:
                self.update_level()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()

            self.keys = pygame.key.get_pressed()
            self.proccess_keys()

            for enemy in self.enemies[:]:
                self.process_enemy(enemy)
            
            if self.level.level > 1:
                self.process_bonus()
                self.check_slow_effect()

            self.player.move_lasers(-self.player_laser_vel, self.enemies, self)