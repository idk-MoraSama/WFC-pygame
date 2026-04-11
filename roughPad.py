# import pygame
# import sys

# pygame.init()

# screen = pygame.display.set_mode((400,400))

# img = pygame.image.load("grass-tiles.png").convert_alpha()
# a = 300

# clock = pygame.time.Clock()

# while True:
#     delta = clock.tick(60)
#     a -= 1

#     if a <= 0:
#         pygame.quit()
#         sys.exit()

#     for y in range(0,img.height - 31,32):
#         for x in range(0,img.width- 31,32):
#             screen.blit(img.subsurface((x,y),(32,32)),(x*1.2,y*1.2))
    
#     pygame.display.update()

print(len([None,1,None]))