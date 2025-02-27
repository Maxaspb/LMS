import pygame
import os

tiles_group1 = pygame.sprite.Group()
tiles_group2 = pygame.sprite.Group()
player_group = pygame.sprite.Group()
screensaver_spr = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return level, len(level[0]) * 41.8, len(level) * 50


class Screensaver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(screensaver_spr)
        self.image = pygame.transform.scale(load_image('fon.jpg'), (800, 450))
        self.rect = self.image.get_rect().move(0, 0)


class Tile1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group1)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)


class Tile2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group2)
        self.image = load_image('grass.png')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = load_image('mar.png')
        self.rect = self.image.get_rect().move(50 * pos_x + 15, 50 * pos_y + 5)

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.rect.x - 50 >= 0:
                    self.rect = self.rect.move(-50, 0)
                if pygame.sprite.spritecollide(self, tiles_group1, False):
                    self.rect = self.rect.move(50, 0)
            if event.key == pygame.K_RIGHT:
                if self.rect.x + 50 <= width:
                    self.rect = self.rect.move(50, 0)
                if pygame.sprite.spritecollide(self, tiles_group1, False):
                    self.rect = self.rect.move(-50, 0)
            if event.key == pygame.K_UP:
                if self.rect.y - 50 >= 0:
                    self.rect = self.rect.move(0, -50)
                if pygame.sprite.spritecollide(self, tiles_group1, False):
                    self.rect = self.rect.move(0, 50)
            if event.key == pygame.K_DOWN:
                if self.rect.y + 50 <= height:
                    self.rect = self.rect.move(0, 50)
                if pygame.sprite.spritecollide(self, tiles_group1, False):
                    self.rect = self.rect.move(0, -50)
                    

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile2(x, y)
            elif level[y][x] == '#':
                Tile1(x, y)
            elif level[y][x] == '@':
                Tile2(x, y)
                new_player = Player(x, y)            
    return new_player, x, y


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 450))
    pygame.display.set_caption('Перемещение героя')
    Screensaver()
    level, width, height = load_level('level1.txt')
    player, level_x, level_y = generate_level(level)
    screensaver = True
    running = True
    while screensaver:
        screensaver_spr.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screensaver = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen = pygame.display.set_mode((width, height))
                screensaver = False
    while running:
        tiles_group1.draw(screen)
        tiles_group2.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            player_group.update(event)
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
