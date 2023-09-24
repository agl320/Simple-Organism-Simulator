import time
import math
import pygame
import random
from food import Food
from cell import Cell
import matplotlib.pyplot as plt


# draws the cell onto the screen
def draw_cell(cell):
    if cell.state == 'ACT':
        pygame.draw.circle(screen, GREEN_DARK, cell.Pos(), cell.radius)
    elif cell.state == 'RST':
        pygame.draw.circle(screen, BLUE, cell.Pos(), cell.radius)
    elif cell.state == 'RPR':
        pygame.draw.circle(screen, GREEN, cell.Pos(), cell.radius)

def animation_rpr(cell):
    pygame.draw.circle(screen, RED, cell.Pos(), cell.radius * 2)
    time.sleep(0.1)
    pygame.draw.circle(screen, RED_LIGHT, cell.Pos(), cell.radius * 3)
    time.sleep(0.1)
    pygame.draw.circle(screen, RED_LIGHT_PLUS, cell.Pos(), cell.radius * 4)

def draw_food(food):
    pygame.draw.circle(screen, BLACK, food.Pos(), 5)

# cell reproduction
def cell_reproduce(cell):
    cell_x, cell_y = cell.Pos()
    listCell.append(Cell(cell_x, cell_y, random.choice(listDirection), cell_radius, cell_speed, screen_width, screen_height))
    cell.foodCounter -= 1

# calculates distance towards closest food source
def find_closest_food(cell, listFood):
    food_distances_list = []
    cell_x, cell_y = cell.Pos()

    if len(listFood) > 0:

        for i in range(len(listFood)):

            food_x, food_y = listFood[i].Pos()

            # remove distances out of range
            food_distances_list.append(math.sqrt((food_x - cell_x) ** 2 + (food_y - cell_y) ** 2))
            # distance formula; finds distances between cell and all foods

        closest_food_index = food_distances_list.index(min(food_distances_list))

        if min(food_distances_list) < cell.range:

            closest_food = listFood[closest_food_index] # closest food; type object

            Cfood_x, Cfood_y = closest_food.Pos() # get closest food coordinates

            if cell_x == Cfood_x and cell_y == Cfood_y:

                # checking if the cell coordinates match food coordinates; cell eats food

                listFood.pop(closest_food_index) # removing food from list

                cell.foodCounter += 1
                cell.hunger += food_regen

                if(cell.state == 'RPR'):
                    cell_reproduce(cell)
                    cell.foodCounter -= 1
                    cell.state = 'RST'

            else:

                cell.MoveToFood(Cfood_x, Cfood_y)

                cell_x, cell_y = cell.Pos()

                if cell_x == Cfood_x and cell_y == Cfood_y:
                    # checking if the cell coordinates match food coordinates; cell eats food

                    listFood.pop(closest_food_index)  # removing food from list

                    cell.foodCounter += 1
                    cell.hunger += food_regen

                    if (cell.state == 'RPR'):
                        cell_reproduce(cell)
                        cell.foodCounter -= 1
                        cell.state = 'RST'
        else:
            cell.Roam()

    else:
        cell.Roam() # if there are no food present (in vicinity) then randomly roam

    return listFood # return updated food list


def action_cell(cell, listFood):

    if cell.age < cell_lifetime and cell.foodCounter > 0 and cell.state == 'ACT':
        # if the cell is not at the end of lifetime and has eaten 1 food
        rpr_chance = random.randint(0, 1 + cell.age) # chance the cell will attempt to reproduce

        if rpr_chance == 0:
            cell.state = 'RPR' # reproduce

        else:
            cell.state = 'RST' # rest

    elif cell.age < cell_lifetime and cell.foodCounter == 0 and cell.state == 'ACT':
        # placeholder; the cell has not ate any food and not at end of lifetime, stays in active state
        pass

    elif cell.age == cell_lifetime:

        cell.state = 'RPR'

        # if cell is at the end of lifetime, the cell will attempt to reproduce

    elif cell.state == 'RST':
        pass

    elif cell.state == 'RPR':
        pass

    else:
        print('ERROR')


    if cell.state == 'ACT':
        listFood = find_closest_food(cell, listFood)

    elif cell.state == 'RST':
        pass # placeholder as cell does nothing

    elif cell.state == 'RPR':
        listFood = find_closest_food(cell, listFood)


    return listFood

def draw_objects(listCell, listFood):
    for i in range(len(listCell)):
        draw_cell(listCell[i])

    for i in range(len(listFood)):
        draw_food(listFood[i])

