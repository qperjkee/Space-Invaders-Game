import pygame
from .constants import BONUS_TYPES


class Bonus:
    def __init__(self, x=0, y=0, bonus_type=None, avaliable_bonuses={}):
        self.x = x
        self.y = y
        self.bonus_type = bonus_type
        self.bonus_img = BONUS_TYPES.get(bonus_type) if bonus_type in BONUS_TYPES else None
        self.mask = None if not self.bonus_img else pygame.mask.from_surface(self.bonus_img)
        self.show_bonus = True if avaliable_bonuses else False
        self.avaliable_bonuses = avaliable_bonuses

    def set_bonuses(self, health=True, lives=True, shield=True, slow=True):
        self.avaliable_bonuses = {}
        if health:
            self.avaliable_bonuses["health"] = BONUS_TYPES["health"]
        if lives:
            self.avaliable_bonuses["lives"] = BONUS_TYPES["lives"]
        if shield:
            self.avaliable_bonuses["shield"] = BONUS_TYPES["shield"]
        if slow:
            self.avaliable_bonuses["slow"] = BONUS_TYPES["slow"]

    def move(self, vel):
        self.y += vel
    
    def draw(self, window):
        if self.bonus_img:
            window.blit(self.bonus_img, (self.x, self.y))
    
    def get_height(self):
        return self.bonus_img.get_height() if self.bonus_img else 0
    
    def apply_bonus(self, player, game, max_lives):
        if self.bonus_type  == "health":
            player.add_hp(20)
        elif self.bonus_type  == "lives":
            game.lives = min(game.lives + 1, max_lives)
        elif self.bonus_type  == "slow":
            game.apply_slow_effect()
        elif self.bonus_type  == "shield":
            player.activate_shield()