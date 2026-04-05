import pygame
import sys
import yaml
import json


pygame.init()

screen = pygame.display.set_mode((400,400))

tilemap = pygame.image.load("tileset.png").convert()

class TileMapper():
    def __init__(self,tilesize = 16):
        self.tileset = []

        for y in range(0,tilemap.height,tilesize):
            for x in range(0,tilemap.width,tilesize):
                tile = tilemap.subsurface((x,y),(tilesize,tilesize))
                self.tileset.append(tile)

if __name__ == "__main__":

    tilegroup = {}

    with open("tilegroup.yaml","r") as file:
        tilegroup = yaml.safe_load(file)
        print(yaml.safe_dump(tilegroup))

    tilemapper = TileMapper(16)
    surf = pygame.Surface(tilemap.size)
    
    y = -1
    for tile in range(len(tilemapper.tileset)):
        if tile % 8 == 0:
            y += 1
        surf.blit(tilemapper.tileset[tile],((tile%8)*16,y*16))

    screen.blit(surf,(0,0))

    a = 300
    clock = pygame.Clock()

    while True:
        clock.tick(60)
        a -= 1
        if a <= 0:
            pygame.quit()
            sys.exit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()