def cell_age(listCell): # cell ages by one
    for i in range(len(listCell)):
        listCell[i].age += 1

    return listCell

def reset_all_state(listCell, state, ignoreState): # reset cell states to specified state
    for i in range(len(listCell)):
        if(listCell[i].state != ignoreState):
            listCell[i].state = state
    return listCell

def check_all_state(listCell, state):
    for i in range(len(listCell)):
        if listCell[i].state != state:
            return False
    return True

def reset_all_food(listCell):
    for i in range(len(listCell)):
        if(listCell[i].state != 'RPR'):
            listCell[i].foodCounter = 0

    return listCell

def remove_zero_hunger(listCell): # removes cells with no hunger
    listCell_tmp = []
    for i in range(len(listCell)):
        if(listCell[i].hunger != 0):
            listCell_tmp.append(listCell[i])

    return listCell_tmp



# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREEN_DARK = (2, 189, 2)
RED = (255, 0, 0)
RED_LIGHT = (255,100, 100)
RED_LIGHT_PLUS = (255, 172, 172)
GREY_LIGHT = (215, 219, 224)
PINK = (245, 66, 224)


# DATA INIT
listFood = []  # list of all food instances
listCell = []  # list of all cell instances
listCell_tmp = [] # list of cell instances used to remove cells
listDirection = ['N', 'S', 'E', 'W']  # list of all directions a cell may go

# INITIAL CONDITIONS
# cell size
cell_radius = 5
# rounds before a cell dies
cell_lifetime = 3
# food regeneration after each round
food_regen = 100 
# number of starting food cells
number_of_food = 100
# number of starting cells
number_of_cells = 20

# graphing
population_per_generation = []

# initializing the pygame window
pygame.init()
pygame.font.init()
screen_width, screen_height = 1200, 750  # screen with and height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Cell Simulator')
fontTNR = pygame.font.SysFont('Times New Roman', 15)
screen.fill(WHITE)
pygame.display.flip()

for i in range(number_of_cells):

    # cell creation

    cell_x = random.randrange(cell_radius, screen_width - cell_radius, cell_radius)
    cell_y = random.randrange(cell_radius, screen_height - cell_radius, cell_radius)
    cell_direction = random.choice(listDirection)

    cell_speed = cell_radius

    listCell.append(Cell(cell_x, cell_y, random.choice(listDirection), cell_radius, cell_speed, screen_width, screen_height))

# spawns food beforehand in order to not trigger aging

for i in range(number_of_food):
    food_x_pos = random.randrange(cell_radius, screen_width - cell_radius, cell_radius)
    food_y_pos = random.randrange(cell_radius, screen_height - cell_radius, cell_radius)
    listFood.append(Food(food_x_pos, food_y_pos))

run = True

# running pygame window

population_per_generation.append(len(listCell))

while run:

    '''
    Order of events:
    
    - Spawns food if there are none // cell age
    - Cell action
    - Draw objects
    - Remove cells who are at end of lifetime
    - End program checks
    '''

    if len(listFood) == 0 or check_all_state(listCell, 'RST'): # if no food, draw food

        population_per_generation.append(len(listCell))

        listCell = cell_age(listCell)

        for i in range(number_of_food):

            food_x_pos = random.randrange(cell_radius, screen_width - cell_radius, cell_radius)
            food_y_pos = random.randrange(cell_radius, screen_height - cell_radius, cell_radius)

            listFood.append(Food(food_x_pos, food_y_pos))

        listCell_tmp = []

        for i in range(len(listCell)):
            if listCell[i].age <= cell_lifetime:
                listCell_tmp.append(listCell[i])

        del listCell[:]

        listCell = listCell_tmp[:]

        listCell = reset_all_food(listCell)

        listCell = reset_all_state(listCell, 'ACT', 'RPR')

    if listCell:
        for i in range(len(listCell)):
            # cell action

            listFood = action_cell(listCell[i], listFood)



    listCell = remove_zero_hunger(listCell)

    #time.sleep(0.03)  # 0.2 second pause between frames

    screen.fill(WHITE)

    draw_objects(listCell, listFood)

    pygame.display.flip()  # update the screen

    # remove cells

    if not listCell:  # if there are no more cells; end program
        run = False
        break

    time.sleep(0.001)

    for event in pygame.event.get():  # if program is exited
        if event.type == pygame.QUIT:
            run = False
            break

y = []
y = population_per_generation[:]
x = []

for i in range(len(population_per_generation)):
    x.append(i)

plt.plot(x, y, 'go--')
plt.show()

pygame.quit()

