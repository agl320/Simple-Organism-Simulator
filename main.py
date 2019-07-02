import time
import math
import pygame
import random
from food import Food
from cell import Cell


def drawCell(cellName):
    pygame.draw.circle(screen, BLUE, cellName.Pos(), cellName.radius)

def drawFood(foodList):
    if(len(foodList) > 0):
        for i in range(len(foodList)):
            pygame.draw.circle(screen, BLACK, foodList[i].Pos(), 5)

def addFood(foodList, x, y):
    foodList.append(Food(x,y))
    return foodList

def cellAction(cell, foodList):


    if(len(foodList) > 0):
        foodList = updateFood(cell, foodList)
    else:
        cell.Roam()

    drawCell(cell)

    return foodList

def updateFood(cellName, foodList):
    distanceList = []
    x_1, y_1 = cellName.Pos()


    for i in range(len(foodList)):
        x_2, y_2 = foodList[i].Pos()
        distanceList.append(math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2))

    minPos = distanceList.index(min(distanceList))

    closestFood = foodList[minPos]

    x_2, y_2 = closestFood.Pos()

    if(x_1 == x_2 and y_1 == y_2):

        foodList.pop(minPos)
        cellName.hunger = 100

    else:

        cellName.MoveToFood(x_2, y_2)

        x_1, y_1 = cellName.Pos()

        if (x_1 == x_2 and y_1 == y_2):
            foodList.pop(minPos)
            cellName.hunger = 100

    return foodList



# foodList stores all instances of food; can remove and add
# distanceList stores the distances between named cell and all foods, gets closest
foodList = []
cellList = []
directionList = ['N', 'S', 'E', 'W']
simNum = 0
sideBarWidth = 200

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LGREY = (215, 219, 224)

# initializing the pygame window
pygame.init()
pygame.font.init()
width, height = 1200, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cell Simulator')
screen.fill(WHITE)
# updating window
pygame.display.flip()

# initializing cells

for i in range(3):
    cellList.append(Cell(random.randrange(10, width - 10 - sideBarWidth, 10), random.randrange(10, height - 10, 10), random.choice(directionList), 5, 10, width - 10 - sideBarWidth, height - 10))

# showing simulation information

font = pygame.font.SysFont('Times New Roman', 20)


# looping window

run = True

while run:

    screen.fill(WHITE)

    # displaying simulation info
    pygame.draw.rect(screen, LGREY, [1000, 0, sideBarWidth, 750])

    simText = font.render(f'Simulation: {simNum}', True, BLACK)
    screen.blit(simText, (width - round(sideBarWidth / 2) - 50, 400))

    aliveText = font.render(f'Alive: {len(cellList)}', True, BLACK)
    screen.blit(aliveText, (width - round(sideBarWidth/2)-50,450))

    space = 0

    for i in range(len(cellList)):
        hungerText = font.render(f'Hunger: {cellList[i].hunger}', True, BLACK)
        screen.blit(hungerText, (width - round(sideBarWidth / 2) - 50, 500 + space))
        space += 50

    newCellList = []
    for i in range(len(cellList)):
        if (cellList[i].hunger > 0):
            newCellList.append(cellList[i])

    cellList = newCellList

    # frame every 0.2 seconds
    time.sleep(0.2)


    # randomly generating food

    if(len(foodList) == 0):
        for i in range(random.randint(9,14)):
            foodList = addFood(foodList, random.randrange(10, width - 10 - sideBarWidth, 10), random.randrange(10, height - 10 - sideBarWidth, 10))
        simNum += 1

    # draw
    for i in range(len(cellList)):
        foodList = cellAction(cellList[i], foodList)

    drawFood(foodList)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()



pygame.quit()
