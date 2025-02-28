import pygame
import os


wall_tiles = pygame.sprite.Group() 
floor_tiles = pygame.sprite.Group()
player_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()

def load_texture(filename):
    try:
        return pygame.image.load(os.path.join(filename))
    except Exception as e:
        print(f"Ошибка загрузки текстуры {filename}: {e}")
        raise

def load_game_map(map_file):
    with open(map_file, 'r') as f:
        map_data = [line.strip() for line in f]
    
    max_row_length = max(len(row) for row in map_data)
    padded_map = [row.ljust(max_row_length, '.') for row in map_data]
    
    return (
        padded_map,
        len(padded_map[0]) * 50,
        len(padded_map) * 50
    )

class MenuScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(menu_group)
        self.image = pygame.transform.scale(
            load_texture('fon.jpg'), 
            (800, 450)
        )
        self.rect = self.image.get_rect(topleft=(0, 0))

class Wall(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__(wall_tiles)
        self.image = load_texture('box.png')
        self.rect = self.image.get_rect(
            topleft=(grid_x * 50, grid_y * 50)
        )
    
    def shift_position(self, dx, dy):
        self.rect.move_ip(dx, dy)

class Floor(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__(floor_tiles)
        self.image = load_texture('grass.png')
        self.rect = self.image.get_rect(
            topleft=(grid_x * 50, grid_y * 50)
        )
    
    def shift_position(self, dx, dy):
        self.rect.move_ip(dx, dy)

class GameHero(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__(player_group)
        self.image = load_texture('mar.png')
        self.rect = self.image.get_rect(
            topleft=(grid_x * 50 + 15, grid_y * 50 + 5)
        )

def create_world(map_data):
    hero = None
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == '#': 
                Wall(x, y)
            elif cell == '.':
                Floor(x, y)
            elif cell == '@':
                Floor(x, y)
                hero = GameHero(x, y)
    return hero

def handle_movement(event, reverse=False):
    direction_map = {
        pygame.K_LEFT: (50, 0) if not reverse else (-50, 0),
        pygame.K_RIGHT: (-50, 0) if not reverse else (50, 0),
        pygame.K_UP: (0, 50) if not reverse else (0, -50),
        pygame.K_DOWN: (0, -50) if not reverse else (0, 50)
    }
    
    if event.key in direction_map:
        dx, dy = direction_map[event.key]
        for tile in (*wall_tiles, *floor_tiles):
            tile.shift_position(dx, dy)

def main():
    pygame.init()
    menu_screen = pygame.display.set_mode((800, 450))
    pygame.display.set_caption('Перемещение героя. Камера')
    MenuScreen()
    level_map, level_w, level_h = load_game_map('level1.txt')
    hero = create_world(level_map)
    show_menu = True
    game_active = True
    while game_active:
        while show_menu:
            menu_group.draw(menu_screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show_menu = False
                    game_active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_screen = pygame.display.set_mode((level_w, level_h))
                    show_menu = False
        menu_screen.fill((0, 0, 0))
        wall_tiles.draw(menu_screen)
        floor_tiles.draw(menu_screen)
        player_group.draw(menu_screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYDOWN:
                handle_movement(event)
                collision = pygame.sprite.spritecollideany(hero, wall_tiles)
                out_of_bounds = not pygame.sprite.spritecollideany(hero, floor_tiles)
                if collision or out_of_bounds:
                    handle_movement(event, reverse=True)
    pygame.quit()

if __name__ == "__main__":
    main()
