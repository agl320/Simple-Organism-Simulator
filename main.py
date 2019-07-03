import time
import math
import pygame
import random
from food import Food
from cell import Cell
import numpy as np
import matplotlib.pyplot as plt

def checkIfAllInRest(cellList):
    for i in range(len(cellList)):
        if(cellList[i].state == 'active'):
            return False
    return True

def drawCell(cellName, state):
    if(state == 'active'):
        pygame.draw.circle(screen, GREEN, cellName.Pos(), cellName.radius)
    elif(state == 'rest'):
        pygame.draw.circle(screen, BLUE, cellName.Pos(), cellName.radius)
    elif(state == 'reproduce'):
        pygame.draw.circle(screen, PINK, cellName.Pos(), cellName.radius)

def drawFood(foodList):
    if(len(foodList) > 0):
        for i in range(len(foodList)):
            pygame.draw.circle(screen, BLACK, foodList[i].Pos(), 5)

def addFood(foodList, x, y):
    foodList.append(Food(x,y))
    return foodList

def reproduce(cellName, cellList):
    x, y = cellName.Pos()
    y += 10
    pygame.draw.circle(screen, GREEN, (x, y), cellName.radius)
    cellList.append(Cell(x, y,
                         random.choice(directionList), 5, 10, width - 10 - sideBarWidth, height - 10))

    return cellList

def cellAction(cell, foodList, cellList):
    choice = random.randint(0,2)
    if(cell.state == 'active'):

        if (cell.foodCounter == 0):

            foodList = updateFood(cell, foodList)
            cell.state = 'active'

        elif(cell.foodCounter == 1):

            if(choice == 0):
                cell.state = 'rest'
            else:
                cell.state = 'reproduce'

    elif(cell.state == 'reproduce'):
        if(cell.foodCounter > 1):
            cell.state = 'rest'
            cellList = reproduce(cell, cellList)
        else:
            foodList = updateFood(cell, foodList)
            cell.state = 'reproduce'

    drawCell(cell, cell.state)

    return foodList, cellList

def updateFood(cellName, foodList):
    distanceList = []
    x_1, y_1 = cellName.Pos()

    if(len(foodList) > 0):

        for i in range(len(foodList)):
            x_2, y_2 = foodList[i].Pos()
            distanceList.append(math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2))

        minPos = distanceList.index(min(distanceList))

        closestFood = foodList[minPos]

        x_2, y_2 = closestFood.Pos()

        if(x_1 == x_2 and y_1 == y_2):

            foodList.pop(minPos)
            cellName.hunger = 100
            cellName.foodCounter += 1

        else:

            cellName.MoveToFood(x_2, y_2)

            x_1, y_1 = cellName.Pos()

            if (x_1 == x_2 and y_1 == y_2):
                foodList.pop(minPos)
                cellName.hunger = 100
                cellName.foodCounter += 1
    else:
        cellName.Roam

    return foodList



# foodList stores all instances of food; can remove and add
# distanceList stores the distances between named cell and all foods, gets closest
foodList = []
cellList = []
directionList = ['N', 'S', 'E', 'W']
generation = 0
sideBarWidth = 200
populationList = []
genList = []

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LGREY = (215, 219, 224)
PINK = (245, 66, 224)

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

for i in range(1):
    cellList.append(Cell(random.randrange(10, width - 10 - sideBarWidth, 10), random.randrange(10, height - 10, 10), random.choice(directionList), 5, 10, width - 10 - sideBarWidth, height - 10))

# showing simulation information

font = pygame.font.SysFont('Times New Roman', 15)

# looping window

run = True

while run:

    screen.fill(WHITE)

    # displaying simulation info
    pygame.draw.rect(screen, LGREY, [1000, 0, sideBarWidth, 750])

    simText = font.render(f'Generation: {generation}', True, BLACK)
    screen.blit(simText, (width - round(sideBarWidth / 2) - 50, 100))

    aliveText = font.render(f'Alive: {len(cellList)}', True, BLACK)
    screen.blit(aliveText, (width - round(sideBarWidth/2)-50,150))

    space = 0

    for i in range(len(cellList)):
        hungerText = font.render(f'Hunger: {cellList[i].hunger}', True, BLACK)
        screen.blit(hungerText, (width - round(sideBarWidth / 2) - 50, 200 + space))

        ageText = font.render(f'Age: {cellList[i].age}', True, BLACK)
        screen.blit(ageText, (width - round(sideBarWidth / 2) - 50, 225 + space))

        space += 50

    if (len(foodList) == 0 or checkIfAllInRest(cellList) == True):

        populationCtr = 0

        for i in range(len(cellList)):
            populationCtr += 1
            if (cellList[i].state == 'rest'):
                cellList[i].state = 'active'
                cellList[i].foodCounter = 0
            cellList[i].age += 1

        for i in range(10):
            foodList = addFood(foodList, random.randrange(10, width - 10 - sideBarWidth, 10),
                               random.randrange(10, height - 10 - sideBarWidth, 10))

        populationList.append(populationCtr)
        genList.append(generation)
        generation += 1


    newCellList = []

    for i in range(len(cellList)):
        if (cellList[i].hunger > 0 and cellList[i].age < 3):
            newCellList.append(cellList[i])

    cellList = newCellList



    # frame every 0.2s
    time.sleep(0.2)

    # draw
    for i in range(len(cellList)):
        foodList, cellList = cellAction(cellList[i], foodList, cellList)

    drawFood(foodList)

    if (len(cellList) == 0):
        time.sleep(1)
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()


x = genList
y = populationList

# Create the plot
plt.plot(x, y, 'go--')
# r- is a style code meaning red solid line

# Show the plot
plt.show()
