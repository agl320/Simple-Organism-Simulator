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

    else:

        cellName.MoveToFood(x_2, y_2)

    return foodList



# foodList stores all instances of food; can remove and add
# distanceList stores the distances between named cell and all foods, gets closest
foodList = []
directionList = ['N', 'S', 'E', 'W']
ctr = 0  # every ctr, food will be randomly generated

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# initializing the pygame window
width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cell Simulator')
screen.fill(WHITE)
# updating window
pygame.display.flip()

# initializing cells
john = Cell(random.randrange(10, width - 10, 10), random.randrange(10, height - 10, 10), random.choice(directionList), 5, 10, width, height)
foodList = addFood(foodList, 400, 50)

# looping window
run = True

while run:

    screen.fill(WHITE)

    # frame every 0.2 seconds
    time.sleep(0.2)

    # randomly generating food
    if(ctr == 20):
        foodList = addFood(foodList, random.randrange(10, width - 10, 10), random.randrange(10, height - 10, 10))
        ctr = 0

    # draw
    foodList = cellAction(john, foodList)
    drawFood(foodList)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

    ctr += 1

pygame.quit()