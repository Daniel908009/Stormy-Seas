import pygame
import random
import threading
import tkinter as tk
from pygame import mixer

# functions
# function for spawning obstacles, powerups, etc.
def spawn_thread():
    global running, spawnning, obstacle_sprites, powerup_sprites, settings, player, game_over, chance_of_powerup, powerups_not_allowed
    clock = pygame.time.Clock()
    waiting_time = 0
    while running:
        #print("Spawning")
        while spawnning and settings == False and game_over == False:
            obs = obstacle(random.choice(obstacle_imges))
            obstacle_sprites.add(obs)
            if player.can_fire == False and player.no_fire_limit == False:
                waiting_time += 1
                if waiting_time == player.firing_rate:
                    player.can_fire = True
                    waiting_time = 0
                    print("Can fire")
            # every once in a while a powerup will spawn
            if random.randint(0, 100) < chance_of_powerup and powerups_not_allowed == False:
                pw = Powerup()
                powerup_sprites.add(pw)
            # adding a point every second
            player.points += 1
            clock.tick(1)
        clock.tick(1)

# function for restarting the game
def restart_game():
    global player, obstacle_sprites, powerup_sprites
    player = Player()
    obstacle_sprites = pygame.sprite.Group()
    powerup_sprites = pygame.sprite.Group()


