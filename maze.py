#створи гру "Лабіринт"!

import pygame


width = 800
height = 600
size = (width,height)
FPS = 60

window = pygame.display.set_mode(size)

background = pygame.transform.scale(
    pygame.image.load("background.jpg"),
size
)

clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x,y, speed):
        self.image = pygame.transform.scale(
                pygame.image.load(image),
                (65,80)  
        )        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_UP]:
            if self.rect.y > 0:
                self.rect.y -=self.speed
            else:
                self.rect.y = height-75

        if key_pressed[pygame.K_DOWN]:
            if self.rect.y < height-85:
                self.rect.y +=self.speed
            else:
                self.rect.y = 0

        if key_pressed[pygame.K_RIGHT]:
            if self.rect.x < width-70:
                self.rect.x +=self.speed
            else:
                self.rect.x = 0

        if key_pressed[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -=self.speed
            else:
                self.rect.x = width-60


class Enemy(GameSprite):
    direction = "left"

    def update(self):
        
        if self.rect.x <= width/2+100:
            self.direction = "right"
        elif self.rect.x >= width-70:
            self.direction = "left"
        
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        
class Wall(pygame.sprite.Sprite):
    def __init__(self, r, g, b,  x,y, length, width ):
        super().__init__()
        self.color = (r, g, b)
        self.rect = pygame.Rect(x,y, length, width)

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)



gold = GameSprite("treasure.png", width-100, height-100,0)
player = Player("hero.png",100, 500, 5)
enemy = Enemy("cyborg.png", width-80, 280, 4)


test_wall = Wall(255,107,12, 100,100, 10,500)
walls = [
    Wall(255,107,12, 200,100, 500,10),
    Wall(255,107,12, 300,350, 10,300),
    #Wall(255,107,12, 300,100, 10,200),
    Wall(255,107,12, 200,100, 10,150),
    Wall(255, 0, 0,   0,0,    10,500),
    Wall(0,0,255,    400,300,  10,500),



]

pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

kick = pygame.mixer.Sound("kick.ogg")
money = pygame.mixer.Sound("money.ogg")

game_over = False

finish = False

pygame.font.init()
font1 = pygame.font.Font(None, 70)
text_win = font1.render("Ти переміг!!!", True, (0,0,255))
text_lose = font1.render("Ти програв....", True, (255,0,0))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if not finish:
        window.blit(background, (0,0))
        player.update()
        player.reset()
        
        enemy.reset()
        enemy.update()

        gold.reset()
        for w in walls:
            w.draw()



    if pygame.sprite.collide_rect(player, gold):
        finish = True
        window.blit(text_win, (width/3, height/3))
        money.play()

    wall_collision = any(pygame.sprite.collide_rect(player, w) for w in walls)
    if pygame.sprite.collide_rect(player, enemy) or wall_collision:
        finish = True
        window.blit(text_lose, (width/3, height/3))
        kick.play()




    pygame.display.update()
    clock.tick(FPS)