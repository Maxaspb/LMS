import pygame
import os


environment_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
background_sprite = pygame.sprite.Group()

def load_image(filename):
    return pygame.image.load(os.path.join(filename))

def load_level_map(filename):
    with open(filename) as f:
        return [line.strip() for line in f]

def process_level_data(raw_level):
    max_width = max(len(row) for row in raw_level)
    return [
        row.ljust(max_width, '.') 
        for row in raw_level
    ], max_width * 41.8, len(raw_level) * 50

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(background_sprite)
        self.image = pygame.transform.scale(
            load_image('fon.jpg'), (800, 450))
        self.rect = self.image.get_rect()

class EnvironmentTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(environment_sprites)
        self.image = load_image('grass.png')
        self.rect = self.image.get_rect(
            topleft=(x * 50, y * 50))

class ObstacleTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(obstacle_sprites)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect(
            topleft=(x * 50, y * 50))

class GameCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_sprite)
        self.image = load_image('mar.png')
        self.rect = self.image.get_rect(
            topleft=(x * 50 + 15, y * 50 + 5))

    def handle_movement(self, event):
        if event.type != pygame.KEYDOWN:
            return

        move_vectors = {
            pygame.K_LEFT: (-50, 0),
            pygame.K_RIGHT: (50, 0),
            pygame.K_UP: (0, -50),
            pygame.K_DOWN: (0, 50)
        }

        if event.key in move_vectors:
            dx, dy = move_vectors[event.key]
            new_pos = self.rect.move(dx, dy)
            
            if self.is_valid_move(new_pos):
                self.rect = new_pos
                self.resolve_collision(dx, dy)

    def is_valid_move(self, new_rect):
        return (
            0 <= new_rect.x <= self.screen_width and
            0 <= new_rect.y <= self.screen_height
        )

    def resolve_collision(self, dx, dy):
        if pygame.sprite.spritecollideany(self, obstacle_sprites):
            self.rect.move_ip(-dx, -dy)

def initialize_level(level_data):
    player = None
    for row_idx, row in enumerate(level_data):
        for col_idx, cell in enumerate(row):
            if cell == '@':
                EnvironmentTile(col_idx, row_idx)
                player = GameCharacter(col_idx, row_idx)
            elif cell == '#':
                ObstacleTile(col_idx, row_idx)
            elif cell == '.':
                EnvironmentTile(col_idx, row_idx)
    return player

if __name__ == "__main__":
    pygame.init()
    display_surface = pygame.display.set_mode((800, 450))
    pygame.display.set_caption('Перемещение героя')
    raw_level = load_level_map('level1.txt')
    processed_level, level_width, level_height = process_level_data(raw_level)
    Background()
    character = initialize_level(processed_level)
    character.screen_width = level_width
    character.screen_height = level_height
    in_menu = True
    game_active = True
    while in_menu:
        background_sprite.draw(display_surface)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                display_surface = pygame.display.set_mode(
                    (int(level_width), int(level_height)))
                in_menu = False
    while game_active:
        environment_sprites.draw(display_surface)
        obstacle_sprites.draw(display_surface)
        player_sprite.draw(display_surface)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            character.handle_movement(event)
    pygame.quit()
