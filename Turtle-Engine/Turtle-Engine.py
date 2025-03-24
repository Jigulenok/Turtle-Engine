import pygame
import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
import json
import queue
import random
from PIL import Image
import os
import ctypes
import sys

def hide_console():
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.WinDLL('kernel32')
            user32 = ctypes.WinDLL('user32')
            SW_HIDE = 0
            hWnd = kernel32.GetConsoleWindow()
            if hWnd:
                user32.ShowWindow(hWnd, SW_HIDE)
        except Exception as e:
            print(f"Не удалось скрыть консоль: {e}")

hide_console()

pygame.init()

font = pygame.font.Font(None, 36)
exclamation_font = pygame.font.Font(None, 48)

WIDTH, HEIGHT = 1920, 1080
INITIAL_WIDTH, INITIAL_HEIGHT = WIDTH, HEIGHT
CELL_SIZE = 20
BACKGROUND_COLOR = (255, 255, 255)
walls = []
floor_color = (200, 200, 200)
floor_tiles = []
doors = []
eraser_mode = False
is_paused = True
WALL_COLOR = (0, 0, 0)
VISION_DISTANCE = 200
msg_queue = queue.Queue()
max_health = 2
current_health = max_health
can_move_player = False
game_over = False
restart_timer = 0
delay_message = False
volume = 0.5
ammo_packs = []
health_packs = []
placement_mode = 'bots'
brush_size = 1
floor_texture_path = None
wall_texture_path = None
current_level_path = None
texture_cache = {}
wall_drawing_mode = 'color'
floor_drawing_mode = 'color'
cutscene_actions = []
characters = []
in_cutscene = False
cutscene_start_time = 0
black_bar_height = 0
black_bar_max_height = 100
black_bar_growth_rate = 2
bots = []
font_cache = {}

player_up_path = None
player_down_path = None
player_left_path = None
player_right_path = None
player_crawl_up_path = None
player_crawl_down_path = None
player_crawl_left_path = None
player_crawl_right_path = None
bot_up_path = None
bot_down_path = None
bot_left_path = None
bot_right_path = None
ammo_texture_path = None
health_texture_path = None
pistol_texture_path = None
walkie_talkie_texture_path = None
door_texture_path = None
music_path = None
walkie_talkie_message = ""

initial_player_position = (0, 0)
initial_bots_positions = []
return_to_menu = False
play_game = False

pistol_image = None
walkie_talkie_image = None

def load_gif(filename):
    frames = []
    if not filename or not os.path.exists(filename):
        return frames
    try:
        with Image.open(filename) as img:
            for frame in range(img.n_frames):
                img.seek(frame)
                frame_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
                if 'transparency' in img.info:
                    frame_surface.set_colorkey(img.info['transparency'])
                frames.append(frame_surface)
    except Exception as e:
        print(f"Ошибка при загрузке {filename}: {e}")
    return frames

player_animations = {
    'up': load_gif(player_up_path),
    'down': load_gif(player_down_path),
    'left': load_gif(player_left_path),
    'right': load_gif(player_right_path),
    'crawl_up': load_gif(player_crawl_up_path),
    'crawl_down': load_gif(player_crawl_down_path),
    'crawl_left': load_gif(player_crawl_left_path),
    'crawl_right': load_gif(player_crawl_right_path)
}
bot_animations = {
    'up': load_gif(bot_up_path),
    'down': load_gif(bot_down_path),
    'left': load_gif(bot_left_path),
    'right': load_gif(bot_right_path)
}

def load_player_up_texture():
    global player_up_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_up_path = file_path
        player_animations['up'] = load_gif(file_path)

def load_player_down_texture():
    global player_down_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_down_path = file_path
        player_animations['down'] = load_gif(file_path)

def load_player_left_texture():
    global player_left_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_left_path = file_path
        player_animations['left'] = load_gif(file_path)

def load_player_right_texture():
    global player_right_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_right_path = file_path
        player_animations['right'] = load_gif(file_path)

def load_player_crawl_up_texture():
    global player_crawl_up_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_crawl_up_path = file_path
        player_animations['crawl_up'] = load_gif(file_path)

def load_player_crawl_down_texture():
    global player_crawl_down_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_crawl_down_path = file_path
        player_animations['crawl_down'] = load_gif(file_path)

def load_player_crawl_left_texture():
    global player_crawl_left_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_crawl_left_path = file_path
        player_animations['crawl_left'] = load_gif(file_path)

def load_player_crawl_right_texture():
    global player_crawl_right_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        player_crawl_right_path = file_path
        player_animations['crawl_right'] = load_gif(file_path)

def load_bot_up_texture():
    global bot_up_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        bot_up_path = file_path
        bot_animations['up'] = load_gif(file_path)

def load_bot_down_texture():
    global bot_down_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        bot_down_path = file_path
        bot_animations['down'] = load_gif(file_path)

def load_bot_left_texture():
    global bot_left_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        bot_left_path = file_path
        bot_animations['left'] = load_gif(file_path)

def load_bot_right_texture():
    global bot_right_path
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        bot_right_path = file_path
        bot_animations['right'] = load_gif(file_path)

def load_ammo_texture():
    global ammo_texture_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        ammo_texture_path = file_path

def load_health_texture():
    global health_texture_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        health_texture_path = file_path

def load_pistol_texture():
    global pistol_texture_path, pistol_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        pistol_texture_path = file_path
        try:
            pistol_image = pygame.image.load(file_path).convert_alpha()
            pistol_image = pygame.transform.scale(pistol_image, (144, 144))
        except pygame.error as e:
            print(f"Ошибка загрузки текстуры пистолета: {e}")
            pistol_image = None

def load_walkie_talkie_texture():
    global walkie_talkie_texture_path, walkie_talkie_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        walkie_talkie_texture_path = file_path
        try:
            walkie_talkie_image = pygame.image.load(file_path).convert_alpha()
            walkie_talkie_image = pygame.transform.scale(walkie_talkie_image, (144, 144))
        except pygame.error as e:
            print(f"Ошибка загрузки текстуры рации: {e}")
            walkie_talkie_image = None

def load_door_texture():
    global door_texture_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        door_texture_path = file_path

def open_texture_loader():
    texture_window = tk.Toplevel()
    texture_window.title("Загрузить текстуры")

    tk.Label(texture_window, text="Анимации игрока:").pack(pady=5)
    tk.Button(texture_window, text="Вверх", command=load_player_up_texture).pack(pady=2)
    tk.Button(texture_window, text="Вниз", command=load_player_down_texture).pack(pady=2)
    tk.Button(texture_window, text="Влево", command=load_player_left_texture).pack(pady=2)
    tk.Button(texture_window, text="Вправо", command=load_player_right_texture).pack(pady=2)
    tk.Button(texture_window, text="Ползание вверх", command=load_player_crawl_up_texture).pack(pady=2)
    tk.Button(texture_window, text="Ползание вниз", command=load_player_crawl_down_texture).pack(pady=2)
    tk.Button(texture_window, text="Ползание влево", command=load_player_crawl_left_texture).pack(pady=2)
    tk.Button(texture_window, text="Ползание вправо", command=load_player_crawl_right_texture).pack(pady=2)

    tk.Label(texture_window, text="Анимации ботов:").pack(pady=5)
    tk.Button(texture_window, text="Вверх", command=load_bot_up_texture).pack(pady=2)
    tk.Button(texture_window, text="Вниз", command=load_bot_down_texture).pack(pady=2)
    tk.Button(texture_window, text="Влево", command=load_bot_left_texture).pack(pady=2)
    tk.Button(texture_window, text="Вправо", command=load_bot_right_texture).pack(pady=2)

    tk.Label(texture_window, text="Текстуры объектов:").pack(pady=5)
    tk.Button(texture_window, text="Патроны", command=load_ammo_texture).pack(pady=2)
    tk.Button(texture_window, text="Аптечки", command=load_health_texture).pack(pady=2)
    tk.Button(texture_window, text="Оружие", command=load_pistol_texture).pack(pady=2)
    tk.Button(texture_window, text="Рация", command=load_walkie_talkie_texture).pack(pady=2)
    tk.Button(texture_window, text="Дверь", command=load_door_texture).pack(pady=2)

