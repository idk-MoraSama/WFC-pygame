import pygame
from sys import exit
from copy import deepcopy
import random
import yaml

colors = {
    "BG" : "#19c0e6"
}

pygame.init()

main_screen = pygame.display.set_mode([800,800])
render_surf = pygame.Surface([400,400])

class Room():
    def __init__(self,image_path,sockets_path,tilesize,room_size):
        self.corners = {}
        self.grid = {}
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_set = []
        self.sockets = {}
        self.classes = []
        self.tiles = {}

        self.size = room_size
        self.tilesize = tilesize

        with open("sockets.yaml","r") as file:
            s = yaml.safe_load(file)
            self.classes = s["Classes"]
            self.sockets = {k : v for k,v in s.items() if type(k) is not str}

        for y in range(0,self.image.height,self.tilesize):
            for x in random(0,self.image.width,self.tilesize):
                self.imageset.append(self.image.subsurface((x,y),(x+self.tilesize,y+self.tilesize)))

    def generate_grid(self):
        for y in range(self.size[1]+1):
            for x in range(self.size[0]+1):
                self.corners[(x,y)] = self.classes.copy()
        
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.grid[(x,y)] = {
                    "corners" : [self.corners[(x,y)],self.corners[(x+1,y)],self.corners[(x,y+1)],self.corners[(x+1,y+1)]],
                    "collapsed" : False,
                    "image" : None 
                }
    
    def collapse_cell(self,cell):
        cell = self.grid[cell]

        if cell["collapsed"]:
            return

        for corner in cell["corners"]:
            while len(corner) > 1:
                corner.pop(random.randint(0,len(corner)-1))
                 


if __name__ == "__main__":

    def Exit_Game():
        pygame.quit()
        exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit_Game()
        
        render_surf.fill(colors["BG"])
        
        main_screen.blit(pygame.transform.scale_by(render_surf,main_screen.height/render_surf.height),(0,0))
        pygame.display.update()