import random

size = 3,3
grid = {}
classes = [None,"G"]

for y in range(size[1]):
    for x in range(size[0]):
        grid[(x,y)] = classes.copy()

for y in range(3):
    for x in range(3):
        while len(grid[(x,y)]) > 1:
            grid[(x,y)].pop(random.randint(0,len(grid[(x,y)])-1))

print(grid)