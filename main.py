import pygame
import random
import threading
import tkinter as tk

# functions
# function for spawning obstacles, powerups, etc.
def spawn_thread():
    global running, spawnning, obstacle_sprites, powerup_sprites, settings, player, game_over
    clock = pygame.time.Clock()
    while running:
        while spawnning and settings == False and game_over == False:
            obs = obstacle(random.choice(obstacle_imges))
            obstacle_sprites.add(obs)
            # every once in a while a powerup will spawn
            if random.randint(0, 100) < 5:
                pw = powerup()
                powerup_sprites.add(pw)
            # adding a point every second
            player.points += 1
            clock.tick(1)
        clock.tick(1)

# function for applying settings
def apply(window):
    global settings
    settings = False
    window.destroy()

# function for restarting the game
def restart_game():
    global player, obstacle_sprites, powerup_sprites
    player = Player()
    obstacle_sprites = pygame.sprite.Group()
    powerup_sprites = pygame.sprite.Group()


# function for game over screen
def game_over_screen():
    global running, spawnning, game_over
    spawnning = False
    game_over = True
    while game_over:
        screen.fill((255, 255, 255))
        text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(text, (800/2-text.get_width()/2, 600/2-text.get_height()/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    restart_game()
                else:
                    running = False
                    game_over = False
        pygame.display.update()

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
        self.health = 3
        self.shield = False
        self.points = 0
        self.upgrade_level = 1
        self.firing_rate = 0

    def move(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
    
    def upgrade(self):
        self.image = pygame.transform.scale(pygame.image.load('boat{self.update_level}.png'), (64, 64))
        self.rect = self.image.get_rect()
        # will be enhanced later on
        if self.upgrade_level == 1:
            self.firing_rate = 1
        elif self.upgrade_level == 2:
            self.firing_rate = 2
        elif self.upgrade_level == 3:
            self.firing_rate = 3
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
        self.image = random.choice(powerupsImgs)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = 0 - self.image.get_height()
        if self.image == powerupImg_speed:
            self.type = "speed"
        elif self.image == powerupImg_health:
            self.type = "health"
        elif self.image == powerupImg_shield:
            self.type = "shield"
        elif self.image == powerupImg_points:
            self.type = "points"
        elif self.image == powerupImg_upgrade:
            self.type = "upgrade"
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
powerupImg_speed = pygame.transform.scale(pygame.image.load("boat.png"), (64, 64))
powerupImg_health = pygame.transform.scale(pygame.image.load("boat.png"), (64, 64))
powerupImg_shield = pygame.transform.scale(pygame.image.load("boat.png"), (64, 64))
powerupImg_points = pygame.transform.scale(pygame.image.load("boat.png"), (64, 64))
powerupImg_upgrade = pygame.transform.scale(pygame.image.load("boat.png"), (64, 64))
powerupsImgs = [powerupImg_speed, powerupImg_health, powerupImg_shield, powerupImg_points, powerupImg_upgrade]
powerup_sprites = pygame.sprite.Group()

# setting up a new thread for handling the spawning of obstacles and enemies and powerups
spawn_thread = threading.Thread(target=spawn_thread)

# main loop
running = True
spawnning = True
settings = False
screen_speed = 1
font = pygame.font.Font(None, 36)
entering_menu = True
game_over = False
while running:

    # entering menu
    while entering_menu:
        screen.fill((255, 255, 255))
        text = font.render("Press any key to start", True, (0, 0, 0))
        screen.blit(text, (800/2-text.get_width()/2, 600/2-text.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                entering_menu = False
            if event.type == pygame.KEYDOWN:
                entering_menu = False

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
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_r:
                restart_game()
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

    # drawing points
    text = font.render(str(player.points), True, (0, 0, 0))
    screen.blit(text, (800/2-text.get_width()/2, 0))

    # drawing health
    text = font.render("Health: "+str(player.health), True, (0, 0, 0))
    screen.blit(text, (800/2 + 800/4-text.get_width()/2, 0))

    # checking for collision between player and obstacles
    for obs in obstacle_sprites:
        if player.rect.colliderect(obs.rect):
            obstacle_sprites.remove(obs)
            player.health -= 1
            if player.health == 0:
                game_over_screen()
    
    # checking for collision between player and powerups
    for powerup in powerup_sprites:
        if player.rect.colliderect(powerup.rect):
            powerup_sprites.remove(powerup)
            if powerup.type == "speed":
                screen_speed += 0.2
            elif powerup.type == "health":
                player.health += 1
            elif powerup.type == "shield":
                player.shield = True
            elif powerup.type == "points":
                player.points += 10
            elif powerup.type == "upgrade":
                player.upgrade()

    clock.tick(60)
    pygame.display.update()

spawnning = False
pygame.quit()