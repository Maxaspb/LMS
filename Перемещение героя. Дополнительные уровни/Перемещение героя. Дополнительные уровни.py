import pygame
import os

obstacle_sprites = pygame.sprite.Group()
environment_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
menu_background = pygame.sprite.Group()

def load_assets():
    print('Выберите файл уровня из доступных: level1.txt, level2.txt, level3.txt')
    return input().strip()

def load_texture(filename):
    return pygame.image.load(os.path.join(filename))

def load_game_level(filename):
    try:
        with open(filename) as file:
            level_data = [line.strip() for line in file]
        
        if not level_data:
            raise ValueError("Файл уровня пуст")
            
        column_count = max(len(row) for row in level_data)
        processed_level = [row.ljust(column_count, '.') for row in level_data]
        
        return (
            processed_level,
            column_count * 50,
            len(processed_level) * 50
        )
    except Exception as e:
        print(f"Ошибка загрузки уровня: {e}")
        return None, None, None

class MainMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(menu_background)
        self.image = pygame.transform.scale(
            load_texture('fon.jpg'), (800, 450))
        self.rect = self.image.get_rect(topleft=(0, 0))

class Wall(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__(obstacle_sprites)
        self.image = load_texture('box.png')
        self.rect = self.image.get_rect(
            topleft=(grid_x * 50, grid_y * 50))

class Floor(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__(environment_sprites)
        self.image = load_texture('grass.png')
        self.rect = self.image.get_rect(
            topleft=(grid_x * 50, grid_y * 50))

class Hero(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__(player_sprite)
        self.image = load_texture('mar.png')
        self.rect = self.image.get_rect(
            topleft=(grid_x * 50 + 15, grid_y * 50 + 5))
        self.play_area = (0, 0)

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return
        movement = {
            pygame.K_LEFT: (-50, 0),
            pygame.K_RIGHT: (50, 0),
            pygame.K_UP: (0, -50),
            pygame.K_DOWN: (0, 50)
        }.get(event.key)
        if not movement:
            return
        dx, dy = movement
        new_position = self.rect.move(dx, dy)
        if (0 <= new_position.x <= self.play_area[0] - 50 and 
            0 <= new_position.y <= self.play_area[1] - 50):
            self.rect = new_position
            if pygame.sprite.spritecollideany(self, obstacle_sprites):
                self.rect.move_ip(-dx, -dy)

def create_world(level_data):
    character = None
    for y, row in enumerate(level_data):
        for x, cell in enumerate(row):
            if cell == '#':
                Wall(x, y)
            elif cell == '.':
                Floor(x, y)
            elif cell == '@':
                Floor(x, y)
                character = Hero(x, y)
    return character

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((800, 450))
    pygame.display.set_caption('Перемещение героя - Расширенная версия')
    level_file = load_assets()
    level_map, map_width, map_height = load_game_level(level_file)
    if not level_map:
        pygame.quit()
        exit()
    MainMenu()
    protagonist = create_world(level_map)
    protagonist.play_area = (map_width, map_height)
    in_menu = True
    while in_menu:
        menu_background.draw(display)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                display = pygame.display.set_mode(
                    (int(map_width), int(map_height)))
                in_menu = False
    game_active = True
    while game_active:
        environment_sprites.draw(display)
        obstacle_sprites.draw(display)
        player_sprite.draw(display)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            protagonist.handle_input(event)

    pygame.quit()
