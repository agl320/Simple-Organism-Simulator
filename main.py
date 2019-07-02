import time
import math
import pygame
import random
from food import Food
from cell import Cell


def drawCell(cellName, state): # ACT = active RST = resting
    if(state == 'ACT'):
        pygame.draw.circle(screen, GREEN, cellName.Pos(), cellName.radius)
    elif(state == 'RST'):
        pygame.draw.circle(screen, BLUE, cellName.Pos(), cellName.radius)


def drawFood(foodList):
    if(len(foodList) > 0):
        for i in range(len(foodList)):
            pygame.draw.circle(screen, BLACK, foodList[i].Pos(), 5)

def addFood(foodList, x, y):
    foodList.append(Food(x,y))
    return foodList

def cellAction(cell, foodList):
    if(cell.resting == False):
        if(cell.stamina > 0):
            foodList = updateFood(cell, foodList)
            drawCell(cell, 'ACT')
            cell.StaminaMove()
            cell.setState(False)
            return foodList
        else:
            drawCell(cell, 'RST')
            cell.StaminaRest()
            cell.setState(True)
            return foodList
    else:
        if (cell.stamina != 100):
            drawCell(cell, 'RST')
            cell.StaminaRest()
            cell.setState(True)
            return foodList
        else:
            drawCell(cell, 'RST')
            cell.StaminaRest()
            cell.setState(False)
            return foodList


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

        else:

            slopeY, slopeX = float.as_integer_ratio((y_2 - y_1) / (x_2 / x_1))

            cellName.MoveToFood(slopeX, slopeY)

        return foodList

    else:
        cellName.Roam()

        return foodList

# foodList stores all instances of food; can remove and add
# distanceList stores the distances between named cell and all foods, gets closest
foodList = []
directionList = ['N', 'S', 'E', 'W']

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# initializing the pygame window
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cell Simulator')
screen.fill(WHITE)
# updating window
pygame.display.flip()

# initializing cells
john = Cell(50, 50, random.choice(directionList), 10, 10, width, height)
foodList = addFood(foodList, 400, 50)

# looping window
run = True

while run:

    screen.fill(WHITE)

    # frame every 0.2 seconds
    time.sleep(0.2)

    # draw
    foodList = cellAction(john, foodList)
    drawFood(foodList)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
