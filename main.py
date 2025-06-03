import random
import pygame
import sys
import os
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

score = 0


class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)


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
        self.sprite = pygame.draw.rect(self.screen, Colors.white, (self.x, self.y, self.width, self.height), border_radius=0, border_top_left_radius=-1, border_bottom_right_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1)
    def moveLeft(self):
        self.x -= self.width / 2
        print("Moving Left")
        self.draw()

    def moveRight(self):
        self.x += self.width / 2
        print("Moving Right")
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

    def draw(self):
        self.sprite = pygame.draw.rect(self.screen, Colors.blue, (self.x, self.y, self.width, self.height))

    def fall(self):
        self.y += self.fallspeed
        self.draw()

        if self.y > SCREEN_HEIGHT:
            gameOver()

    def changeSpeed(self, direction):
        if direction == "up":
            self.fallspeed += 0.25
        else:
            if self.fallspeed > 2:
                self.fallspeed -= 0.25
                

    def checkCollision(self, collisionItem):
        if self.sprite.colliderect(collisionItem.sprite):
            print("Collision detected")
            return True
        return False

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH - 1)
        self.y = 10
        self.fallspeed += 0.25
        self.draw()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catching the falling blocks")

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30)

runScript = True
paddle = Paddle(10, 10)
block = Block( 10, 10)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

raw_image = pygame.image.load(resource_path("Flag.png"))
background_image = pygame.transform.scale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def gameOver():
    global showText
    showText = False

    screen.blit(background_image, (0, 0))

    text = font.render("Your final score is: " + str(score), True, Colors.white)
    screen.blit(text, (((SCREEN_WIDTH - text.get_width()) / 2), SCREEN_HEIGHT / 2))

    pygame.display.flip()
showText = True
while __name__ == "__main__" and runScript:


    screen.fill(Colors.black)
    paddle.draw()
    block.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runScript = False
            pygame.quit()
            sys.exit()

        # check if arrows are pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.moveLeft()
            elif event.key == pygame.K_RIGHT:
                paddle.moveRight()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP:
                block.changeSpeed("up")
            elif event.key == pygame.K_DOWN:
                block.changeSpeed("down")


    block.fall()
    if block.checkCollision(paddle):
        score += 1
        block.reset()

    if showText:

        score_text = font.render("Score: " + str(score), True, Colors.green)
        screen.blit(score_text, (10, 10))

        score_text = font.render("Your fall speed is: " + str(block.fallspeed), True, Colors.green)
        screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width() - 5), 10))


    pygame.display.update()
    clock.tick(60)
