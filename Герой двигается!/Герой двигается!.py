import pygame
import os
 
 
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image

 
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Герой двигается!')
    all_sprites = pygame.sprite.Group()
    creature = pygame.sprite.Sprite()
    creature.image = load_image('creature.png')
    creature.rect = creature.image.get_rect()
    creature.rect.x = 0
    creature.rect.y = 0
    all_sprites.add(creature)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    creature.rect.x -= 10
                if event.key == pygame.K_UP:
                    creature.rect.y -= 10
                if event.key == pygame.K_RIGHT:
                    creature.rect.x += 10
                if event.key == pygame.K_DOWN:
                    creature.rect.y += 10
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
