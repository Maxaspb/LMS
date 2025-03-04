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
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return level, len(level[0]) * 50, len(level) * 50


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

    def update(self, event, typ):
        global x_flag, y_flag
        if typ is True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    y_flag += 1
                    self.rect = self.rect.move(50, 0)
                if event.key == pygame.K_RIGHT:
                    self.rect = self.rect.move(-50, 0)
                if event.key == pygame.K_UP:
                    x_flag += 1
                    self.rect = self.rect.move(0, 50)
                if event.key == pygame.K_DOWN:
                    self.rect = self.rect.move(0, -50)
        elif typ is False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    y_flag -= 1
                    self.rect = self.rect.move(-50, 0)
                if event.key == pygame.K_RIGHT:
                    self.rect = self.rect.move(50, 0)
                if event.key == pygame.K_UP:
                    x_flag -= 1
                    self.rect = self.rect.move(0, -50)
                if event.key == pygame.K_DOWN:
                    self.rect = self.rect.move(0, 50)
        else:
            if event.type == pygame.KEYDOWN:
                if self.rect.x < 0 and not y_empty or self.rect.x < 1 and y_empty:
                    Tile1(width / 50 - 1, self.rect.y / 50)
                    self.kill()
                if self.rect.x > width - 50:
                    if y_empty:
                        Tile1(1, self.rect.y / 50)
                    else:
                        Tile1(0, self.rect.y / 50)
                    self.kill()
                if self.rect.y < 0 and not x_empty or self.rect.y < 1 and x_empty:
                    Tile1(self.rect.x / 50, height / 50 - 1)
                    self.kill()
                if self.rect.y > height - 50:
                    if x_empty:
                        Tile1(self.rect.x / 50, 1)
                    else:
                        Tile1(self.rect.x / 50, 0)
                    self.kill()


class Tile2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group2)
        self.image = load_image('grass.png')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)

    def update(self, event, typ):
        if typ is True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.rect = self.rect.move(50, 0)
                if event.key == pygame.K_RIGHT:
                    self.rect = self.rect.move(-50, 0)
                if event.key == pygame.K_UP:
                    self.rect = self.rect.move(0, 50)
                if event.key == pygame.K_DOWN:
                    self.rect = self.rect.move(0, -50)
        elif typ is False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.rect = self.rect.move(-50, 0)
                if event.key == pygame.K_RIGHT:
                    self.rect = self.rect.move(50, 0)
                if event.key == pygame.K_UP:
                    self.rect = self.rect.move(0, -50)
                if event.key == pygame.K_DOWN:
                    self.rect = self.rect.move(0, 50)
        else:
            if event.type == pygame.KEYDOWN:
                if self.rect.x < 0 and not y_empty or self.rect.x < 1 and y_empty:
                    Tile2(width / 50 - 1, self.rect.y / 50)
                    self.kill()
                if self.rect.x > width - 50:
                    if y_empty:
                        Tile2(1, self.rect.y / 50)
                    else:
                        Tile2(0, self.rect.y / 50)
                    self.kill()
                if self.rect.y < 0 and not x_empty or self.rect.y < 1 and x_empty:
                    Tile2(self.rect.x / 50, height / 50 - 1)
                    self.kill()
                if self.rect.y > height - 50:
                    if x_empty:
                        Tile2(self.rect.x / 50, 1)
                    else:
                        Tile2(self.rect.x / 50, 0)
                    self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = load_image('mar.png')
        self.rect = self.image.get_rect().move(50 * pos_x + 15, 50 * pos_y + 5)
        

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
    pygame.display.set_caption('Перемещение героя. Новый уровень')
    Screensaver()
    level, width, height = load_level('level1.txt')
    player, level_x, level_y = generate_level(level)
    x_flag = 0
    y_flag = 0
    x_empty = False
    y_empty = False
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
                screen = pygame.display.set_mode((width + 50, height + 50))
                screensaver = False
    while running:
        screen.fill((0, 0, 0))
        tiles_group1.draw(screen)
        tiles_group2.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        pygame.time.delay(500)
        for event in pygame.event.get():
            tiles_group1.update(event, True)
            tiles_group2.update(event, True)
            if pygame.sprite.spritecollide(player, tiles_group1, False) or \
               not pygame.sprite.spritecollide(player, tiles_group2, False):
                tiles_group1.update(event, False)
                tiles_group2.update(event, False)
            tiles_group1.update(event, None)
            tiles_group2.update(event, None)
            if x_flag:
                x_empty = True
                for sprite in tiles_group1:
                    if sprite.rect.y == 0:
                        sprite.kill()
                for sprite in tiles_group2:
                    if sprite.rect.y == 0:
                        sprite.kill()
            if y_flag:
                y_empty = True
                for sprite in tiles_group1:
                    if sprite.rect.x == 0:
                        sprite.kill()
                for sprite in tiles_group2:
                    if sprite.rect.x == 0:
                        sprite.kill()
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