def is_wall_in_direction(x, y, direction):
    if direction == 'right':
        check_x = x + CELL_SIZE
        check_y = y
    elif direction == 'left':
        check_x = x - CELL_SIZE
        check_y = y
    elif direction == 'down':
        check_x = x
        check_y = y + CELL_SIZE
    elif direction == 'up':
        check_x = x
        check_y = y - CELL_SIZE
    else:
        return False
    return any(wall[0] == check_x and wall[1] == check_y for wall in walls)

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.direction = direction
        self.speed = 10

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        if self.check_collision():
            return True
        return False

    def check_collision(self):
        if characters:
            char_rect = pygame.Rect(characters[0]['position'][0], characters[0]['position'][1], CELL_SIZE * 1.5, CELL_SIZE * 1.5)
            if self.rect.colliderect(char_rect):
                return True
        return self.rect.collidelist([pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE) for wall in walls]) != -1

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, int(CELL_SIZE * 1.5), int(CELL_SIZE * 1.5))
        self.collision_rect = self.rect.copy()
        self.direction = 'down'
        self.target_x = self.rect.centerx
        self.target_y = self.rect.centery
        self.normal_speed = CELL_SIZE // 4
        self.crawl_speed = self.normal_speed // 2
        self.speed = self.normal_speed
        self.ammo = 0
        self.animation_duration = 1000
        self.start_time = pygame.time.get_ticks()
        self.is_crawling = False

    def reset_target(self):
        self.target_x = self.rect.centerx
        self.target_y = self.rect.centery

    def move(self, dx, dy):
        if is_paused or eraser_mode or in_cutscene:
            return
        if dx != 0 or dy != 0:
            self.direction = self.get_direction(dx, dy)
            grid_x = round(self.rect.centerx / CELL_SIZE) * CELL_SIZE
            grid_y = round(self.rect.centery / CELL_SIZE) * CELL_SIZE

            if self.is_crawling:
                if dx > 0:
                    self.target_x = grid_x + CELL_SIZE
                    self.target_y = self.rect.centery
                elif dx < 0:
                    self.target_x = grid_x - CELL_SIZE
                    self.target_y = self.rect.centery
                elif dy > 0:
                    self.target_y = grid_y + CELL_SIZE
                    self.target_x = self.rect.centerx
                elif dy < 0:
                    self.target_y = grid_y - CELL_SIZE
                    self.target_x = self.rect.centerx
            else:
                if dx > 0:
                    self.target_x = grid_x + CELL_SIZE
                elif dx < 0:
                    self.target_x = grid_x - CELL_SIZE
                elif dy > 0:
                    self.target_y = grid_y + CELL_SIZE
                elif dy < 0:
                    self.target_y = grid_y - CELL_SIZE

    def get_direction(self, dx, dy):
        if dx > 0:
            return 'right'
        elif dx < 0:
            return 'left'
        elif dy > 0:
            return 'down'
        elif dy < 0:
            return 'up'
        return self.direction

    def update(self):
        global current_health
        if is_paused or eraser_mode or in_cutscene:
            return
        keys = pygame.key.get_pressed()
        self.is_crawling = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        self.speed = self.crawl_speed if self.is_crawling else self.normal_speed

        if self.is_crawling:
            if self.direction in ['right', 'left']:
                self.collision_rect.width = int(CELL_SIZE * 1.5)
                self.collision_rect.height = int(CELL_SIZE * 0.5)
            elif self.direction in ['down', 'up']:
                self.collision_rect.width = int(CELL_SIZE * 0.5)
                self.collision_rect.height = int(CELL_SIZE * 1.5)
            self.collision_rect.center = self.rect.center
        else:
            self.collision_rect = self.rect.copy()

        if self.rect.centerx < self.target_x:
            dx = min(self.speed, self.target_x - self.rect.centerx)
        elif self.rect.centerx > self.target_x:
            dx = -min(self.speed, self.rect.centerx - self.target_x)
        else:
            dx = 0
        new_centerx = self.rect.centerx + dx
        test_rect = self.collision_rect.copy()
        test_rect.centerx = new_centerx
        if characters:
            char_rect = pygame.Rect(characters[0]['position'][0], characters[0]['position'][1], CELL_SIZE * 1.5, CELL_SIZE * 1.5)
            if test_rect.colliderect(char_rect):
                return
        if not any(test_rect.colliderect(pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE)) for wall in walls):
            self.rect.centerx = new_centerx
            self.collision_rect.centerx = new_centerx

        if self.rect.centery < self.target_y:
            dy = min(self.speed, self.target_y - self.rect.centery)
        elif self.rect.centery > self.target_y:
            dy = -min(self.speed, self.rect.centery - self.target_y)
        else:
            dy = 0
        new_centery = self.rect.centery + dy
        test_rect = self.collision_rect.copy()
        test_rect.centery = new_centery
        if characters:
            char_rect = pygame.Rect(characters[0]['position'][0], characters[0]['position'][1], CELL_SIZE * 1.5, CELL_SIZE * 1.5)
            if test_rect.colliderect(char_rect):
                return
        if not any(test_rect.colliderect(pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE)) for wall in walls):
            self.rect.centery = new_centery
            self.collision_rect.centery = new_centery

        for pack in ammo_packs[:]:
            if self.collision_rect.colliderect(pack):
                self.ammo += 5
                ammo_packs.remove(pack)
                message_text = "+5 ammo"
                message_position = (self.rect.centerx, self.rect.top - 20)
                pickup_messages.append(PickupMessage(message_text, message_position))

        for pack in health_packs[:]:
            if not pack.used and self.collision_rect.colliderect(pack.rect):
                if current_health < max_health:
                    current_health += 1
                    pack.used = True
                    message_text = "+1 health"
                    message_position = (self.rect.centerx, self.rect.top - 20)
                    pickup_messages.append(PickupMessage(message_text, message_position))
                    health_packs.remove(pack)

        for door in doors:
            door_rect = pygame.Rect(door[0], door[1], CELL_SIZE, CELL_SIZE)
            if self.collision_rect.colliderect(door_rect):
                if current_level_path:
                    save_level_to_path(current_level_path)
                load_level_from_path(door[3])
                break

    def draw(self, surface, camera_offset):
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        if self.is_crawling:
            animation_key = f'crawl_{self.direction}'
        else:
            animation_key = self.direction
        if player_animations.get(animation_key) and player_animations[animation_key]:
            current_time = pygame.time.get_ticks()
            time_elapsed = (current_time - self.start_time) % self.animation_duration
            frame_count = len(player_animations[animation_key])
            frame = int(time_elapsed / (self.animation_duration / frame_count))
            surface.blit(player_animations[animation_key][frame], (screen_x, screen_y))
        else:
            pygame.draw.rect(surface, (255, 0, 0), (screen_x, screen_y, self.rect.width, self.rect.height))

