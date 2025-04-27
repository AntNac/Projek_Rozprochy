import pygame
import math

class Box:
    def __init__(self, id, startx, starty, hp):
        self.id = id
        self.hp = hp
        self.x = startx
        self.y = starty
        self.size = 15
        self.alive = True

    def draw(self, g):
        pygame.draw.rect(g, (100, 0, 0), (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2))

    def get_hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            return True  # dead
        return False
