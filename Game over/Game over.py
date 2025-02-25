import pygame
import os
 
 
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image

 
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 300))
    pygame.display.set_caption('Game over')
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    game_over = pygame.sprite.Sprite()
    game_over.image = load_image('gameover.png')
    game_over.rect = game_over.image.get_rect()
    game_over.rect.x = -600
    game_over.rect.y = 0
    all_sprites.add(game_over)
    running = True
    while running:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game_over.rect.x + 1 <= 0:
            game_over.rect.x += 200 / 50
        screen.fill((0, 0, 255))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