class Bot:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, int(CELL_SIZE * 1.5), int(CELL_SIZE * 1.5))
        self.initial_position = (x, y)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.movement_timer = random.randint(150, 300)
        self.bullets = []
        self.shoot_timer = 0
        self.state = 'patrol'
        self.health = 2
        self.max_health = 2
        self.animation_duration = 1000
        self.start_time = pygame.time.get_ticks()

    def update(self, player):
        if is_paused or eraser_mode or in_cutscene:
            return
        if self.can_see_player(player):
            self.state = 'chase'
        else:
            self.state = 'patrol'
        if self.state == 'patrol':
            self.patrol()
        elif self.state == 'chase':
            self.chase(player)
            self.attack(player)

    def patrol(self):
        if self.movement_timer > 0:
            self.movement_timer -= 1
        else:
            possible_directions = ['up', 'down', 'left', 'right']
            available_directions = [d for d in possible_directions if not is_wall_in_direction(self.rect.x, self.rect.y, d)]
            if available_directions:
                self.direction = random.choice(available_directions)
            else:
                self.direction = random.choice(possible_directions)
            self.movement_timer = random.randint(150, 300)
        move_step = CELL_SIZE // 10
        dx, dy = 0, 0
        if self.direction == 'right':
            dx = move_step
        elif self.direction == 'left':
            dx = -move_step
        elif self.direction == 'down':
            dy = move_step
        elif self.direction == 'up':
            dy = -move_step
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        if not self.check_collision(new_x, self.rect.y):
            self.rect.x = new_x
        if not self.check_collision(self.rect.x, new_y):
            self.rect.y = new_y

    def chase(self, player):
        if self.rect.colliderect(player.collision_rect):
            return
        move_step = CELL_SIZE // 10
        dx, dy = 0, 0
        if abs(self.rect.centerx - player.rect.centerx) > abs(self.rect.centery - player.rect.centery):
            if self.rect.centerx < player.rect.centerx:
                dx = move_step
                self.direction = 'right'
            elif self.rect.centerx > player.rect.centerx:
                dx = -move_step
                self.direction = 'left'
            if self.check_collision(self.rect.x + dx, self.rect.y):
                dx = 0
                if self.rect.centery < player.rect.centery:
                    dy = move_step
                    self.direction = 'down'
                elif self.rect.centery > player.rect.centery:
                    dy = -move_step
                    self.direction = 'up'
        else:
            if self.rect.centery < player.rect.centery:
                dy = move_step
                self.direction = 'down'
            elif self.rect.centery > player.rect.centery:
                dy = -move_step
                self.direction = 'up'
            if self.check_collision(self.rect.x, self.rect.y + dy):
                dy = 0
                if self.rect.centerx < player.rect.centerx:
                    dx = move_step
                    self.direction = 'right'
                elif self.rect.centerx > player.rect.centerx:
                    dx = -move_step
                    self.direction = 'left'
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        if not self.check_collision(new_x, self.rect.y):
            self.rect.x = new_x
        if not self.check_collision(self.rect.x, new_y):
            self.rect.y = new_y

    def attack(self, player):
        if self.shoot_timer <= 0:
            predicted_direction = self.predict_player_movement(player)
            if self.can_shoot_player(predicted_direction, player):
                self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, predicted_direction))
                self.shoot_timer = 60
        self.shoot_timer -= 1

    def predict_player_movement(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        if abs(dx) > abs(dy):
            return 'right' if dx > 0 else 'left'
        else:
            return 'down' if dy > 0 else 'up'

    def can_shoot_player(self, direction, player):
        return is_clear_path(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)

    def can_see_player(self, player):
        distance = ((self.rect.centerx - player.rect.centerx)**2 + (self.rect.centery - player.rect.centery)**2)**0.5
        vision_distance = VISION_DISTANCE / 2 if player.is_crawling else VISION_DISTANCE
        return distance < vision_distance and is_clear_path(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)

    def check_collision(self, x, y):
        test_rect = pygame.Rect(x, y, int(CELL_SIZE * 1.5), int(CELL_SIZE * 1.5))
        if characters:
            char_rect = pygame.Rect(characters[0]['position'][0], characters[0]['position'][1], CELL_SIZE * 1.5, CELL_SIZE * 1.5)
            if test_rect.colliderect(char_rect):
                return True
        return test_rect.collidelist([pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE) for wall in walls]) != -1

    def draw(self, surface, camera_offset):
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        if screen_x > WIDTH or screen_x + self.rect.width < 0 or screen_y > HEIGHT or screen_y + self.rect.height < 0:
            return
        if bot_animations[self.direction] and bot_animations[self.direction]:
            current_time = pygame.time.get_ticks()
            time_elapsed = (current_time - self.start_time) % self.animation_duration
            frame_count = len(bot_animations[self.direction])
            frame = int(time_elapsed / (self.animation_duration / frame_count))
            surface.blit(bot_animations[self.direction][frame], (screen_x, screen_y))
        else:
            pygame.draw.rect(surface, (0, 0, 255), (screen_x, screen_y, self.rect.width, self.rect.height))

        health_bar_width = self.rect.width
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        current_health_width = health_bar_width * health_ratio
        pygame.draw.rect(surface, (255, 0, 0), (screen_x, screen_y - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (screen_x, screen_y - 10, current_health_width, health_bar_height))

        if self.can_see_player(player):
            exclamation_text = exclamation_font.render("!", True, (255, 0, 0))
            exclamation_rect = exclamation_text.get_rect(center=(self.rect.centerx - camera_offset[0], self.rect.top - 20 - camera_offset[1]))
            surface.blit(exclamation_text, exclamation_rect)

        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
            else:
                bullet_screen_x = bullet.rect.x - camera_offset[0]
                bullet_screen_y = bullet.rect.y - camera_offset[1]
                if 0 <= bullet_screen_x < WIDTH and 0 <= bullet_screen_y < HEIGHT:
                    pygame.draw.rect(surface, (0, 0, 255), (bullet_screen_x, bullet_screen_y, 5, 5))

class HealthPack:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.used = False

class PickupMessage:
    def __init__(self, text, position, duration=2000):
        self.text = text
        self.position = position
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration

class DialogMessage:
    def __init__(self, text, message_type, position=None, duration=2000, typing_speed=150):
        self.text = text
        self.type = message_type
        self.position = position
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.displayed_text = ""
        self.char_index = 0
        self.typing_speed = typing_speed
        self.last_char_time = pygame.time.get_ticks()
        self.typing_complete = False
        self.typing_complete_time = None

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.char_index < len(self.text):
            if current_time - self.last_char_time >= self.typing_speed:
                self.displayed_text += self.text[self.char_index]
                self.char_index += 1
                self.last_char_time = current_time
                if self.char_index >= len(self.text):
                    self.typing_complete = True
                    self.typing_complete_time = current_time
        elif self.typing_complete and current_time - self.typing_complete_time > self.duration:
            return True
        return False

    def is_expired(self):
        return self.typing_complete and pygame.time.get_ticks() - self.typing_complete_time > self.duration

def get_line_cells(x1, y1, x2, y2):
    cells = []
    x1, y1 = x1 // CELL_SIZE, y1 // CELL_SIZE
    x2, y2 = x2 // CELL_SIZE, y2 // CELL_SIZE
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        cells.append((x1 * CELL_SIZE, y1 * CELL_SIZE))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return cells

def is_clear_path(x1, y1, x2, y2):
    cells = get_line_cells(x1, y1, x2, y2)
    for cell in cells:
        if any(wall[0] == cell[0] and wall[1] == cell[1] for wall in walls):
            return False
        if characters and (cell[0] == characters[0]['position'][0] and cell[1] == characters[0]['position'][1]):
            return False
    return True

def create_bots_at_mouse(x, y):
    global bots
    create_bot(x, y)

def create_bot(x, y):
    global bots
    new_bot_rect = pygame.Rect(x, y, int(CELL_SIZE * 1.5), int(CELL_SIZE * 1.5))
    if not any(new_bot_rect.colliderect(bot.rect) for bot in bots):
        bots.append(Bot(x, y))

def place_ammo_at_mouse(grid_x, grid_y):
    if not any(wall[0] == grid_x and wall[1] == grid_y for wall in walls):
        if not any(pack.x == grid_x and pack.y == grid_y for pack in ammo_packs):
            new_rect = pygame.Rect(grid_x, grid_y, CELL_SIZE, CELL_SIZE)
            ammo_packs.append(new_rect)

def place_health_at_mouse(grid_x, grid_y):
    if not any(wall[0] == grid_x and wall[1] == grid_y for wall in walls):
        if not any(pack.rect.x == grid_x and pack.rect.y == grid_y for pack in health_packs):
            new_pack = HealthPack(grid_x, grid_y)
            health_packs.append(new_pack)

def erase_objects(world_x, world_y):
    if not eraser_mode:
        return
    click_area_width = brush_size * CELL_SIZE
    click_area_height = brush_size * CELL_SIZE
    click_area_x = world_x - click_area_width / 2
    click_area_y = world_y - click_area_height / 2
    click_area = pygame.Rect(click_area_x, click_area_y, click_area_width, click_area_height)

    health_to_remove = [pack for pack in health_packs if pack.rect.colliderect(click_area)]
    for pack in health_to_remove:
        health_packs.remove(pack)

    if placement_mode == 'bots':
        bots_to_remove = [bot for bot in bots if bot.rect.colliderect(click_area)]
        for bot in bots_to_remove:
            bots.remove(bot)
    elif placement_mode == 'ammo':
        ammo_to_remove = [pack for pack in ammo_packs if pack.colliderect(click_area)]
        for pack in ammo_to_remove:
            ammo_packs.remove(pack)
    elif placement_mode == 'door':
        doors_to_remove = [door for door in doors if pygame.Rect(door[0], door[1], CELL_SIZE, CELL_SIZE).colliderect(click_area)]
        for door in doors_to_remove:
            doors.remove(door)
    if characters:
        char_rect = pygame.Rect(characters[0]['position'][0], characters[0]['position'][1], CELL_SIZE * 1.5, CELL_SIZE * 1.5)
        if char_rect.colliderect(click_area):
            characters.clear()

def load_texture(path):
    if path is None:
        return None
    if path not in texture_cache:
        if os.path.exists(path):
            texture_cache[path] = pygame.image.load(path).convert()
        else:
            print(f"Текстура не найдена: {path}")
            texture_cache[path] = None
    return texture_cache[path]

def draw_grid(camera_offset):
    start_x = camera_offset[0] - (camera_offset[0] % CELL_SIZE)
    start_y = camera_offset[1] - (camera_offset[1] % CELL_SIZE)
    end_x = start_x + WIDTH + CELL_SIZE
    end_y = start_y + HEIGHT + CELL_SIZE

    for x in range(int(start_x), int(end_x), CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x - camera_offset[0], 0), (x - camera_offset[0], HEIGHT))
    for y in range(int(start_y), int(end_y), CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y - camera_offset[1]), (WIDTH, y - camera_offset[1]))

    for tile in floor_tiles:
        x, y, color, texture_path = tile
        screen_x = x - camera_offset[0]
        screen_y = y - camera_offset[1]
        if screen_x + CELL_SIZE > 0 and screen_x < WIDTH and screen_y + CELL_SIZE > 0 and screen_y < HEIGHT:
            if texture_path:
                texture = load_texture(texture_path)
                if texture:
                    scaled_texture = pygame.transform.scale(texture, (CELL_SIZE, CELL_SIZE))
                    screen.blit(scaled_texture, (screen_x, screen_y))
                else:
                    pygame.draw.rect(screen, floor_color, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
            elif color:
                pygame.draw.rect(screen, color, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, floor_color, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))

    for wall in walls:
        x, y, color, texture_path = wall
        screen_x = x - camera_offset[0]
        screen_y = y - camera_offset[1]
        if screen_x + CELL_SIZE > 0 and screen_x < WIDTH and screen_y + CELL_SIZE > 0 and screen_y < HEIGHT:
            if texture_path:
                texture = load_texture(texture_path)
                if texture:
                    scaled_texture = pygame.transform.scale(texture, (CELL_SIZE, CELL_SIZE))
                    screen.blit(scaled_texture, (screen_x, screen_y))
                else:
                    pygame.draw.rect(screen, WALL_COLOR, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
            elif color:
                pygame.draw.rect(screen, color, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WALL_COLOR, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))

    for door in doors:
        x, y, _, _ = door
        screen_x = x - camera_offset[0]
        screen_y = y - camera_offset[1]
        if screen_x + CELL_SIZE > 0 and screen_x < WIDTH and screen_y + CELL_SIZE > 0 and screen_y < HEIGHT:
            texture = load_texture(door_texture_path)
            if texture:
                scaled_texture = pygame.transform.scale(texture, (CELL_SIZE, CELL_SIZE))
                screen.blit(scaled_texture, (screen_x, screen_y))
            else:
                pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y, CELL_SIZE, CELL_SIZE))

    for pack in ammo_packs:
        screen_x = pack.x - camera_offset[0]
        screen_y = pack.y - camera_offset[1]
        if screen_x + CELL_SIZE > 0 and screen_x < WIDTH and screen_y + CELL_SIZE > 0 and screen_y < HEIGHT:
            if ammo_texture_path:
                texture = load_texture(ammo_texture_path)
                if texture:
                    scaled_texture = pygame.transform.scale(texture, (CELL_SIZE, CELL_SIZE))
                    screen.blit(scaled_texture, (screen_x, screen_y))
                else:
                    pygame.draw.rect(screen, (255, 255, 0), (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, (255, 255, 0), (screen_x, screen_y, CELL_SIZE, CELL_SIZE))

    for pack in health_packs:
        screen_x = pack.rect.x - camera_offset[0]
        screen_y = pack.rect.y - camera_offset[1]
        if screen_x + CELL_SIZE > 0 and screen_x < WIDTH and screen_y + CELL_SIZE > 0 and screen_y < HEIGHT:
            if health_texture_path:
                texture = load_texture(health_texture_path)
                if texture:
                    scaled_texture = pygame.transform.scale(texture, (CELL_SIZE, CELL_SIZE))
                    screen.blit(scaled_texture, (screen_x, screen_y))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                cross_arm_length = CELL_SIZE // 3
                cross_thickness = 2
                center_x = screen_x + CELL_SIZE // 2
                center_y = screen_y + CELL_SIZE // 2
                pygame.draw.line(screen, (255, 0, 0),
                                 (center_x, center_y - cross_arm_length // 2),
                                 (center_x, center_y + cross_arm_length // 2),
                                 cross_thickness)
                pygame.draw.line(screen, (255, 0, 0),
                                 (center_x - cross_arm_length // 2, center_y),
                                 (center_x + cross_arm_length // 2, center_y),
                                 cross_thickness)

    for char in characters:
        screen_x = char['position'][0] - camera_offset[0]
        screen_y = char['position'][1] - camera_offset[1]
        texture = load_texture(char['texture'])
        if texture:
            scaled_texture = pygame.transform.scale(texture, (int(CELL_SIZE * 1.5), int(CELL_SIZE * 1.5)))
            screen.blit(scaled_texture, (screen_x, screen_y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y, int(CELL_SIZE * 1.5), int(CELL_SIZE * 1.5)))

def choose_wall_color():
    global WALL_COLOR
    color = colorchooser.askcolor(title="Выберите цвет стены")
    if color[0] is not None:
        WALL_COLOR = tuple(int(c) for c in color[0])

def choose_floor_color():
    global floor_color
    color = colorchooser.askcolor(title="Выберите цвет пола")
    if color[0] is not None:
        floor_color = tuple(int(c) for c in color[0])

def save_level():
    global walkie_talkie_message, music_path
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        level_data = {
            'walls': [(wall[0], wall[1], list(wall[2]) if wall[2] else None, os.path.basename(wall[3]) if wall[3] else None) for wall in walls],
            'floor': [(tile[0], tile[1], list(tile[2]) if tile[2] else None, os.path.basename(tile[3]) if tile[3] else None) for tile in floor_tiles],
            'floor_color': floor_color,
            'bots': [(bot.rect.x, bot.rect.y) for bot in bots],
            'wall_color': WALL_COLOR,
            'player_position': (player.rect.x, player.rect.y),
            'ammo_packs': [(pack.x, pack.y) for pack in ammo_packs],
            'health_packs': [(pack.rect.x, pack.rect.y) for pack in health_packs],
            'walkie_talkie_message': walkie_talkie_message,
            'doors': [(door[0], door[1], door[2], os.path.basename(door[3]) if door[3] else None) for door in doors],
            'cutscene_actions': cutscene_actions,
            'characters': [{'texture': os.path.basename(characters[0]['texture']), 'position': characters[0]['position']}] if characters else [],
            'music_path': os.path.basename(music_path) if music_path else None,
            'textures': {
                'player_up': os.path.basename(player_up_path) if player_up_path else None,
                'player_down': os.path.basename(player_down_path) if player_down_path else None,
                'player_left': os.path.basename(player_left_path) if player_left_path else None,
                'player_right': os.path.basename(player_right_path) if player_right_path else None,
                'player_crawl_up': os.path.basename(player_crawl_up_path) if player_crawl_up_path else None,
                'player_crawl_down': os.path.basename(player_crawl_down_path) if player_crawl_down_path else None,
                'player_crawl_left': os.path.basename(player_crawl_left_path) if player_crawl_left_path else None,
                'player_crawl_right': os.path.basename(player_crawl_right_path) if player_crawl_right_path else None,
                'bot_up': os.path.basename(bot_up_path) if bot_up_path else None,
                'bot_down': os.path.basename(bot_down_path) if bot_down_path else None,
                'bot_left': os.path.basename(bot_left_path) if bot_left_path else None,
                'bot_right': os.path.basename(bot_right_path) if bot_right_path else None,
                'ammo': os.path.basename(ammo_texture_path) if ammo_texture_path else None,
                'health': os.path.basename(health_texture_path) if health_texture_path else None,
                'pistol': os.path.basename(pistol_texture_path) if pistol_texture_path else None,
                'walkie_talkie': os.path.basename(walkie_talkie_texture_path) if walkie_talkie_texture_path else None,
                'door': os.path.basename(door_texture_path) if door_texture_path else None,
            }
        }
        with open(file_path, 'w') as f:
            json.dump(level_data, f)

def save_level_to_path(file_path):
    global walkie_talkie_message, music_path
    if file_path:
        level_data = {
            'walls': [(wall[0], wall[1], list(wall[2]) if wall[2] else None, os.path.basename(wall[3]) if wall[3] else None) for wall in walls],
            'floor': [(tile[0], tile[1], list(tile[2]) if tile[2] else None, os.path.basename(tile[3]) if tile[3] else None) for tile in floor_tiles],
            'floor_color': floor_color,
            'bots': [(bot.rect.x, bot.rect.y) for bot in bots],
            'wall_color': WALL_COLOR,
            'player_position': (player.rect.x, player.rect.y),
            'ammo_packs': [(pack.x, pack.y) for pack in ammo_packs],
            'health_packs': [(pack.rect.x, pack.rect.y) for pack in health_packs],
            'walkie_talkie_message': walkie_talkie_message,
            'doors': [(door[0], door[1], door[2], os.path.basename(door[3]) if door[3] else None) for door in doors],
            'cutscene_actions': cutscene_actions,
            'characters': [{'texture': os.path.basename(characters[0]['texture']), 'position': characters[0]['position']}] if characters else [],
            'music_path': os.path.basename(music_path) if music_path else None,
            'textures': {
                'player_up': os.path.basename(player_up_path) if player_up_path else None,
                'player_down': os.path.basename(player_down_path) if player_down_path else None,
                'player_left': os.path.basename(player_left_path) if player_left_path else None,
                'player_right': os.path.basename(player_right_path) if player_right_path else None,
                'player_crawl_up': os.path.basename(player_crawl_up_path) if player_crawl_up_path else None,
                'player_crawl_down': os.path.basename(player_crawl_down_path) if player_crawl_down_path else None,
                'player_crawl_left': os.path.basename(player_crawl_left_path) if player_crawl_left_path else None,
                'player_crawl_right': os.path.basename(player_crawl_right_path) if player_crawl_right_path else None,
                'bot_up': os.path.basename(bot_up_path) if bot_up_path else None,
                'bot_down': os.path.basename(bot_down_path) if bot_down_path else None,
                'bot_left': os.path.basename(bot_left_path) if bot_left_path else None,
                'bot_right': os.path.basename(bot_right_path) if bot_right_path else None,
                'ammo': os.path.basename(ammo_texture_path) if ammo_texture_path else None,
                'health': os.path.basename(health_texture_path) if health_texture_path else None,
                'pistol': os.path.basename(pistol_texture_path) if pistol_texture_path else None,
                'walkie_talkie': os.path.basename(walkie_talkie_texture_path) if walkie_talkie_texture_path else None,
                'door': os.path.basename(door_texture_path) if door_texture_path else None,
            }
        }
        with open(file_path, 'w') as f:
            json.dump(level_data, f)

def load_level():
    global walls, floor_tiles, floor_color, bots, WALL_COLOR, player, ammo_packs, health_packs, walkie_talkie_message, doors, current_level_path, cutscene_actions, characters, in_cutscene, cutscene_start_time, black_bar_height, cutscene_index, initial_player_position, initial_bots_positions, player_animations, bot_animations, ammo_texture_path, health_texture_path, pistol_texture_path, walkie_talkie_texture_path, door_texture_path, music_path, pistol_image, walkie_talkie_image
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as f:
            level_data = json.load(f)
            walls = []
            for x, y, color, texture_path in level_data['walls']:
                full_texture_path = os.path.join("Текстуры", texture_path) if texture_path else None
                walls.append((x, y, tuple(color) if color else None, full_texture_path))
            floor_tiles = []
            for x, y, color, texture_path in level_data['floor']:
                full_texture_path = os.path.join("Текстуры", texture_path) if texture_path else None
                floor_tiles.append((x, y, tuple(color) if color else None, full_texture_path))
            floor_color = level_data.get('floor_color', (200, 200, 200))
            WALL_COLOR = level_data.get('wall_color', (0, 0, 0))
            bots = [Bot(x, y) for x, y in level_data.get('bots', [])]
            player.rect.x, player.rect.y = level_data.get('player_position', (0, 0))
            player.reset_target()
            ammo_packs = [pygame.Rect(x, y, CELL_SIZE, CELL_SIZE) for x, y in level_data.get('ammo_packs', [])]
            health_packs = [HealthPack(x, y) for x, y in level_data.get('health_packs', [])]
            walkie_talkie_message = level_data.get('walkie_talkie_message', "")
            doors = []
            for door_data in level_data.get('doors', []):
                x, y, door_type, json_filename = door_data
                json_path = os.path.join(os.path.dirname(file_path), json_filename) if json_filename else None
                doors.append((x, y, door_type, json_path))
            cutscene_actions = level_data.get('cutscene_actions', [])
            characters = [{'texture': os.path.join("Текстуры", char['texture']), 'position': char['position']} for char in level_data.get('characters', [])]
            initial_player_position = level_data.get('player_position', (0, 0))
            initial_bots_positions = level_data.get('bots', [])
            music_path = os.path.join("Музыка", level_data.get('music_path', '')) if level_data.get('music_path') else None
            if music_path and os.path.exists(music_path):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
            else:
                print(f"Музыка не найдена: {music_path}")
            textures = level_data.get('textures', {})
            player_up_path = os.path.join("Анимации", textures.get('player_up', '')) if textures.get('player_up') else None
            player_animations['up'] = load_gif(player_up_path)
            player_down_path = os.path.join("Анимации", textures.get('player_down', '')) if textures.get('player_down') else None
            player_animations['down'] = load_gif(player_down_path)
            player_left_path = os.path.join("Анимации", textures.get('player_left', '')) if textures.get('player_left') else None
            player_animations['left'] = load_gif(player_left_path)
            player_right_path = os.path.join("Анимации", textures.get('player_right', '')) if textures.get('player_right') else None
            player_animations['right'] = load_gif(player_right_path)
            player_crawl_up_path = os.path.join("Анимации", textures.get('player_crawl_up', '')) if textures.get('player_crawl_up') else None
            player_animations['crawl_up'] = load_gif(player_crawl_up_path)
            player_crawl_down_path = os.path.join("Анимации", textures.get('player_crawl_down', '')) if textures.get('player_crawl_down') else None
            player_animations['crawl_down'] = load_gif(player_crawl_down_path)
            player_crawl_left_path = os.path.join("Анимации", textures.get('player_crawl_left', '')) if textures.get('player_crawl_left') else None
            player_animations['crawl_left'] = load_gif(player_crawl_left_path)
            player_crawl_right_path = os.path.join("Анимации", textures.get('player_crawl_right', '')) if textures.get('player_crawl_right') else None
            player_animations['crawl_right'] = load_gif(player_crawl_right_path)
            bot_up_path = os.path.join("Анимации", textures.get('bot_up', '')) if textures.get('bot_up') else None
            bot_animations['up'] = load_gif(bot_up_path)
            bot_down_path = os.path.join("Анимации", textures.get('bot_down', '')) if textures.get('bot_down') else None
            bot_animations['down'] = load_gif(bot_down_path)
            bot_left_path = os.path.join("Анимации", textures.get('bot_left', '')) if textures.get('bot_left') else None
            bot_animations['left'] = load_gif(bot_left_path)
            bot_right_path = os.path.join("Анимации", textures.get('bot_right', '')) if textures.get('bot_right') else None
            bot_animations['right'] = load_gif(bot_right_path)
            ammo_texture_path = os.path.join("Текстуры", textures.get('ammo', '')) if textures.get('ammo') else None
            health_texture_path = os.path.join("Текстуры", textures.get('health', '')) if textures.get('health') else None
            pistol_texture_path = os.path.join("Текстуры", textures.get('pistol', '')) if textures.get('pistol') else None
            walkie_talkie_texture_path = os.path.join("Текстуры", textures.get('walkie_talkie', '')) if textures.get('walkie_talkie') else None
            door_texture_path = os.path.join("Текстуры", textures.get('door', '')) if textures.get('door') else None
            if pistol_texture_path and os.path.exists(pistol_texture_path):
                try:
                    pistol_image = pygame.image.load(pistol_texture_path).convert_alpha()
                    pistol_image = pygame.transform.scale(pistol_image, (144, 144))
                except pygame.error as e:
                    print(f"Ошибка загрузки текстуры пистолета: {e}")
                    pistol_image = None
            else:
                pistol_image = None
            if walkie_talkie_texture_path and os.path.exists(walkie_talkie_texture_path):
                try:
                    walkie_talkie_image = pygame.image.load(walkie_talkie_texture_path).convert_alpha()
                    walkie_talkie_image = pygame.transform.scale(walkie_talkie_image, (144, 144))
                except pygame.error as e:
                    print(f"Ошибка загрузки текстуры рации: {e}")
                    walkie_talkie_image = None
            else:
                walkie_talkie_image = None
        current_level_path = file_path
        if cutscene_actions:
            in_cutscene = True
            cutscene_start_time = pygame.time.get_ticks() + 1000
            black_bar_height = 0
            cutscene_index = 0

def load_level_from_path(file_path):
    global walls, floor_tiles, floor_color, bots, WALL_COLOR, player, ammo_packs, health_packs, walkie_talkie_message, doors, current_level_path, cutscene_actions, characters, in_cutscene, cutscene_start_time, black_bar_height, cutscene_index, initial_player_position, initial_bots_positions, player_animations, bot_animations, ammo_texture_path, health_texture_path, pistol_texture_path, walkie_talkie_texture_path, door_texture_path, music_path, pistol_image, walkie_talkie_image
    if file_path:
        with open(file_path, 'r') as f:
            level_data = json.load(f)
            walls = []
            for x, y, color, texture_path in level_data['walls']:
                full_texture_path = os.path.join("Текстуры", texture_path) if texture_path else None
                walls.append((x, y, tuple(color) if color else None, full_texture_path))
            floor_tiles = []
            for x, y, color, texture_path in level_data['floor']:
                full_texture_path = os.path.join("Текстуры", texture_path) if texture_path else None
                floor_tiles.append((x, y, tuple(color) if color else None, full_texture_path))
            floor_color = level_data.get('floor_color', (200, 200, 200))
            WALL_COLOR = level_data.get('wall_color', (0, 0, 0))
            bots = [Bot(x, y) for x, y in level_data.get('bots', [])]
            player.rect.x, player.rect.y = level_data.get('player_position', (0, 0))
            player.reset_target()
            ammo_packs = [pygame.Rect(x, y, CELL_SIZE, CELL_SIZE) for x, y in level_data.get('ammo_packs', [])]
            health_packs = [HealthPack(x, y) for x, y in level_data.get('health_packs', [])]
            walkie_talkie_message = level_data.get('walkie_talkie_message', "")
            doors = []
            for door_data in level_data.get('doors', []):
                x, y, door_type, json_filename = door_data
                json_path = os.path.join(os.path.dirname(file_path), json_filename) if json_filename else None
                doors.append((x, y, door_type, json_path))
            cutscene_actions = level_data.get('cutscene_actions', [])
            characters = [{'texture': os.path.join("Текстуры", char['texture']), 'position': char['position']} for char in level_data.get('characters', [])]
            initial_player_position = level_data.get('player_position', (0, 0))
            initial_bots_positions = level_data.get('bots', [])
            music_path = os.path.join("Музыка", level_data.get('music_path', '')) if level_data.get('music_path') else None
            if music_path and os.path.exists(music_path):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
            else:
                print(f"Музыка не найдена: {music_path}")
            textures = level_data.get('textures', {})
            player_up_path = os.path.join("Анимации", textures.get('player_up', '')) if textures.get('player_up') else None
            player_animations['up'] = load_gif(player_up_path)
            player_down_path = os.path.join("Анимации", textures.get('player_down', '')) if textures.get('player_down') else None
            player_animations['down'] = load_gif(player_down_path)
            player_left_path = os.path.join("Анимации", textures.get('player_left', '')) if textures.get('player_left') else None
            player_animations['left'] = load_gif(player_left_path)
            player_right_path = os.path.join("Анимации", textures.get('player_right', '')) if textures.get('player_right') else None
            player_animations['right'] = load_gif(player_right_path)
            player_crawl_up_path = os.path.join("Анимации", textures.get('player_crawl_up', '')) if textures.get('player_crawl_up') else None
            player_animations['crawl_up'] = load_gif(player_crawl_up_path)
            player_crawl_down_path = os.path.join("Анимации", textures.get('player_crawl_down', '')) if textures.get('player_crawl_down') else None
            player_animations['crawl_down'] = load_gif(player_crawl_down_path)
            player_crawl_left_path = os.path.join("Анимации", textures.get('player_crawl_left', '')) if textures.get('player_crawl_left') else None
            player_animations['crawl_left'] = load_gif(player_crawl_left_path)
            player_crawl_right_path = os.path.join("Анимации", textures.get('player_crawl_right', '')) if textures.get('player_crawl_right') else None
            player_animations['crawl_right'] = load_gif(player_crawl_right_path)
            bot_up_path = os.path.join("Анимации", textures.get('bot_up', '')) if textures.get('bot_up') else None
            bot_animations['up'] = load_gif(bot_up_path)
            bot_down_path = os.path.join("Анимации", textures.get('bot_down', '')) if textures.get('bot_down') else None
            bot_animations['down'] = load_gif(bot_down_path)
            bot_left_path = os.path.join("Анимации", textures.get('bot_left', '')) if textures.get('bot_left') else None
            bot_animations['left'] = load_gif(bot_left_path)
            bot_right_path = os.path.join("Анимации", textures.get('bot_right', '')) if textures.get('bot_right') else None
            bot_animations['right'] = load_gif(bot_right_path)
            ammo_texture_path = os.path.join("Текстуры", textures.get('ammo', '')) if textures.get('ammo') else None
            health_texture_path = os.path.join("Текстуры", textures.get('health', '')) if textures.get('health') else None
            pistol_texture_path = os.path.join("Текстуры", textures.get('pistol', '')) if textures.get('pistol') else None
            walkie_talkie_texture_path = os.path.join("Текстуры", textures.get('walkie_talkie', '')) if textures.get('walkie_talkie') else None
            door_texture_path = os.path.join("Текстуры", textures.get('door', '')) if textures.get('door') else None
            if pistol_texture_path and os.path.exists(pistol_texture_path):
                try:
                    pistol_image = pygame.image.load(pistol_texture_path).convert_alpha()
                    pistol_image = pygame.transform.scale(pistol_image, (144, 144))
                except pygame.error as e:
                    print(f"Ошибка загрузки текстуры пистолета: {e}")
                    pistol_image = None
            else:
                pistol_image = None
            if walkie_talkie_texture_path and os.path.exists(walkie_talkie_texture_path):
                try:
                    walkie_talkie_image = pygame.image.load(walkie_talkie_texture_path).convert_alpha()
                    walkie_talkie_image = pygame.transform.scale(walkie_talkie_image, (144, 144))
                except pygame.error as e:
                    print(f"Ошибка загрузки текстуры рации: {e}")
                    walkie_talkie_image = None
            else:
                walkie_talkie_image = None
        current_level_path = file_path
        if cutscene_actions:
            in_cutscene = True
            cutscene_start_time = pygame.time.get_ticks() + 1000
            black_bar_height = 0
            cutscene_index = 0

def move_player_with_mouse():
    global can_move_player
    can_move_player = not can_move_player

def toggle_eraser_mode():
    global eraser_mode
    eraser_mode = not eraser_mode

def toggle_pause():
    global is_paused
    is_paused = not is_paused

def cycle_volume():
    global volume
    volume = round((volume + 0.1) % 1.1, 1)
    if volume > 1.0:
        volume = 0.0
    pygame.mixer.music.set_volume(volume)

def cycle_brush_size():
    global brush_size
    brush_size = (brush_size % 18) + 1

def toggle_placement_mode():
    global placement_mode
    if placement_mode == 'bots':
        placement_mode = 'ammo'
    elif placement_mode == 'ammo':
        placement_mode = 'health'
    else:
        placement_mode = 'bots'

def set_placement_mode(mode):
    global placement_mode
    placement_mode = mode

def load_floor_texture():
    global floor_texture_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        floor_texture_path = file_path

def load_wall_texture():
    global wall_texture_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        wall_texture_path = file_path

def open_walkie_talkie_input():
    input_window = tk.Toplevel()
    input_window.title("Сказать в рацию")
    tk.Label(input_window, text="Введите сообщение:").pack(pady=10)
    message_entry = tk.Entry(input_window, width=50)
    message_entry.pack(pady=10)
    def submit_message():
        global walkie_talkie_message
        walkie_talkie_message = message_entry.get()
        input_window.destroy()
    tk.Button(input_window, text="Отправить", command=submit_message).pack(pady=10)

def open_cutscene_editor():
    cutscene_window = tk.Toplevel()
    cutscene_window.title("Редактор кат-сцены")

    tk.Button(cutscene_window, text="Сказать игроку", command=lambda: add_action('say_player')).pack(pady=5)
    tk.Button(cutscene_window, text="Сказать рации", command=lambda: add_action('say_walkie_talkie')).pack(pady=5)
    tk.Button(cutscene_window, text="Добавить текстуру персонажа", command=add_character_texture).pack(pady=5)
    tk.Button(cutscene_window, text="Сказать персонажу", command=lambda: add_action('say_character')).pack(pady=5)

    tk.Label(cutscene_window, text="Последовательность действий:").pack()
    action_listbox = tk.Listbox(cutscene_window)
    action_listbox.pack(fill=tk.BOTH, expand=True)

    def update_action_list():
        action_listbox.delete(0, tk.END)
        for idx, action in enumerate(cutscene_actions):
            action_type = action['type']
            message = action['data'].get('message', 'No message')
            display_text = f"{idx}: {action_type} - {message}"
            action_listbox.insert(tk.END, display_text)

    def delete_action():
        selected = action_listbox.curselection()
        if selected:
            idx = selected[0]
            del cutscene_actions[idx]
            update_action_list()

    def edit_action():
        selected = action_listbox.curselection()
        if selected:
            idx = selected[0]
            action = cutscene_actions[idx]
            if action['type'] in ['say_player', 'say_walkie_talkie', 'say_character']:
                new_message = simpledialog.askstring("Редактировать сообщение", "Введите новое сообщение:", initialvalue=action['data']['message'])
                if new_message:
                    action['data']['message'] = new_message
                    update_action_list()

    def save_and_play_cutscene():
        global in_cutscene, cutscene_start_time, black_bar_height, cutscene_index
        in_cutscene = True
        cutscene_start_time = pygame.time.get_ticks() + 1000
        black_bar_height = 0
        cutscene_index = 0
        cutscene_window.destroy()

    tk.Button(cutscene_window, text="Удалить действие", command=delete_action).pack(pady=5)
    tk.Button(cutscene_window, text="Редактировать действие", command=edit_action).pack(pady=5)
    tk.Button(cutscene_window, text="Сохранить и запустить", command=save_and_play_cutscene).pack(pady=5)

    update_action_list()

def add_action(action_type):
    global cutscene_actions
    action_data = {}
    if action_type == 'say_player':
        message = simpledialog.askstring("Сказать игроку", "Введите сообщение для игрока:")
        if message:
            action_data['message'] = message
    elif action_type == 'say_walkie_talkie':
        message = simpledialog.askstring("Сказать рации", "Введите сообщение для рации:")
        if message:
            action_data['message'] = message
    elif action_type == 'say_character':
        if characters:
            message = simpledialog.askstring("Сказать персонажу", "Введите сообщение для персонажа:")
            if message:
                action_data['message'] = message
        else:
            tk.messagebox.showwarning("Предупреждение", "На уровне нет персонажа!")
            return
    if action_data:
        cutscene_actions.append({'type': action_type, 'data': action_data})
        open_cutscene_editor()

def add_character_texture():
    global characters, placement_mode
    texture_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if texture_path:
        if characters:
            characters.clear()
        characters.append({'texture': texture_path, 'position': (0, 0)})
        set_placement_mode('character')

def load_music():
    global music_path
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        music_path = file_path
        pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

def toggle_wall_mode():
    global wall_drawing_mode
    wall_drawing_mode = 'texture' if wall_drawing_mode == 'color' else 'color'

def toggle_floor_mode():
    global floor_drawing_mode
    floor_drawing_mode = 'texture' if floor_drawing_mode == 'color' else 'color'

def back_to_menu():
    global return_to_menu, running
    return_to_menu = True
    running = False

def clear_field():
    global walls, floor_tiles, bots, ammo_packs, health_packs, doors, characters, player
    walls.clear()
    floor_tiles.clear()
    bots.clear()
    ammo_packs.clear()
    health_packs.clear()
    doors.clear()
    characters.clear()
    player = Turtle()
    player.rect.topleft = (0, 0)
    player.reset_target()

def display_message(surface, message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(text, text_rect)

def round_to_grid(x, y):
    return round(x / CELL_SIZE) * CELL_SIZE, round(y / CELL_SIZE) * CELL_SIZE

def draw_health_bar(surface, current_health, max_health):
    bar_width = 100
    bar_height = 20
    bar_x = 10
    bar_y = 10
    pygame.draw.rect(surface, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)
    pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    health_ratio = current_health / max_health
    current_health_width = bar_width * health_ratio
    pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, current_health_width, bar_height))
    health_text = font.render(f"HP: {current_health}/{max_health}", True, (0, 0, 0))
    surface.blit(health_text, (bar_x, bar_y + bar_height + 5))

def paint_area(target_list, i_center, j_center, brush_size, color, eraser):
    texture_path = None
    if target_list is walls and wall_drawing_mode == 'texture':
        texture_path = wall_texture_path
    elif target_list is floor_tiles and floor_drawing_mode == 'texture':
        texture_path = floor_texture_path
    i_start = i_center - (brush_size // 2)
    j_start = j_center - (brush_size // 2)
    for di in range(brush_size):
        for dj in range(brush_size):
            i = i_start + di
            j = j_start + dj
            x = i * CELL_SIZE
            y = j * CELL_SIZE
            if eraser:
                target_list[:] = [item for item in target_list if (item[0], item[1]) != (x, y)]
                if target_list == walls:
                    doors[:] = [door for door in doors if (door[0], door[1]) != (x, y)]
            else:
                if not any((item[0], item[1]) == (x, y) for item in target_list):
                    if texture_path:
                        target_list.append((x, y, None, texture_path))
                    else:
                        target_list.append((x, y, color, None))

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_dialog_box(surface, text, position, camera_offset):
    lines = wrap_text(text, font, 280 - 20)
    num_lines = len(lines)
    line_height = font.get_height()
    dialog_box_height = (num_lines * line_height) + 20
    dialog_box_rect = pygame.Rect(position[0] - camera_offset[0], position[1] - camera_offset[1] - dialog_box_height - 10, 280, dialog_box_height)
    pygame.draw.rect(surface, (200, 200, 200), dialog_box_rect)
    y_offset = dialog_box_rect.y + 10
    for line in lines:
        text_surface = font.render(line, True, (0, 0, 0))
        surface.blit(text_surface, (dialog_box_rect.x + 10, y_offset))
        y_offset += line_height

def main():
    global is_paused, game_over, in_cutscene, running, current_health, can_move_player, restart_timer, delay_message, WIDTH, HEIGHT, player, black_bar_height, cutscene_index, volume, brush_size, placement_mode, wall_drawing_mode, floor_drawing_mode, walkie_talkie_message, return_to_menu, screen, bots, bullets, pickup_messages
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Turtle-Engine")

    player = Turtle()
    player.rect.topleft = initial_player_position
    bots = [Bot(x, y) for x, y in initial_bots_positions]
    bullets = []
    pickup_messages = []
    dialog_queue = queue.Queue()
    current_dialog = None
    running = True

    panel_width = 200
    walkie_talkie_x = WIDTH - panel_width - 144
    walkie_talkie_y = 0
    dialog_box_x = WIDTH - panel_width - 144
    dialog_box_y = 150
    dialog_box_width = int(144 * 1.5)
    dialog_box_right_padding = 15

    settings_buttons = [
        'Цвета',
        {'label': 'Сменить цвет стены', 'action': choose_wall_color},
        {'label': 'Сменить цвет пола', 'action': choose_floor_color},
        'Текстуры',
        {'label': 'Загрузить текстуры', 'action': open_texture_loader},
        {'label': 'Загрузить текстуру пола', 'action': load_floor_texture},
        {'label': 'Загрузить текстуру стены', 'action': load_wall_texture},
        'Уровень',
        {'label': 'Сохранить уровень', 'action': save_level},
        {'label': 'Загрузить уровень', 'action': load_level},
        'Инструменты',
        {'label': 'Переключить ластик', 'action': toggle_eraser_mode},
        {'label': lambda: f"Размер кисти: {brush_size}", 'action': cycle_brush_size},
        {'label': 'Перемещение игрока', 'action': move_player_with_mouse},
        {'label': 'Переключить режим размещения', 'action': toggle_placement_mode},
        {'label': 'Размещение патронов', 'action': lambda: set_placement_mode('ammo')},
        {'label': 'Размещение аптечек', 'action': lambda: set_placement_mode('health')},
        {'label': 'Поставить дверь', 'action': lambda: set_placement_mode('door')},
        {'label': 'Сказать в рацию', 'action': open_walkie_talkie_input},
        {'label': 'Сделать кат-сцену', 'action': open_cutscene_editor},
        {'label': 'Загрузить музыку', 'action': load_music},
        {'label': 'Вернуться в меню', 'action': back_to_menu},
        {'label': 'Очистить поле', 'action': clear_field},
        'Режимы',
        {'label': lambda: f"Режим стен: {wall_drawing_mode}", 'action': toggle_wall_mode},
        {'label': lambda: f"Режим пола: {floor_drawing_mode}", 'action': toggle_floor_mode},
        'Настройки',
        {'label': lambda: f"Громкость: {volume:.1f}", 'action': cycle_volume},
        {'label': 'Пауза', 'action': toggle_pause},
    ]

    cutscene_index = 0

    while running:
        camera_offset_x = player.rect.centerx - WIDTH // 2
        camera_offset_y = player.rect.centery - HEIGHT // 2
        camera_offset = [camera_offset_x, camera_offset_y]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.size
                if new_width > INITIAL_WIDTH or new_height > INITIAL_HEIGHT:
                    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    WIDTH, HEIGHT = new_width, new_height
                    walkie_talkie_x = WIDTH - panel_width - 144
                    dialog_box_x = WIDTH - panel_width - 144
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not in_cutscene:
                    toggle_pause()
                if event.key == pygame.K_SPACE and not is_paused and not in_cutscene:
                    if player.ammo > 0 and not any(
                            wall[0] <= player.rect.centerx < wall[0] + CELL_SIZE and
                            wall[1] <= player.rect.centery < wall[1] + CELL_SIZE for wall in walls):
                        bullets.append(Bullet(player.rect.centerx, player.rect.centery, player.direction))
                        player.ammo -= 1
                if event.key == pygame.K_t and not is_paused and not in_cutscene and walkie_talkie_message:
                    dialog_queue.put(DialogMessage(walkie_talkie_message, 'walkie_talkie'))
            if event.type == pygame.MOUSEBUTTONDOWN and not in_cutscene:
                mouse_x, mouse_y = event.pos
                if mouse_x >= WIDTH - panel_width:
                    if event.button == 1:
                        y_offset = 10
                        for option in settings_buttons:
                            if isinstance(option, dict):
                                button_rect = pygame.Rect(WIDTH - panel_width + 10, y_offset, panel_width - 20, 30)
                                if button_rect.collidepoint((mouse_x, mouse_y)):
                                    option['action']()
                                y_offset += 40
                            else:
                                y_offset += 20
                else:
                    world_x = mouse_x + camera_offset[0]
                    world_y = mouse_y + camera_offset[1]
                    i_center = round(world_x / CELL_SIZE)
                    j_center = round(world_y / CELL_SIZE)
                    grid_x, grid_y = round_to_grid(world_x, world_y)
                    if event.button == 1:
                        if placement_mode == 'door':
                            json_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
                            if json_path:
                                doors.append((grid_x, grid_y, 1, json_path))
                        elif placement_mode == 'character' and characters:
                            characters[0]['position'] = (grid_x, grid_y)
                            set_placement_mode('bots')
                        else:
                            paint_area(walls, i_center, j_center, brush_size, WALL_COLOR, eraser_mode)
                    if event.button == 2:
                        if eraser_mode:
                            erase_objects(world_x, world_y)
                        else:
                            if placement_mode == 'ammo':
                                place_ammo_at_mouse(grid_x, grid_y)
                            elif placement_mode == 'health':
                                place_health_at_mouse(grid_x, grid_y)
                            else:
                                create_bots_at_mouse(grid_x, grid_y)
                    if event.button == 3:
                        paint_area(floor_tiles, i_center, j_center, brush_size, floor_color, eraser_mode)

        if not in_cutscene:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < WIDTH - panel_width:
                if pygame.mouse.get_pressed()[0]:
                    world_x = mouse_x + camera_offset[0]
                    world_y = mouse_y + camera_offset[1]
                    i_center = round(world_x / CELL_SIZE)
                    j_center = round(world_y / CELL_SIZE)
                    if placement_mode not in ['door', 'character']:
                        paint_area(walls, i_center, j_center, brush_size, WALL_COLOR, eraser_mode)
                if pygame.mouse.get_pressed()[1]:
                    world_x = mouse_x + camera_offset[0]
                    world_y = mouse_y + camera_offset[1]
                    grid_x, grid_y = round_to_grid(world_x, world_y)
                    if eraser_mode:
                        erase_objects(world_x, world_y)
                    else:
                        if placement_mode == 'ammo':
                            place_ammo_at_mouse(grid_x, grid_y)
                        elif placement_mode == 'health':
                            place_health_at_mouse(grid_x, grid_y)
                        else:
                            create_bots_at_mouse(grid_x, grid_y)
                if pygame.mouse.get_pressed()[2]:
                    world_x = mouse_x + camera_offset[0]
                    world_y = mouse_y + camera_offset[1]
                    i_center = round(world_x / CELL_SIZE)
                    j_center = round(world_y / CELL_SIZE)
                    paint_area(floor_tiles, i_center, j_center, brush_size, floor_color, eraser_mode)
                if can_move_player and pygame.mouse.get_pressed()[0]:
                    world_x = mouse_x + camera_offset[0]
                    world_y = mouse_y + camera_offset[1]
                    player.rect.center = round_to_grid(world_x, world_y)

        if not is_paused and not game_over and not in_cutscene:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_s]:
                dy = 1
            if keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_d]:
                dx = 1
            player.move(dx, dy)
            player.update()

            for bot in bots:
                bot.update(player)
                for bullet in bot.bullets[:]:
                    if bullet.rect.colliderect(player.collision_rect):
                        current_health -= 1
                        bot.bullets.remove(bullet)

            if current_health <= 0 and not game_over:
                game_over = True
                restart_timer = pygame.time.get_ticks()
            if any(bot.rect.colliderect(player.collision_rect) for bot in bots) and not delay_message:
                delay_message = True
                game_over = True
                restart_timer = pygame.time.get_ticks()

        if game_over and pygame.time.get_ticks() - restart_timer >= 3000:
            player = Turtle()
            player.rect.topleft = initial_player_position
            player.reset_target()
            for bot in bots:
                bot.rect.topleft = bot.initial_position
                bot.health = bot.max_health
                bot.bullets = []
                bot.state = 'patrol'
            current_health = max_health
            game_over = False
            delay_message = False

        for bullet in bullets[:]:
            if bullet.update():
                bullets.remove(bullet)
            else:
                for bot in bots[:]:
                    if bullet.rect.colliderect(bot.rect):
                        bot.health -= 1
                        bullets.remove(bullet)
                        if bot.health <= 0:
                            bots.remove(bot)
                        break

        current_time = pygame.time.get_ticks()
        if in_cutscene and current_time >= cutscene_start_time:
            if black_bar_height < black_bar_max_height:
                black_bar_height += black_bar_growth_rate
                if black_bar_height > black_bar_max_height:
                    black_bar_height = black_bar_max_height
            else:
                if cutscene_index < len(cutscene_actions):
                    if current_dialog is None:
                        action = cutscene_actions[cutscene_index]
                        if action['type'] == 'say_player':
                            dialog_queue.put(DialogMessage(action['data']['message'], 'player', player.rect.topleft))
                        elif action['type'] == 'say_walkie_talkie':
                            dialog_queue.put(DialogMessage(action['data']['message'], 'walkie_talkie'))
                        elif action['type'] == 'say_character':
                            if characters:
                                char_position = characters[0]['position']
                                dialog_queue.put(DialogMessage(action['data']['message'], 'character', char_position))
                        cutscene_index += 1
                elif cutscene_index >= len(cutscene_actions) and current_dialog is None:
                    in_cutscene = False

        if current_dialog is None and not dialog_queue.empty():
            current_dialog = dialog_queue.get()

        screen.fill(BACKGROUND_COLOR)
        draw_grid(camera_offset)
        player.draw(screen, camera_offset)
        for bot in bots:
            bot.draw(screen, camera_offset)
        for bullet in bullets:
            bullet_screen_x = bullet.rect.x - camera_offset[0]
            bullet_screen_y = bullet.rect.y - camera_offset[1]
            if 0 <= bullet_screen_x < WIDTH and 0 <= bullet_screen_y < HEIGHT:
                pygame.draw.rect(screen, (255, 0, 0), (bullet_screen_x, bullet_screen_y, 5, 5))

        if in_cutscene:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, black_bar_height))
            pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - black_bar_height, WIDTH, black_bar_height))

        if current_dialog:
            if current_dialog.update():
                current_dialog = None
            else:
                if current_dialog.type == 'walkie_talkie':
                    lines = wrap_text(current_dialog.displayed_text, font, dialog_box_width - 20)
                    num_lines = len(lines)
                    line_height = font.get_height()
                    dialog_box_height = (num_lines * line_height) + 20
                    dialog_box_rect = pygame.Rect(
                        walkie_talkie_x + 144 - dialog_box_width - dialog_box_right_padding,
                        dialog_box_y,
                        dialog_box_width,
                        dialog_box_height
                    )
                    pygame.draw.rect(screen, (200, 200, 200), dialog_box_rect)
                    y_offset = dialog_box_rect.y + 10
                    for line in lines:
                        text_surface = font.render(line, True, (0, 0, 0))
                        screen.blit(text_surface, (dialog_box_rect.x + 10, y_offset))
                        y_offset += line_height
                elif current_dialog.type in ['player', 'character']:
                    if current_dialog.position:
                        lines = wrap_text(current_dialog.displayed_text, font, 280 - 20)
                        num_lines = len(lines)
                        line_height = font.get_height()
                        dialog_box_height = (num_lines * line_height) + 20
                        screen_x = current_dialog.position[0] - camera_offset[0]
                        screen_y = current_dialog.position[1] - camera_offset[1] - dialog_box_height - 10
                        if screen_y < black_bar_height:
                            screen_y = black_bar_height + 10
                        elif screen_y + dialog_box_height > HEIGHT - black_bar_height:
                            screen_y = HEIGHT - black_bar_height - dialog_box_height - 10
                        draw_dialog_box(screen, current_dialog.displayed_text, (screen_x, screen_y), (0, 0))

        if not in_cutscene:
            draw_health_bar(screen, current_health, max_health)
            triangle_points = [
                (player.rect.centerx - camera_offset[0], player.rect.top - 10 - camera_offset[1]),
                (player.rect.centerx - 5 - camera_offset[0], player.rect.top - 20 - camera_offset[1]),
                (player.rect.centerx + 5 - camera_offset[0], player.rect.top - 20 - camera_offset[1])
            ]
            pygame.draw.polygon(screen, (0, 255, 0), triangle_points)
            ammo_text = font.render(f"Ammo: {player.ammo}", True, (0, 0, 0))
            text_width, text_height = font.size(f"Ammo: {player.ammo}")
            text_x = WIDTH - panel_width - text_width - 10
            text_y = HEIGHT - 30
            screen.blit(ammo_text, (text_x, text_y))
            pistol_x = WIDTH - panel_width - 154
            pistol_y = HEIGHT - 174
            if pistol_image:
                screen.blit(pistol_image, (pistol_x, pistol_y))

        if walkie_talkie_image:
            screen.blit(walkie_talkie_image, (walkie_talkie_x, walkie_talkie_y))

        if game_over:
            if current_health <= 0:
                display_message(screen, "Игрок мертв")
            elif delay_message:
                display_message(screen, "Игрок задержан")

        for message in pickup_messages[:]:
            if message.is_expired():
                pickup_messages.remove(message)
            else:
                text_surface = font.render(message.text, True, (0, 255, 0))
                screen_x = message.position[0] - camera_offset[0]
                screen_y = message.position[1] - camera_offset[1]
                screen.blit(text_surface, (screen_x, screen_y))

        panel_rect = pygame.Rect(WIDTH - panel_width, 0, panel_width, HEIGHT)
        pygame.draw.rect(screen, (200, 200, 200), panel_rect)
        y_offset = 10
        for option in settings_buttons:
            if isinstance(option, str):
                header_text = font.render(option, True, (0, 0, 0))
                screen.blit(header_text, (panel_rect.x + 10, y_offset))
                y_offset += 20
            else:
                button_rect = pygame.Rect(panel_rect.x + 10, y_offset, panel_width - 20, 30)
                color = (150, 150, 150) if button_rect.collidepoint(pygame.mouse.get_pos()) else (100, 100, 100)
                pygame.draw.rect(screen, color, button_rect)
                if callable(option['label']):
                    label_text = option['label']()
                else:
                    label_text = option['label']

                button_font_size = 36
                if button_font_size not in font_cache:
                    font_cache[button_font_size] = pygame.font.Font(None, button_font_size)
                button_font = font_cache[button_font_size]
                text_surface = button_font.render(label_text, True, (0, 0, 0))

                while text_surface.get_width() > button_rect.width - 10 and button_font_size > 10:
                    button_font_size -= 2
                    if button_font_size not in font_cache:
                        font_cache[button_font_size] = pygame.font.Font(None, button_font_size)
                    button_font = font_cache[button_font_size]
                    text_surface = button_font.render(label_text, True, (0, 0, 0))

                text_rect = text_surface.get_rect(center=button_rect.center)
                screen.blit(text_surface, text_rect)
                y_offset += 40

        pygame.display.flip()
        try:
            root.update()
        except tk.TclError:
            pass
        pygame.time.Clock().tick(60)

def menu_window():
    global play_game, root
    root = tk.Tk()
    root.title("Меню")
    title_label = tk.Label(root, text="Turtle-Target", font=("Arial", 24))
    title_label.pack(pady=20)
    subtitle_label = tk.Label(root, text="Made by Jigulenok", font=("Arial", 12))
    subtitle_label.pack()

    def set_play_game():
        global play_game
        play_game = True
        root.destroy()

    tk.Button(root, text="Продолжить", command=set_play_game).pack(pady=20)
    tk.Button(root, text="Выйти на рабочий стол", command=sys.exit).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    while True:
        play_game = False
        menu_window()
        if play_game:
            main()
            if return_to_menu:
                continue
            else:
                break
        else:
            break