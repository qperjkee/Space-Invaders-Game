import pygame


class DropDown():
    def __init__(self, color_menu, color_option, x, y, w, h, font, selected, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.selected = selected
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.border_radius = 3

    def draw(self, surf):
        self.draw_rounded_rect(surf, self.rect, self.color_menu[self.menu_active])

        msg = self.font.render(self.selected, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
    
    def draw_rounded_rect(self, surf, rect, color):
        pygame.draw.rect(surf, color, rect.inflate(-self.border_radius * 2, -self.border_radius * 2))
        pygame.draw.circle(surf, color, (rect.left + self.border_radius, rect.top + self.border_radius), self.border_radius)
        pygame.draw.circle(surf, color, (rect.right - self.border_radius, rect.top + self.border_radius), self.border_radius)
        pygame.draw.circle(surf, color, (rect.left + self.border_radius, rect.bottom - self.border_radius), self.border_radius)
        pygame.draw.circle(surf, color, (rect.right - self.border_radius, rect.bottom - self.border_radius), self.border_radius)

        pygame.draw.rect(surf, color, (rect.left + self.border_radius, rect.top, rect.width - self.border_radius * 2, rect.height))
        pygame.draw.rect(surf, color, (rect.left, rect.top + self.border_radius, rect.width, rect.height - self.border_radius * 2))

    def update(self, event):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            option_rect = self.rect.copy()
            option_rect.y += (i + 1) * self.rect.height
            if option_rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                return self.active_option
    
    def set_selected(self, value):
        self.selected = value
    
    def get_selected(self):
        return self.selected

