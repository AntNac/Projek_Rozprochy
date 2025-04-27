import pygame
import math

class Box:
    def __init__(self, startx, starty,hp):
        self.hp = hp
        self.x = startx
        self.y = starty
        self.size = 15
        self.alive=True

    def draw(self,g):
        pygame.draw.rect(g,(100,0,0),(self.x - self.size, self.y - self.size, self.size * 2,self.size * 2))

    def getting_hit(self, BulletsList, oponent):
        for bullet in BulletsList:
            distance = math.hypot(bullet.x - self.x, bullet.y - self.y)
            if distance <= self.size:
                bullet.active = False
                self.hp -= oponent.damage
                if self.hp <= 0:
                    self.alive = False
                    oponent.level_up()