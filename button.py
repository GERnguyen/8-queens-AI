import pygame
import sys

class Button:
    def __init__(self, x, y, width, height, text, 
                 color=(100, 100, 100), 
                 hover_color=(150, 150, 150),
                 select_color=(50, 50, 50),
                 text_color=(255, 255, 255),
                 font_size = 25):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.select_color = select_color
        self.text_color = text_color
        self.border_radius = 10
        self.font_size = font_size
        self.font = pygame.font.Font('MontserratRegular-BWBEl.ttf', font_size)
        
        self.is_hovered = False
        self.is_pressed = False
        self.is_selected = False
    
    def get_current_color(self):
        if self.is_pressed:
            return self.select_color
        elif self.is_hovered:
            return self.hover_color
        else:
            return self.color
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  
        
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered and mouse_pressed:
            self.is_pressed = True
        else:
            if self.is_pressed and not mouse_pressed and self.is_hovered:
                self.is_selected = True
            self.is_pressed = False
    
    def draw(self, screen):
        current_color = self.get_current_color()
        self.font = pygame.font.Font('MontserratRegular-BWBEl.ttf', self.font_size)
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)
        
        border_color = (200, 200, 200) if self.is_hovered else (100, 100, 100)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=self.border_radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        text_rect.move_ip(0, -2)
        if self.is_pressed:
            text_rect.move_ip(2, 2) 
            
        screen.blit(text_surface, text_rect)
    
    def is_Selected(self):
        if self.is_selected:
            self.is_selected = False
            return True
        return False
