import pygame
import sys
from pygame.locals import *
import math
from random import uniform


class Pong:
    def __init__(self):

        self.screen = pygame.display.set_mode((800, 600))

        pygame.font.init()
        self.font = pygame.font.Font("pongFont.TTF", 50)

        self.ball = pygame.Rect(400, 300, 5, 5)
        self.ballAngle = math.radians(0)
        self.ballSpeed = 10.0

        # mechanics
        self.playerScore = 0
        self.opponentScore = 0

        # direction of ball
        self.direction = -1

        self.playerRects = {
            -60: pygame.Rect(50, 380, 10, 20),  # Bottom of paddle
            -45: pygame.Rect(50, 360, 10, 20),
            -30: pygame.Rect(50, 340, 10, 20),
            -0: pygame.Rect(50, 320, 10, 20),
            30: pygame.Rect(50, 300, 10, 20),
            45: pygame.Rect(50, 280, 10, 20),
            60: pygame.Rect(50, 260, 10, 20),  # Top of paddle
        }

        self.opponentRects = {
            -60: pygame.Rect(750, 380, 10, 20),  # Bottom of paddle
            -45: pygame.Rect(750, 360, 10, 20),
            -30: pygame.Rect(750, 340, 10, 20),
            -0: pygame.Rect(750, 320, 10, 20),
            30: pygame.Rect(750, 300, 10, 20),
            45: pygame.Rect(750, 280, 10, 20),
            60: pygame.Rect(750, 260, 10, 20),  # Top of paddle
        }

        self.colors_list = [
            (255, 0, 0),
            (0, 0, 255),
            (255, 0, 255),
            (255, 255, 0),
            (0, 255, 255)
        ]
        self.pause = 10

    ############################
    #                          #
    #       Draw objects       #
    #                          #
    ############################

    def drawColorsHits(self, target):
        for tRect in target:
            pygame.draw.rect(self.screen, (0, 0, 0), target[tRect])

    def drawBall(self):
        return pygame.draw.rect(self.screen, (255, 255, 255), self.ball)

    def drawPlayers(self):
        for pRect in self.playerRects:
            pygame.draw.rect(self.screen, (255, 255, 255), self.playerRects[pRect])

        for oRect in self.opponentRects:
            pygame.draw.rect(self.screen, (255, 255, 255), self.opponentRects[oRect])


    ############################
    #                          #
    #      Updates objects     #
    #                          #
    ############################

    def updateBall(self):
        self.ball.x += self.direction * self.ballSpeed * math.cos(self.ballAngle)
        self.ball.y += self.direction * self.ballSpeed * -math.sin(self.ballAngle)

        if self.ball.x > 800 or self.ball.x < 0:
            if self.ball.x > 800:
                self.playerGetScore()

            elif self.ball.x < 0:
                self.enemyGetScore()

            pygame.display.flip()
            pygame.time.wait(1000)
            self.ball.x = 400
            self.ball.y = 300
            self.ballAngle = math.radians(0)
            if self.opponentScore >= 11 or self.playerScore >= 11:
                self.opponentScore = 0
                self.playerScore = 0
            return

        if self.direction < 0:
            for pRect in self.playerRects:
                if self.playerRects[pRect].colliderect(self.ball):
                    self.ballAngle = math.radians(pRect)
                    self.direction = 1
                    break

        else:
            for oRect in self.opponentRects:
                if self.opponentRects[oRect].colliderect(self.ball):
                    self.ballAngle = math.radians(oRect)
                    self.direction = -1

    def updatePlayer(self):
        key = pygame.key.get_pressed()

        if self.ball.y <= 0 or self.ball.y > 595:
            self.ballAngle *= -1

        if key[K_UP]:
            if self.playerRects[60].y > 0:
                for pRect in self.playerRects:
                    self.playerRects[pRect].y -= 5

        elif key[K_DOWN]:
            if self.playerRects[-60].y < 590:
                for pRect in self.playerRects:
                    self.playerRects[pRect].y += 5

    def updateOpponent(self):

        # TODO remove enemy shake
        if self.ball.y > self.opponentRects[0].y:
            if self.opponentRects[-60].y > 580:
                return
            for oRect in self.opponentRects:
                self.opponentRects[oRect].y += 6

        elif self.ball.y < self.opponentRects[0].y:
            if self.opponentRects[60].y <= 0:
                return
            for oRect in self.opponentRects:
                self.opponentRects[oRect].y -= 6


    ############################
    #                          #
    #      Updates objects     #
    #                          #
    ############################

    def color_random(self):
        return int(uniform(0, len(self.colors_list) - 1))

    def displayColorChange(self):
        self.screen.fill(self.colors_list[self.color_random()])

    def playerGetScore(self):
        self.displayColorChange()
        self.playerScore += 1
        self.screen.blit(self.font.render(str(self.playerScore), -1, (0, 0, 0)), (200, 25))
        self.drawColorsHits(self.playerRects)

    def enemyGetScore(self):
        self.displayColorChange()
        self.opponentScore += 1
        self.screen.blit(self.font.render(str(self.opponentScore), -1, (0, 0, 0)), (600, 25))
        self.drawColorsHits(self.opponentRects)

    ############################
    #                          #
    #     Run motherfucka!     #
    #                          #
    ############################

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((50, 150, 100))
            clock.tick(60)
            # print('FPS: {}'.format(int(clock.get_fps())))
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            self.drawBall()
            self.screen.blit(self.font.render(str(self.playerScore), -1, (255, 255, 255)), (200, 25))
            self.screen.blit(self.font.render(str(self.opponentScore), -1, (255, 255, 255)), (600, 25))
            self.drawPlayers()
            self.updatePlayer()
            self.updateOpponent()
            self.updateBall()
            pygame.display.flip()


if __name__ == '__main__':
    Pong().run()
