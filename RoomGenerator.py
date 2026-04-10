import pygame
from sys import exit
import random
import yaml

colors = {
    "BG" : "#19c0e6"
}

pygame.init()

main_screen = pygame.display.set_mode([1280,720])
render_surf = pygame.Surface([320,180])

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,image,size):
        super().__init__()
        self.pos = [p*size for p in pos]
        self.image = image
        self.rect = pygame.Rect((self.pos),(size,size))
        tilegroup.add(self)

tilegroup = pygame.sprite.Group()
class Room():
    def __init__(self,image_path,sockets_path,tilesize,room_size):
        self.corners = {}
        self.grid = {}
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_set = []
        self.sockets = {}
        self.classes = []

        self.size = room_size
        self.tilesize = tilesize

        with open(sockets_path,"r") as file:
            s = yaml.safe_load(file)
            self.classes = s["Classes"]
            self.sockets = {k : v for k,v in s.items() if type(k) is not str}

        for y in range(0,self.image.height - self.tilesize + 1,self.tilesize):
            for x in range(0,self.image.width - self.tilesize + 1,self.tilesize):
                self.image_set.append(self.image.subsurface((x,y),(self.tilesize,self.tilesize)))
        
        self.generate_grid()
        for cell in self.grid:
            self.collapse_cell(cell)

    def generate_grid(self):
        for y in range(self.size[1]+1):
            for x in range(self.size[0]+1):
                self.corners[(x,y)] = self.classes.copy()
        
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.grid[(x,y)] = {
                    "collapsed" : False,
                    "tile" : None 
                }

    def collapse_cell(self,pos:tuple):
        if self.grid[pos]["collapsed"]:
            return

        x,y = pos
        corner_cords = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]

        for cord in corner_cords:
            corner:list = self.corners[cord]
            while len(corner) > 1:
                corner.pop(random.randint(0,len(corner)-1))
            
            self.corners[cord] = corner
        
        corners = [self.corners[cord][0] for cord in corner_cords]
        candidates = []
        for _id,socket in self.sockets.items():
            if corners == socket:
                candidates.append(_id)
        
        if not candidates:
            candidates = [12]
        self.grid[pos]["tile"] = Tile(pos,self.image_set[random.choice(candidates)],32)
        self.grid[pos]["collapsed"] = True


if __name__ == "__main__":

    def Exit_Game():
        pygame.quit()
        exit()
    
    room1 = Room("grass-tiles.png","sockets.yaml",32,(10,6))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit_Game()
        
        render_surf.fill(colors["BG"])
        tilegroup.draw(render_surf)

        for x in range(0,render_surf.width,32):
            pygame.draw.line(render_surf,(0,0,0),(x,0),(x,400),1)
        for y in range(0,render_surf.height,32):
            pygame.draw.line(render_surf,(0,0,0),(0,y),(400,y),1)
        
        main_screen.blit(pygame.transform.scale_by(render_surf,main_screen.height/render_surf.height),(0,0))
        pygame.display.update()