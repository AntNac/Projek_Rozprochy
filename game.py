import random
import pygame
import math
from network import Network
from player import Player
from canvas import Canvas
from box import Box
from bullet import Bullet

class Game:
    pygame.init()

    def __init__(self):
        self.net = Network()
        self.width = 1920
        self.height = 1080
        self.player = Player(random.randint(0, 1920), random.randint(0, 1080), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.player2 = Player(random.randint(0, 1920), random.randint(0, 1080), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.canvas = Canvas("Testing...")
        self.Players = [self.player, self.player2]
        self.Boxes = []

    def start(self):
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            self.player.recovery_health()
            self.player2.recovery_health()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    self.player.shot(mouse_pos[0], mouse_pos[1])

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.player.move(0)
            if keys[pygame.K_LEFT]:
                self.player.move(1)
            if keys[pygame.K_UP]:
                self.player.move(2)
            if keys[pygame.K_DOWN]:
                self.player.move(3)

            self.canvas.draw_background()

            self.player.hitBoxesList = []

            for bullet in self.player.bulletList:
                bullet.update()
                if bullet.active:
                    bullet.draw(self.canvas.get_canvas())
                else:
                    self.player.bulletList.remove(bullet)

            for bullet in self.player2.bulletList:
                bullet.update()
                if bullet.active:
                    bullet.draw(self.canvas.get_canvas())
                else:
                    self.player2.bulletList.remove(bullet)

            for box in self.Boxes:
                for bullet in self.player.bulletList:
                    distance = math.hypot(bullet.x - box.x, bullet.y - box.y)
                    if distance <= box.size:
                        bullet.active = False
                        self.player.hitBoxesList.append(box.id)

            data = self.parse_data(self.send_data())
            self.Boxes = data[6]

            self.player2.update(*data[:6])

            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())

            for box in self.Boxes:
                if box.alive:
                    box.draw(self.canvas.get_canvas())

            self.canvas.update()

        pygame.quit()

    def send_data(self):
        color = self.player.color
        bullet_data = ";".join(f"{b.x},{b.y},{b.endx},{b.endy}" for b in self.player.bulletList)
        hitbox_data = ";".join(f"{id}" for id in self.player.hitBoxesList)
        box_data = ";".join(f"{b.id},{b.x},{b.y},{b.hp}" for b in self.Boxes)
        data = (
            f"{self.net.id}:{self.player.x},{self.player.y},{self.player.level},"
            f"{color[0]},{color[1]},{color[2]},{self.player.hp}|{bullet_data}|{hitbox_data}#{box_data}"
        )
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            if "#" in data:
                main_data, boxes_data = data.split("#")
            else:
                main_data = data
                boxes_data = ""

            if "|" in main_data:
                player_part, bullets_part, _ = main_data.split("|")
            else:
                player_part = main_data
                bullets_part = ""

            d = player_part.split(":")[1].split(",")
            x = int(d[0])
            y = int(d[1])
            level = int(d[2])
            color = (int(d[3]), int(d[4]), int(d[5]))
            hp = int(d[6])

            bullets = []
            if bullets_part:
                for bullet in bullets_part.split(";"):
                    bullet_data = bullet.split(",")
                    if len(bullet_data) == 4:
                        bx, by, ex, ey = [int(float(b)) for b in bullet_data]
                        bullets.append(Bullet(bx, by, ex, ey))

            boxes = []
            if boxes_data:
                for box in boxes_data.split(";"):
                    box_data = box.split(",")
                    if len(box_data) == 4 and all(b != '' for b in box_data):
                        id, bx, by, hp = [int(float(b)) for b in box_data]
                        if hp > 0:
                            boxes.append(Box(id, bx, by, hp))

            return x, y, level, color, hp, bullets, boxes

        except Exception as e:
            print("Parse error:", e)
            return 0, 0, 1, (255, 0, 0), 100, [], []
