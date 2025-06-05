import os
import random
import sys
import argparse
from time import sleep
import pygame

parser = argparse.ArgumentParser(description='A simple game made by Mathys Penson')

group = parser.add_mutually_exclusive_group()
group.add_argument("-fs", "--fullscreen", action="store_true", help="Enable fullscreen mode (default)")
group.add_argument("-w", "--windowed", action="store_true", help="Enable windowed mode")

parser.add_argument("-r", "--resolution", type=str, help="The screen resolution in WIDTH:HEIGHT format (e.g., 1920:1080)")
parser.add_argument("-l", "--limit", type=float, help="What is the limit of the falling speed (default 18)")
args = parser.parse_args()

pygame.init()

mode = "windowed"
if args.windowed:
    mode = "windowed"
elif args.fullscreen:
    mode = "fullscreen"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

maxFallSpeed = 18

if args.resolution:
    try:
        width, height = args.resolution.split(":")
        SCREEN_WIDTH, SCREEN_HEIGHT = int(width), int(height)
    except ValueError:
        print("❌ Invalid resolution format. Use WIDTH:HEIGHT (e.g., 1920:1080).")
        sys.exit(1)
elif mode == "fullscreen":
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

if args.limit:
    try:
        maxFallSpeed = args.limit
    except ValueError:
        print("❌ Invalid limit fall speed.")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)


class Paddle:
    def __init__(self, x, y, width=(SCREEN_WIDTH // 8), height=(SCREEN_HEIGHT // 100), ):
        self.x = x
        self.y = y
        self.screen = screen
        self.width = width
        self.height = height
        self.sprite = None

        self.centerPaddle()

    def centerPaddle(self):
        self.x = SCREEN_WIDTH / 2 - self.width / 2
        self.y = SCREEN_HEIGHT - 50
        self.draw()

    def draw(self):
        self.sprite = pygame.draw.rect(self.screen, Colors.white, (self.x, self.y, self.width, self.height),
                                       border_radius=0, border_top_left_radius=-1, border_bottom_right_radius=-1,
                                       border_top_right_radius=-1, border_bottom_left_radius=-1)

    def moveLeft(self):
        self.x -= self.width / 10
        if self.x < 0:
            self.x = 0
        self.draw()

    def moveRight(self):
        self.x += self.width / 10
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        self.draw()


class Block:
    def __init__(self, width, height):
        self.x = random.randint(0, SCREEN_WIDTH - 1)
        self.y = 10
        self.width = width
        self.height = height
        self.screen = screen
        self.fallspeed = 2
        self.sprite = None
        self.rect = None
        self.velocity = pygame.math.Vector2(0, self.fallspeed)
        self.angle = 90.00

    def draw(self):
        self.sprite = pygame.draw.rect(self.screen, Colors.blue, (self.x, self.y, self.width, self.height))

    def fall(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()

        if self.y + self.height > SCREEN_HEIGHT:
            gameOver()

    def updateFallSpeed(self):
        if self.fallspeed >= maxFallSpeed:
            self.fallspeed = maxFallSpeed
        else:
            self.fallspeed += .5

    def changeSpeed(self, direction):
        if direction == "up":
            self.updateFallSpeed()
        else:
            if self.fallspeed > 2:
                self.fallspeed -= 0.25
        self.velocity = self.velocity.normalize() * self.fallspeed

    def checkCollision(self, collisionItem):
        if self.sprite.colliderect(collisionItem.sprite):
            return True
        return False

    def reset(self):
        self.angle = 90.00
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.velocity = pygame.math.Vector2(1, 0).rotate(self.angle) * self.fallspeed
        self.y = 10
        self.fallspeed = 2
        self.draw()

    def rebounce(self, distanceFromMiddle):
        self.updateFallSpeed()
        maxAfwijking = 45
        norm = distanceFromMiddle / (paddle.width / 2)
        angle = 270 - norm * maxAfwijking
        self.angle = angle
        self.velocity = pygame.math.Vector2(1, 0).rotate(angle) * self.fallspeed

    def rebounceFromScreen(self, axis):
        if axis == 'x':
            self.velocity.x = -self.velocity.x
        elif axis == 'y':
            self.velocity.y = -self.velocity.y
        self.angle = self.velocity.angle_to(pygame.math.Vector2(1, 0))
        self.updateFallSpeed()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catching the falling blocks")

clock = pygame.time.Clock()
smallFont = pygame.font.SysFont("comicsans", 20)
font = pygame.font.SysFont("comicsans", 30)

runScript = True
paddle = Paddle(10, 10)
block = Block(10, 10)


def startupFrame():
    screen.fill(Colors.black)
    text = font.render("This game has been made by Mathys Penson", True, Colors.red)
    screen.blit(text, (((SCREEN_WIDTH - text.get_width()) / 2), SCREEN_HEIGHT / 2))
    link = smallFont.render('https://github.com/mattplaygamez/fallingBlocks', True, Colors.red)
    screen.blit(link, (((SCREEN_WIDTH - link.get_width()) / 2), (SCREEN_HEIGHT / 2)+50))

    pygame.display.update()
    sleep(2)


def gameOver():
    global showText
    showText = False

    screen.fill(Colors.blue)

    text = font.render("Your final score is: " + str(score), True, Colors.white)
    screen.blit(text, (((SCREEN_WIDTH - text.get_width()) / 2), SCREEN_HEIGHT / 2))

    text = smallFont.render("Press ENTER to restart", True, Colors.white)
    screen.blit(text, (((SCREEN_WIDTH - text.get_width()) / 2), (SCREEN_HEIGHT / 2) + 50))

    pygame.display.flip()

score = 0
showText = True
startupFrame()
while __name__ == "__main__" and runScript:
    didBounce = False

    screen.fill(Colors.black)
    paddle.draw()
    block.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runScript = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                screen.fill(Colors.black)
                score = 0
                block.reset()
                paddle.centerPaddle()
                runScript = True
                showText = True
            elif event.key == pygame.K_UP:
                block.changeSpeed("up")
            elif event.key == pygame.K_DOWN:
                block.changeSpeed("down")
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_RALT:
                score += 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft()
    elif keys[pygame.K_RIGHT]:
        paddle.moveRight()


    block.fall()
    if block.checkCollision(paddle) and not didBounce:
        distanceFromMiddle = (paddle.x + (paddle.width / 2)) - (block.x + block.width / 2)
        block.rebounce(distanceFromMiddle)
        score += 1
        didBounce = True

    if not didBounce:
        if block.x <= 0:
            block.rebounceFromScreen('x')
            didBounce = True
        elif block.x + block.width >= SCREEN_WIDTH:
            block.rebounceFromScreen('x')
            didBounce = True
        elif block.y <= 0:
            block.rebounceFromScreen('y')
            didBounce = True


    if showText:
        scoreText = font.render("Score: " + str(score), True, Colors.green)
        screen.blit(scoreText, (10, 10))

        scoreText = font.render("Your fall speed is: " + str(round(block.fallspeed, 2)), True, Colors.green)
        screen.blit(scoreText, ((SCREEN_WIDTH - scoreText.get_width() - 5), 10))

    pygame.display.update()
    clock.tick(60)