# function for game over screen
def game_over_screen():
    global running, spawnning, game_over, width, height
    spawnning = False
    game_over = True
    can_exit = 0
    while game_over:
        screen.fill((255, 255, 255))
        text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(text, (width/2-text.get_width()/2, height/2-text.get_height()/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                running = False
            # checking for restart or exit and also ensuring that the player cant misclick
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    spawnning = True
                    game_over = False
                    restart_game()
                elif can_exit >= 600:
                    running = False
                    game_over = False
            
        if can_exit < 600:
            can_exit += 1
        clock.tick(60)
        pygame.display.update()

# function for applying settings
def apply(window, health, speed, upgrade, invincible, powerup, enemy, reload, enemies, sound, music, powerups, mode):
    global settings, setting_health, setting_speed, setting_upgrade, no_fire_limit, sounds_allowed, music_allowed, powerups_not_allowed, game_mode, chance_of_powerup
    if health != "":
        setting_health = int(health)
    if speed != "":
        setting_speed = int(speed)
    if upgrade != "":
        setting_upgrade = int(upgrade)
    if invincible:
        player.invincible = True
    else:
        player.invincible = False
    if powerup != "":
        chance_of_powerup = int(powerup)
    if reload:
        no_fire_limit = True
    else:
        no_fire_limit = False
    if sound:
        sounds_allowed = True
    else:
        sounds_allowed = False
    if music:
        music_allowed = True
    else:
        music_allowed = False
    if powerups:
        powerups_not_allowed = True
    else:
        powerups_not_allowed = False
    if mode != "":
        game_mode = mode
    settings = False
    window.destroy()
    restart_game()

# function for settings window
# currently for some reason when called it doesnt respond, will fix later though
def settings_window():
    global setting_health, setting_speed, setting_upgrade, player, chance_of_powerup, no_fire_limit, sounds_allowed, music_allowed, powerups_not_allowed, game_mode
    window = tk.Tk()
    window.title("Settings")
    window.geometry("500x500")
    window.resizable(False, False)
    #window.iconbitmap("")
    label = tk.Label(window, text="Settings")
    label.pack()
    frame = tk.Frame(window)
    frame.pack()
    # health number setting
    health_label = tk.Label(frame, text="Health:")
    health_label.grid(row=0, column=0)
    e1 = tk.StringVar()
    e1.set(setting_health)
    health_entry = tk.Entry(frame, textvariable= e1)   
    health_entry.grid(row=0, column=1)
    # speed setting
    speed_label = tk.Label(frame, text="Speed:")
    speed_label.grid(row=1, column=0)
    e2 = tk.StringVar()
    e2.set(setting_speed)
    speed_entry = tk.Entry(frame, textvariable=e2)
    speed_entry.grid(row=1, column=1)
    # boat setting
    upgrade_label = tk.Label(frame, text="Boat level:")
    upgrade_label.grid(row=2, column=0)
    e3 = tk.StringVar()
    e3.set(setting_upgrade)
    upgrade_entry = tk.Entry(frame, textvariable=e3)
    upgrade_entry.grid(row=2, column=1)
    # invincibility setting
    invincible_label = tk.Label(frame, text="Invincibility: ")
    invincible_label.grid(row=3, column=0)
    e9 = tk.BooleanVar()
    if player.invincible:
        e9.set(True)
    else:
        e9.set(False)
    invincible_check = tk.Checkbutton(frame, variable=e9)
    invincible_check.grid(row=3, column=1)
    # chance of powerup setting
    powerup_label = tk.Label(frame, text="Powerup chance:")
    powerup_label.grid(row=4, column=0)
    e4 = tk.StringVar()
    e4.set(str(chance_of_powerup))
    powerup_entry = tk.Entry(frame, textvariable=e4)
    powerup_entry.grid(row=4, column=1)
    # chance of enemy setting
    enemy_label = tk.Label(frame, text="Enemy chance:")
    enemy_label.grid(row=5, column=0)
    # will need to be done later when I actually add enemies
    enemy_entry = tk.Entry(frame)
    enemy_entry.grid(row=5, column=1)
    # no firing reload setting
    reload_label = tk.Label(frame, text="No reload time:")
    reload_label.grid(row=6, column=0)
    e5 = tk.BooleanVar()
    e5.set(no_fire_limit)
    reload_entry = tk.Checkbutton(frame, variable=e5)
    reload_entry.grid(row=6, column=1)
    # no of enemies setting
    enemies_label = tk.Label(frame, text="No enemies:")
    enemies_label.grid(row=7, column=0)
    # also needs to be done later
    enemies_entry = tk.Checkbutton(frame)
    enemies_entry.grid(row=7, column=1)
    # no sound setting
    sound_label = tk.Label(frame, text="Sound:")
    sound_label.grid(row=8, column=0)
    e6 = tk.BooleanVar()
    e6.set(sounds_allowed)
    sound_check = tk.Checkbutton(frame, variable=e6)
    sound_check.grid(row=8, column=1)
    # no music setting
    music_label = tk.Label(frame, text="Music:")
    music_label.grid(row=9, column=0)
    e7 = tk.BooleanVar()
    e7.set(music_allowed)
    music_check = tk.Checkbutton(frame, variable=e7)
    music_check.grid(row=9, column=1)
    # no of powerups setting
    powerups_label = tk.Label(frame, text="No powerups:")
    powerups_label.grid(row=10, column=0)
    e10 = tk.BooleanVar()
    e10.set(powerups_not_allowed)
    powerups_check = tk.Checkbutton(frame, variable=e10)
    powerups_check.grid(row=10, column=1)
    # game mode setting
    mode_label = tk.Label(frame, text="Game mode:")
    mode_label.grid(row=11, column=0)
    e8 = tk.StringVar()
    e8.set(game_mode)
    mode_option = tk.OptionMenu(frame, e8, "Endless", "Timed")
    mode_option.grid(row=11, column=1)

    # apply button
    button = tk.Button(window, text="Apply", command=lambda: apply(window, e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get(), e10.get()))
    button.pack(side=tk.BOTTOM)

    window.mainloop()

# classes
# class for player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = playerImg
        self.rect = self.img.get_rect()
        self.rect.x = width/2 - self.img.get_width()/2
        self.rect.y = height - self.img.get_height()
        self.speed = setting_speed
        self.x_change = 0
        self.y_change = 0
        self.health = setting_health
        self.shield = False
        self.points = 0
        self.upgrade_level = setting_upgrade
        self.can_fire = True
        self.firing_rate = 10
        self.invincible = False

    def shoot(self):
        global canonballs
        if sounds_allowed:
            ship_fire.play()
        self.can_fire = False
        bullet = Bullet(self.rect.x, self.rect.y)
        canonballs.add(bullet)

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
class Powerup(pygame.sprite.Sprite):
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

# class for bullets/cannonballs
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("powerup_upg.png"), (base_size/4, base_size/4))
        self.rect = self.image.get_rect()
        self.rect.x = x + base_size/2 - self.image.get_width()/2
        self.rect.y = y - self.image.get_height()
    def move(self):
        self.rect.y -= 5

# Initializing the game
pygame.init()
width, height = 800, 600
# base size is a metric for the size of all the basic objects in the game
base_size = width/12
# allowing resizability
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stormy Seas")
icon = pygame.image.load("boat.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
setting_img = pygame.transform.scale(pygame.image.load("settings.png"), (base_size, base_size))

# sounds and music
ship_hit = mixer.Sound("ship_hit.mp3")
powerup_pickup = mixer.Sound("power up collected.mp3")
ship_fire = mixer.Sound("explosion.mp3")
ship_destroyed = mixer.Sound("ship_exp.mp3")
enemy_destroyed = mixer.Sound("enemy_exp.mp3")

# Player
playerImg = pygame.transform.scale(pygame.image.load("boat.png"), (base_size, base_size))
setting_speed = 2
setting_health = 3
setting_upgrade = 1
no_fire_limit = False
player = Player()

# canonballs
canonballs = pygame.sprite.Group()

# Obstacle
obstacleImg = pygame.transform.scale(pygame.image.load("stone.png"), (base_size, base_size))
obstacleImg2 = pygame.transform.scale(pygame.image.load("glacier.png"), (base_size, base_size))
obstacleImg3 = pygame.transform.scale(pygame.image.load("stone2.png"), (base_size, base_size))
obstacle_imges = [obstacleImg, obstacleImg2, obstacleImg3]
obstacle_sprites = pygame.sprite.Group()

# Powerup
# I will add distinct powerup images later on
powerupImg_speed = pygame.transform.scale(pygame.image.load("boat.png"), (base_size, base_size))
powerupImg_health = pygame.transform.scale(pygame.image.load("powerup_health.png"), (base_size, base_size))
powerupImg_shield = pygame.transform.scale(pygame.image.load("powerup.png"), (base_size, base_size))
powerupImg_points = pygame.transform.scale(pygame.image.load("boat.png"), (base_size, base_size))
powerupImg_upgrade = pygame.transform.scale(pygame.image.load("powerup_upg.png"), (base_size, base_size))
powerupsImgs = [powerupImg_speed, powerupImg_health, powerupImg_shield, powerupImg_points, powerupImg_upgrade]
powerup_sprites = pygame.sprite.Group()

# setting up a new thread for handling the spawning of obstacles and enemies and powerups
spawn_thread = threading.Thread(target=spawn_thread)

# main loop
running = True
spawnning = True
settings = False
screen_speed = 1
sounds_allowed = True
music_allowed = True
chance_of_powerup = 5
font = pygame.font.Font(None, int(base_size/2))
entering_menu = True
game_over = False
powerups_not_allowed = False
game_mode = "Endless"
while running:

    # entering menu
    while entering_menu:
        screen.fill((255, 255, 255))
        # creating three buttons for the main menu
        button1 = pygame.Rect(width/2 - base_size*2, height/2 - base_size/2, base_size*4, base_size)
        button2 = pygame.Rect(width/2 - base_size*2, height/2 + base_size/2, base_size*4, base_size)
        button3 = pygame.Rect(width/2 - base_size*2, height/2 + base_size*1.5, base_size*4, base_size)
        pygame.draw.rect(screen, (0, 0, 0), button1)
        pygame.draw.rect(screen, (0, 0, 0), button2)
        pygame.draw.rect(screen, (0, 0, 0), button3)
        text = font.render("Start", True, (255, 255, 255))
        screen.blit(text, (width/2-text.get_width()/2, height/2 - base_size/2 + base_size/4))
        text = font.render("High scores", True, (255, 255, 255))
        screen.blit(text, (width/2-text.get_width()/2, height/2 + base_size/2 + base_size/4))
        text = font.render("Exit", True, (255, 255, 255))
        screen.blit(text, (width/2-text.get_width()/2, height/2 + base_size*1.5 + base_size/4))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                entering_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button1.collidepoint(x, y):
                    entering_menu = False
                elif button2.collidepoint(x, y):
                    pass
                elif button3.collidepoint(x, y):
                    running = False
                    entering_menu = False
                    spawnning = False
        pygame.display.update()

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
            if event.key == pygame.K_SPACE and player.firing_rate != 0 and player.can_fire == True:
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
                if x > width - setting_img.get_width() and y < setting_img.get_height():
                    settings = True
                    settings_window()

    # moving player
    player.move()

    # checking boundaries for player
    if player.rect.x < 0:
        player.rect.x = 0
    elif player.rect.x > width - playerImg.get_width():
        player.rect.x = width - playerImg.get_width() 
    if player.rect.y < 0:
        player.rect.y = 0
    elif player.rect.y > height - playerImg.get_height():
        player.rect.y = height - playerImg.get_height()
    
    # drawing and moving obstacles
    obstacle_sprites.draw(screen)
    for obs in obstacle_sprites:
        obs.move(screen_speed)

    # drawing and moving powerups
    powerup_sprites.draw(screen)
    for powerup in powerup_sprites:
        powerup.move(screen_speed)

    # drawing and moving bullets
    canonballs.draw(screen)
    for bullet in canonballs:
        bullet.move()

    # drawing player
    player.draw()

    # drawing settings button
    screen.blit(setting_img, (width - setting_img.get_width(), 0))

    # drawing points
    text = font.render(str(player.points)+" m", True, (0, 0, 0))
    screen.blit(text, (width/2-text.get_width()/2, 0))

    # drawing health
    text = font.render("Health: "+str(player.health), True, (0, 0, 0))
    screen.blit(text, (width/2 + width/4-text.get_width()/2, 0))

    # checking for collision between player and obstacles
    for obs in obstacle_sprites:
        if player.rect.colliderect(obs.rect):
            obstacle_sprites.remove(obs)
            if player.invincible == False:
                if player.shield == True:
                    player.shield = False
                else:
                    player.health -= 1
                if player.health == 0:
                    if sounds_allowed:
                        ship_destroyed.play()
                    game_over_screen()
                elif sounds_allowed:
                    ship_hit.play()
    
    # checking for collision between player and powerups
    for powerup in powerup_sprites:
        if player.rect.colliderect(powerup.rect):
            powerup_sprites.remove(powerup)
            if sounds_allowed:
                powerup_pickup.play()
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
                
    # checking for collision between bullets and obstacles
    for bullet in canonballs:
        for obs in obstacle_sprites:
            if bullet.rect.colliderect(obs.rect):
                canonballs.remove(bullet)
                obstacle_sprites.remove(obs)

    clock.tick(60)
    pygame.display.update()

spawnning = False
pygame.quit()