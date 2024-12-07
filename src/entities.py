import pygame
from .constants import HEIGHT, WIDTH, YELLOW_LASER, YELLOW_SPACE_SHIP, GREEN_LASER, ORANGE_LASER, WIN, COLOR_MAP, LASER_OFFSETS, POINTS_EARNED
from .laser import Laser


class Ship:
    COOLDOWN = 20
    def __init__(self, x, y, health=100, ship_img=None, laser_img=None):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = ship_img
        self.laser_img = laser_img
        self.lasers = []
        self.cool_down_counter = 0
        self.max_health = 100

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if obj.has_shield == False:
                    if laser.img in [GREEN_LASER, ORANGE_LASER]:
                        obj.health -= 20
                    else:
                        obj.health -= 10
                else:
                    obj.deactivate_shield()
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN :
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width() if self.ship_img else 0
    
    def get_height(self):
        return self.ship_img.get_height() if self.ship_img else 0


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health, YELLOW_SPACE_SHIP, YELLOW_LASER)
        self.mask = pygame.mask.from_surface(self.ship_img) if self.ship_img else None
        self.max_health = health
        self.has_shield = False
        self.heal_amount = 20

    def draw(self, window):
        self.draw_healthbar(window)
        super().draw(window)

    def move_lasers(self, vel, objs, game):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 100
                        if obj.health <= 0:
                            objs.remove(obj)
                            game.score += obj.points
                        if laser in self.lasers:
                            self.lasers.remove(laser)
   
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+15, self.y+10, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def add_hp(self, heal=None):
        if not heal:
            self.health += self.heal_amount
        else:
            self.health += heal
        while self.health > self.max_health:
            self.health -= 10
    
    def activate_shield(self):
        self.has_shield = True
    
    def deactivate_shield(self):
        self.has_shield = False

    def draw_healthbar(self, window):
        main_font = pygame.font.SysFont("comicsans", 20)
        hp_label = main_font.render(f"HP: ", 1, (255,255,255))
        WIN.blit(hp_label, (WIDTH - 1190, HEIGHT-35))
        pygame.draw.rect(window, (255,0,0), (45, HEIGHT-24, 80, 10))
        pygame.draw.rect(window, (0,255,0), (45, HEIGHT-24, 80 * (self.health/self.max_health), 10))
        if self.has_shield:
            pygame.draw.rect(window, (255,215,0), (45, HEIGHT-24, 80, 10))


class Enemy(Ship):
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.color = color
        if self.color in ["blue", "orange"]:
            self.health = 200
        elif self.color == "pink":
            self.health = 300
        self.max_health = health
        self.ship_img, self.laser_img = COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.points = POINTS_EARNED[color]

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            offset_x, offset_y = LASER_OFFSETS.get(self.ship_img, LASER_OFFSETS["default"])

            laser = Laser(self.x + offset_x, self.y + offset_y, self.laser_img)
            self.lasers.append(laser)

            self.cool_down_counter = 1
    
    def draw_health(self, window):
        if self.color == "blue":
            pygame.draw.rect(window, (255,0,0), (self.x + 13, self.y, self.ship_img.get_width() - 22, 5))
            pygame.draw.rect(window, (0,255,0), (self.x + 13, self.y, (self.ship_img.get_width() - 46) * (self.health/self.max_health), 5))
        elif self.color == "orange":
            pygame.draw.rect(window, (255,0,0), (self.x, self.y - 9, self.ship_img.get_width(), 5))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y - 9, (self.ship_img.get_width() - 22) * (self.health/self.max_health), 5))
        elif self.color == "pink":
            pygame.draw.rect(window, (255,0,0), (self.x + 42, self.y + 6, self.ship_img.get_width() - 81, 5))
            pygame.draw.rect(window, (0,255,0), (self.x + 42, self.y + 6, (self.ship_img.get_width() - 127) * (self.health/self.max_health), 5))
