import pygame
from bullet import *

class Player():
    def __init__(self, startx, starty, color):
        self.level=1
        self.hp=100
        self.max_hp=100
        self.damage=5
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.color = color
        self.size=15
        self.health_recovery_delay = 700
        self.time_prev=pygame.time.get_ticks()
        self.range=400
        self.bulletList = []

    def update(self,x, y, level, color, hp, bullets):
        self.x = x
        self.y = y
        self.level = level
        self.color = color
        self.hp = hp
        self.size=15+2*(self.level-1)
        self.velocity-=self.level//5
        self.damage=5+(self.level-1)
        self.max_hp = 100 + (self.level - 1) * 10
        self.bulletList = bullets

    def level_up(self):
        if self.level<25:
            self.level += 1
            self.size += 2
            self.max_hp+=10
            self.damage+=1
        if self.level%5==0 and self.velocity>1:
            self.velocity-=1

    def recovery_health(self):
        if self.chcek_health_recovery_delay() and self.hp<self.max_hp:
            self.hp+=1

    def chcek_health_recovery_delay(self):
        time_now=pygame.time.get_ticks()
        if time_now - self.time_prev>self.health_recovery_delay:
            self.time_prev=time_now
            return True

    def getting_hit(self,OponentBulletList,damage):
        for bullet in OponentBulletList:
            if math.sqrt((bullet.x-self.x)**2 + (bullet.y-self.y)**2) < self.size:
                bullet.active=False
                self.hp-=damage


    def draw(self, g):
        pygame.draw.circle(g, self.color ,(self.x, self.y), self.size)
        font = pygame.font.SysFont('Arial', 16)
        text_surface = font.render(f"Lv: {self.level}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x, self.y - self.size - 22))

        pygame.draw.rect(g, (0,0,0), (self.x-self.size, self.y - self.size - 12, self.size * 2, 11),1)
        hp_ratio = self.hp / self.max_hp
        hp_width = int((self.size * 2) * hp_ratio)-2
        pygame.draw.rect(g, (0, 255, 0), (self.x - self.size+1, self.y - self.size - 11, hp_width, 9))

        g.blit(text_surface, text_rect)

    def end_point(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        length = math.hypot(dx, dy)

        dx /= length
        dy /= length

        endx = self.x + dx * self.range
        endy = self.y + dy * self.range

        return endx, endy

    def shot(self, target_x, target_y):
        endp=self.end_point(target_x,target_y)
        bullet = Bullet(self.x, self.y, endp[0], endp[1])
        self.bulletList.append(bullet)

    def move(self, dirn):
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity