import pygame
import random
import threading
import tkinter as tk
from pygame import mixer
import math

# functions
# function for spawning obstacles, powerups, etc.
def spawn_thread():
    global running, spawnning, obstacle_sprites, powerup_sprites, settings, player, game_over, chance_of_powerup, powerups_not_allowed,no_fire_limit, day_night_cycle, chance_of_enemy, enemies_not_allowed
    clock = pygame.time.Clock()
    global waiting_time, reloading_time
    while running:
        while spawnning and settings == False and game_over == False:
            obs = obstacle(random.choice(obstacle_imges))
            obstacle_sprites.add(obs)
            if player.can_fire == False and no_fire_limit == False:
                waiting_time -= 1
                reloading_time += 1
                if waiting_time == 0:
                    player.can_fire = True
                    waiting_time = player.firing_rate
                    reloading_time = 0
            # every once in a while a powerup will spawn
            if random.randint(0, 100) < chance_of_powerup and powerups_not_allowed == False:
                pw = Powerup()
                powerup_sprites.add(pw)
            # every once in a while an enemy will spawn
            if player.points > 20 and random.randint(0, 100) < chance_of_enemy and enemies_not_allowed == False:
                enemy = Enemy()
                enemies.add(enemy)
            # changing the day night cycle
            if player.points % 100 == 0 and player.points != 0:
                if day_night_cycle == "day":
                    day_night_cycle = "night"
                else:
                    day_night_cycle = "day"
            # adding a point every second
            player.points += 1
            clock.tick(1)
        clock.tick(1)

# function for restarting the game
def restart_game():
    global player, obstacle_sprites, powerup_sprites, day_night_cycle, enemy_canonballs, canonballs
    day_night_cycle = "day"
    player = Player()
    obstacle_sprites = pygame.sprite.Group()
    powerup_sprites = pygame.sprite.Group()
    enemy_canonballs = pygame.sprite.Group()
    canonballs = pygame.sprite.Group()

# function for saving the score to a separate file
def save_score():
    global player
    # saving the score with a player name to a separate file, this is used for the high scores leaderboard screen
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            scores.append("Player, "+str(player.points)+"\n")
            scores = sorted(scores, key=lambda x: int(x.split(", ")[1]), reverse=True)
        with open("scores.txt", "w") as file:
            for score in scores:
                file.write(score)
    # if there is no file for the scores, creating one and writing the score to it
    except:
        with open("scores.txt", "w") as file:
            file.write("Player, "+str(player.points)+"\n")
        
    # closing the file
    file.close()
# function for high scores screen
def high_scores_screen():
    global width, height, screen, running, spawnning, entering_menu
    # reading the scores from the file if it exists and displaying the first 10
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            scores = scores[:10]
    except:
        scores = []
    # creating the actual window
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, int(base_size))
    score_screen_running = True
    while score_screen_running:
        for i, score in enumerate(scores):
            score = score.strip()
            text = font.render(str(i+1)+". "+score, True, (0, 0, 0))
            screen.blit(text, (width/2-text.get_width()/2, height/4-text.get_height()/2 + i*text.get_height()))
        
        # displaying the back arrow
        screen.blit(back_arrow, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                score_screen_running = False
                running = False
                entering_menu = False
                spawnning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x < back_arrow.get_width() and y < back_arrow.get_height():
                    score_screen_running = False
        pygame.display.update()

# function for game over screen
def game_over_screen():
    global running, spawnning, game_over, width, height, game_played
    spawnning = False
    game_over = True
    can_exit = 0
    game_played = False
    while game_over:
        screen.fill((255, 255, 255))
        text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(text, (width/2-text.get_width()/2, height/2-text.get_height()))
        text = font.render("Number of points: "+str(player.points), True, (0, 0, 0))
        screen.blit(text, (width/2-text.get_width()/2, height/2+text.get_height()*0.5))
        text = font.render("Press R to restart", True, (0, 0, 0))
        screen.blit(text, (width/2-text.get_width()/2, height/2+text.get_height()*2))
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
    global settings, setting_health, setting_speed, setting_upgrade, no_fire_limit, sounds_allowed, music_allowed, powerups_not_allowed, game_mode, chance_of_powerup, enemies_not_allowed, chance_of_enemy
    if health != "":
        try:
            setting_health = int(health)
        except:
            pass
    if speed != "":
        try:
            setting_speed = int(speed)
        except:
            pass
    if upgrade != "":
        try:
            setting_upgrade = int(upgrade)
        except:
            pass
    if invincible:
        player.invincible = True
    else:
        player.invincible = False
    if powerup != "":
        try:
            chance_of_powerup = int(powerup)
        except:
            pass
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
    if enemies:
        enemies_not_allowed = True
    else:
        enemies_not_allowed = False
    if enemy != "":
        try:
            chance_of_enemy = int(enemy)
        except:
            pass
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
    e11 = tk.StringVar()
    e11.set(str(chance_of_enemy))
    enemy_entry = tk.Entry(frame, textvariable=e11)
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
    e12 = tk.BooleanVar()
    e12.set(enemies_not_allowed)
    enemies_entry = tk.Checkbutton(frame, variable=e12)
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
    button = tk.Button(window, text="Apply", command=lambda: apply(window, e1.get(), e2.get(), e3.get(), e9.get(), e4.get(), e11.get(), e5.get(), e12.get(), e6.get(), e7.get(), e10.get(), e8.get()))# it is a bit confusing naming, but it works
    button.pack(side=tk.BOTTOM)

    window.mainloop()

# classes
# class for player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = playerImg
        self.x = width/2 - self.img.get_width()/2
        self.y = height - self.img.get_height()
        self.rect = self.img.get_rect(center = (self.x, self.y))
        self.speed = setting_speed
        self.health = setting_health
        self.shield = False
        self.points = 0
        self.upgrade_level = setting_upgrade
        self.can_fire = True
        self.firing_rate = 7
        self.invincible = False
        self.angle = 0
        self.direction = ""

    def shoot(self):
        global canonballs
        if sounds_allowed:
            ship_fire.play()
        self.can_fire = False
        bullet = Bullet(self.x ,self.y, self.angle)
        canonballs.add(bullet)

    def move(self):
        # using the angle to move the player
        if self.direction == "up":
            self.hori -= math.sin(math.radians(self.angle)) * self.speed
            self.vert -= math.cos(math.radians(self.angle)) * self.speed
        elif self.direction == "down":
            self.hori += math.sin(math.radians(self.angle)) * self.speed
            self.vert += math.cos(math.radians(self.angle)) * self.speed
        elif self.direction == "":
            self.hori = 0
            self.vert = 0
        self.x += self.hori
        self.y += self.vert

        self.rect = self.img.get_rect(center = (self.x, self.y))
    
    def upgrade(self):
        self.img = pygame.transform.scale(pygame.image.load('boat'+str(player.upgrade_level)+'.png'), (base_size, base_size))
        self.rect = self.img.get_rect(center = (self.x, self.y))
        # will be enhanced later on
        if self.upgrade_level == 1:
            self.firing_rate = 1
        elif self.upgrade_level == 2:
            self.firing_rate = 2
        elif self.upgrade_level == 3:
            self.firing_rate = 3

    def draw(self):
        screen.blit(pygame.transform.rotate(self.img, self.angle), (self.rect))
        self.rect = self.img.get_rect(center = (self.x, self.y))

# class for obstacles
class obstacle(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.rect = img.get_rect()
        self.rect.x = random.randint(0, width - img.get_width())
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
        self.rect.x = random.randint(0, width - self.image.get_width())
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
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.angle = angle +180
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("powerup_upg.png"), (base_size/4, base_size/4)), self.angle)
        self.x = x 
        self.y = y 
        self.hori = math.sin(math.radians(self.angle)) * self.speed
        self.vert = math.cos(math.radians(self.angle)) * self.speed
        self.rect = self.image.get_rect(center = (self.x, self.y))
    def move(self):
        self.x += self.hori
        self.y += self.vert
        self.rect = self.image.get_rect(center = (self.x, self.y))

# class for enemies(enemy boats)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        global frame_rate, width, height
        pygame.sprite.Sprite.__init__(self)
        # the enemy will use the same boat as the player, however the enemy will boats will have a pirate flag on them, this will be added later on
        if player.upgrade_level == 1:
            self.image = pygame.transform.scale(pygame.image.load("boat.png"), (base_size, base_size))
        else:
            self.image = pygame.transform.scale(pygame.image.load("boat{player.update_level}.png"), (base_size, base_size))
        self.x = random.randint(0, width - self.image.get_width())
        self.y = 0 - self.image.get_height()
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.destin_x = random.randint(self.image.get_width(), width - self.image.get_width())
        self.destin_y = random.randint(self.image.get_height(), height - self.image.get_height())
        self.angle = player.angle #math.degrees(math.atan2(self.destin_x - self.x, self.destin_y - self.y)) # later will be changed, this is just for testing purposes
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.turret_image = pygame.transform.scale(pygame.image.load("powerup_upg.png"), (base_size/4, base_size/4)) # will have its own image later
        self.fire_rate = player.firing_rate * frame_rate # this is because the shoot function is called from the main loop 
        self.can_fire = True
        self.health = player.health # enemies will have the same health as the player, this could work as a balancing factor
        self.speed = player.speed
 
    def move(self):
        global width, height
        # moving the enemy, the  enemy will now do random circle like movements around the player, maybe I will change this later
        #print(self.rect.x, self.rect.y, self.destin_x, self.destin_y)
        if abs(self.x - self.destin_x) < self.speed:
            pass
        elif self.x < self.destin_x:
            self.x += self.speed
        elif self.x > self.destin_x:
            self.x -= self.speed
        if abs(self.y - self.destin_y) < self.speed:
            pass
        elif self.y < self.destin_y:
            self.y += self.speed
        elif self.y > self.destin_y:
            self.y -= self.speed
        # if the enemy is close enough to the destination point, a new destination point will be set
        if abs(self.x - self.destin_x) < self.speed and abs(self.y - self.destin_y) < self.speed:
            self.destin_x = random.randint(self.image.get_width(), width - self.image.get_width())
            self.destin_y = random.randint(self.image.get_height(), height - self.image.get_height())
            # adjusting the angle of the enemy to the destination point
        self.angle = player.angle

        self.rect = self.image.get_rect( center = (self.x, self.y))
    
    def draw(self):
        # I didnt know I cant just modify the self.image with the new rotated image, because it will deteriorate until it crashes the game
        # so instead I will not use the sprite draw function, but my own that will rotate the image every time its drawn
        screen.blit(pygame.transform.rotate(self.image, self.angle), (self.rect))
        screen.blit(pygame.transform.rotate(self.turret_image, self.angle), (self.x, self.y))
    
    def update(self):
        # displaying the health of the enemy below the enemy
        global enemy_font
        text = enemy_font.render(str(self.health), True, (255, 0, 0))
        screen.blit(text, (self.x- text.get_width()/2, self.y + self.image.get_height()/2))

    def shoot(self):
        global enemy_canonballs, frame_rate, sounds_allowed
        if self.can_fire == True:
            if sounds_allowed:
                ship_fire.play() # maybe later the enemies will have a distinct sound for firing
            bullet = EnemyBullet(self.x, self.y, self.angle)
            enemy_canonballs.add(bullet)
            self.can_fire = False
        else:
            self.fire_rate -= 1
            if self.fire_rate == 0:
                self.can_fire = True
                self.fire_rate = player.firing_rate * frame_rate

# class for enemy bullets
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.angle = angle +180
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("powerup_upg.png"), (base_size/4, base_size/4)), self.angle)
        self.x = x 
        self.y = y 
        self.hori = math.sin(math.radians(self.angle)) * self.speed
        self.vert = math.cos(math.radians(self.angle)) * self.speed
        self.rect = self.image.get_rect(center = (self.x, self.y))
    def move(self):
        self.x += self.hori
        self.y += self.vert
        self.rect = self.image.get_rect(center = (self.x, self.y))

# Initializing the game
pygame.init()
width, height = 800, 600
# base size is a metric for the size of all the basic objects in the game
base_size = width/12
# frame rate
frame_rate = 60
# allowing resizability
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stormy Seas")
icon = pygame.image.load("boat.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
setting_img = pygame.transform.scale(pygame.image.load("settings.png"), (base_size, base_size))
back_arrow = pygame.transform.scale(pygame.image.load("back_arrow.png"), (base_size, base_size))
sun = pygame.transform.scale(pygame.image.load("sun.png"), (base_size, base_size))
moon = pygame.transform.scale(pygame.image.load("moon.png"), (base_size, base_size))

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
waiting_time = player.firing_rate
reloading_time = 0 # I tried to not have two basicaly same variables, but it needed to be done like this, maybe I will change it later, if I find a better way


# canonballs
canonballs = pygame.sprite.Group()

# enemies
enemies = pygame.sprite.Group()
enemy_canonballs = pygame.sprite.Group()
chance_of_enemy = 3
enemies_not_allowed = False
enemy_font = pygame.font.Font(None, int(base_size/2))
# spawning a test enemy
enemy = Enemy()
enemies.add(enemy)

# Obstacle
obstacleImg = pygame.transform.scale(pygame.image.load("stone.png"), (base_size, base_size))
obstacleImg2 = pygame.transform.scale(pygame.image.load("glacier.png"), (base_size, base_size))
obstacleImg3 = pygame.transform.scale(pygame.image.load("stone2.png"), (base_size, base_size))
obstacleImg4 = pygame.transform.scale(pygame.image.load("stone3.png"), (base_size, base_size))
obstacleImg5 = pygame.transform.scale(pygame.image.load("glacier2.png"), (base_size, base_size))
obstacle_imges = [obstacleImg, obstacleImg2, obstacleImg3, obstacleImg4, obstacleImg5]
obstacle_sprites = pygame.sprite.Group()

# Powerup
# More powerup images will be added later
powerupImg_speed = pygame.transform.scale(pygame.image.load("boat.png"), (base_size, base_size))
powerupImg_health = pygame.transform.scale(pygame.image.load("powerup_health.png"), (base_size, base_size))
powerupImg_shield = pygame.transform.scale(pygame.image.load("powerup.png"), (base_size, base_size))
powerupImg_points = pygame.transform.scale(pygame.image.load("boat.png"), (base_size, base_size))
powerupImg_upgrade = pygame.transform.scale(pygame.image.load("powerup_upg.png"), (base_size, base_size))
powerupsImgs = [powerupImg_speed, powerupImg_health, powerupImg_shield, powerupImg_points, powerupImg_upgrade]
powerup_sprites = pygame.sprite.Group()

# day night cycle settup
day_night_cycle = "day" # will be used later for changing the colors of the enemies and background

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
game_played = False
angle = 0
show_powerup_message = False
keep_message = 5 * frame_rate
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
        # displaying a resume button if the game has started but not ended
        if game_played:
            button4 = pygame.Rect(width/2 - base_size*2, height/2 - base_size*2, base_size*4, base_size)
            pygame.draw.rect(screen, (0, 0, 0), button4)
            text = font.render("Resume", True, (255, 255, 255))
            screen.blit(text, (width/2-text.get_width()/2, height/2 - base_size*2 + base_size/4))
            
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
                    spawnning = True
                    game_played = True
                    restart_game()
                elif button2.collidepoint(x, y):
                    high_scores_screen()
                elif button3.collidepoint(x, y):
                    running = False
                    entering_menu = False
                    spawnning = False
                elif game_played and button4.collidepoint(x, y):
                    entering_menu = False
                    spawnning = True
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
                angle = 5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                angle = -5
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.direction = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.direction = "down"
            if event.key == pygame.K_SPACE and player.firing_rate != 0 and player.can_fire == True:
                player.shoot()
            if event.key == pygame.K_r:
                restart_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player.direction = ""
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                angle = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # checking if the settings button is clicked
                x, y = pygame.mouse.get_pos()
                if x > width - setting_img.get_width() and y < setting_img.get_height():
                    settings = True
                    settings_window()
                # checking if the back arrow is clicked
                elif x < back_arrow.get_width() and y < back_arrow.get_height():
                    entering_menu = True
                    spawnning = False

    # moving player
    player.angle += angle
    player.move()

    # checking boundaries for player
    if player.x < 0:
        player.x = 0
    elif player.x > width - playerImg.get_width():
        player.x = width - playerImg.get_width() 
    if player.y < 0:
        player.y = 0
    elif player.y > height - playerImg.get_height():
        player.y = height - playerImg.get_height()
    
    # drawing and moving obstacles
    obstacle_sprites.draw(screen)
    for obs in obstacle_sprites:
        obs.move(screen_speed)
    obstacle_sprites = pygame.sprite.Group(sorted(obstacle_sprites, key=lambda x: x.rect.y))

    # drawing and moving powerups
    powerup_sprites.draw(screen)
    for powerup in powerup_sprites:
        powerup.move(screen_speed)

    # drawing and moving bullets
    canonballs.draw(screen)
    for bullet in canonballs:
        bullet.move()

    # drawing and moving enemy bullets
    enemy_canonballs.draw(screen)
    for bullet in enemy_canonballs:
        bullet.move()

    # drawing player
    player.draw()

    # drawing and moving enemies
    for enemy in enemies:
        enemy.draw()
        enemy.move()
        enemy.update() # displaying the health of the enemy
        enemy.shoot()

    # drawing settings button
    screen.blit(setting_img, (width - setting_img.get_width(), 0))

    # drawing back arrow
    screen.blit(back_arrow, (0, 0))

    # drawing sun or moon based on the day night cycle
    if day_night_cycle == "day":
        screen.blit(sun, (width - sun.get_width(), setting_img.get_height()*1.5))
    else:
        screen.blit(moon, (width - moon.get_width(), setting_img.get_height()*1.5))

    # drawing points
    text = font.render(str(player.points)+" points", True, (0, 0, 0))
    screen.blit(text, (width/2-text.get_width()/2, 0))

    # drawing health
    text = font.render("Health: "+str(player.health), True, (0, 0, 0))
    screen.blit(text, (width/2 + width/4-text.get_width()/2, 0))

    # drawing the reload time, this may not be the best solution, but I am tired and it works
    if reloading_time == 0:
        text = font.render("Reload time: Ready", True, (0, 0, 0))
    else:
        text = font.render("Reload time: "+str(player.firing_rate - reloading_time), True, (0, 0, 0))
    screen.blit(text, (width/2 - width/4-text.get_width()/2, 0))

    # drawing the powerup message
    if show_powerup_message:
        screen.blit(powerup_message, (width/2-powerup_message.get_width()/2, height-powerup_message.get_height()*1.5))
        keep_message -= 1
        if keep_message == 0:
            show_powerup_message = False
            keep_message = 5 * frame_rate

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
                    save_score()
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
                powerup_message = font.render("Speed", True, (0, 0, 0))
            elif powerup.type == "health":
                player.health += 1
                powerup_message = font.render("Health", True, (0, 0, 0))
            elif powerup.type == "shield":
                player.shield = True
                powerup_message = font.render("Shield", True, (0, 0, 0))
            elif powerup.type == "points":
                player.points += 30
                powerup_message = font.render("Points", True, (0, 0, 0))
            elif powerup.type == "upgrade":
                powerup_message = font.render("Upgrade", True, (0, 0, 0))
                player.upgrade()
            show_powerup_message = True
                
    # checking for collision between bullets and obstacles
    for bullet in canonballs:
        for obs in obstacle_sprites:
            if bullet.rect.colliderect(obs.rect):
                canonballs.remove(bullet)
                obstacle_sprites.remove(obs)

    # checking for collision between bullets and enemies
    for bullet in canonballs:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                enemy.health -= 1
                canonballs.remove(bullet)
                if enemy.health == 0:
                    if sounds_allowed:
                        enemy_destroyed.play()
                    enemies.remove(enemy)
                    player.points += 10
    
    # checking for collision between enemy bullets and player
    for bullet in enemy_canonballs:
        if player.rect.colliderect(bullet.rect):
            enemy_canonballs.remove(bullet)
            if player.invincible == False:
                if player.shield == True:
                    player.shield = False
                else:
                    player.health -= 1
                if player.health == 0:
                    if sounds_allowed:
                        ship_destroyed.play()
                    save_score()
                    game_over_screen()
                elif sounds_allowed:
                    ship_hit.play()
    
    # checking for collision between enemy bullets and powerups(I will add this to later see if this feature makes sense gameplay wise)
    for bullet in enemy_canonballs:
        for powerup in powerup_sprites:
            if bullet.rect.colliderect(powerup.rect):
                enemy_canonballs.remove(bullet)
                powerup_sprites.remove(powerup)

    clock.tick(frame_rate)
    pygame.display.update()

spawnning = False
pygame.quit()