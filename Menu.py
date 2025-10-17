from button import Button
from const import *

class Menu:
    def __init__(self, screen):
        self.screen = screen 
    def draw(self):
        for button in self.buttons: button.draw(self.screen)
    def update(self):
        for button in self.buttons: button.update()