import pygame
import random
import threading
import tkinter as tk

# functions
# function for spawning obstacles, powerups, etc.
def spawn_thread():
    global running, spawnning, obstacle_sprites, powerup_sprites, settings
    clock = pygame.time.Clock()
    while running:
        while spawnning and settings == False:
            obs = obstacle(random.choice(obstacle_imges))
            obstacle_sprites.add(obs)
            # every once in a while a powerup will spawn
            if random.randint(0, 100) < 5:
                pw = powerup()
                powerup_sprites.add(pw)
            clock.tick(1)
        clock.tick(1)

# function for applying settings
def apply(window):
    global settings
    settings = False
    window.destroy()

# function for settings window
def settings_window():
    window = tk.Tk()
    window.title("Settings")
    window.geometry("300x300")
    window.resizable(False, False)
    label = tk.Label(window, text="Settings")
    label.pack()
    frame = tk.Frame(window)
    frame.pack()
    button = tk.Button(frame, text="Apply", command=lambda: apply(window))
    button.grid(row=0, column=0)
    # settings will be added later on
    window.mainloop()

# classes
# class for player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = playerImg
        self.rect = self.img.get_rect()
        self.rect.x = 370
        self.rect.y = 480
        self.speed = 2
        self.x_change = 0
        self.y_change = 0

    def move(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
    
    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

# class for obstacles
class obstacle(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.rect = img.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = 0 - obstacleImg.get_height()
        self.image = img

    def move(self, change):
        self.rect.y += change

# class for powerups
class powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = powerupImg.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = 0 - powerupImg.get_height()
        self.image = random.choice(powerupsImgs)
    def move(self, change):
        self.rect.y += change

# Initializing the game
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Stormy Seas")
icon = pygame.image.load("boat.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
setting_img = pygame.transform.scale(pygame.image.load("settings.png"), (64, 64))

# Player
playerImg = pygame.transform.scale(pygame.image.load("boat.png"), (64, 64))
player = Player()

# Obstacle
obstacleImg = pygame.transform.scale(pygame.image.load("stone.png"), (64, 64))
obstacleImg2 = pygame.transform.scale(pygame.image.load("glacier.png"), (64, 64))
obstacleImg3 = pygame.transform.scale(pygame.image.load("stone2.png"), (64, 64))
obstacle_imges = [obstacleImg, obstacleImg2, obstacleImg3]
obstacle_sprites = pygame.sprite.Group()

# Powerup
# I will add distinct powerup images later on
powerupImg = pygame.transform.scale(pygame.image.load("boat.png"), (64, 64))
powerupsImgs = [powerupImg]
powerup_sprites = pygame.sprite.Group()

# setting up a new thread for handling the spawning of obstacles and enemies and powerups
spawn_thread = threading.Thread(target=spawn_thread)

# main loop
running = True
spawnning = True
settings = False
screen_speed = 1
while running:
    # starting the spawning thread
    if not spawn_thread.is_alive():
        spawn_thread.start()
    # making background blue
    screen.fill((0, 0, 255))
    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.x_change = -player.speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.x_change = player.speed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.y_change = -player.speed
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.y_change = player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player.x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player.y_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            # checking if the settings button is clicked
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                if x > 800 - setting_img.get_width() and y < setting_img.get_height():
                    settings = True
                    settings_window()

    # moving player
    player.move()

    # checking boundaries for player
    if player.rect.x < 0:
        player.rect.x = 0
    elif player.rect.x > 800 - playerImg.get_width():
        player.rect.x = 800 - playerImg.get_width()
    if player.rect.y < 0:
        player.rect.y = 0
    elif player.rect.y > 600 - playerImg.get_height():
        player.rect.y = 600 - playerImg.get_height()
    
    # drawing and moving obstacles
    obstacle_sprites.draw(screen)
    for obs in obstacle_sprites:
        obs.move(screen_speed)

    # drawing and moving powerups
    powerup_sprites.draw(screen)
    for powerup in powerup_sprites:
        powerup.move(screen_speed)

    # drawing player
    player.draw()

    # drawing settings button
    screen.blit(setting_img, (800 - setting_img.get_width(), 0))

    # checking for collision between player and obstacles
    for obs in obstacle_sprites:
        if player.rect.colliderect(obs.rect):
            obstacle_sprites.remove(obs)
            print("collision")
    
    # checking for collision between player and powerups
    for powerup in powerup_sprites:
        if player.rect.colliderect(powerup.rect):
            powerup_sprites.remove(powerup)
            print("powerup collected")

    clock.tick(60)
    pygame.display.update()

spawnning = False
pygame.quit()