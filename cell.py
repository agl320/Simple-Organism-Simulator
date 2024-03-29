import random
from random import randint

directionList = ['N', 'S', 'E', 'W']


class Cell:
    def __init__(self, x, y, direction, radius, speed, window_width, window_height, hunger = 100, hungerDepletion = 2, state = 'ACT', age = 0, range = 200):
        self.x = x
        self.y = y
        self.direction = direction
        self.radius = radius
        self.speed = speed
        self.window_width = window_width
        self.window_height = window_height
        self.hunger = hunger
        self.hungerDepletion = hungerDepletion
        self.foodCounter = 0
        self.state = state
        self.age = age
        self.range = range

    def Pos(self):
        return self.x, self.y

    def MoveToFood(self, foodX, foodY):

        if self.x > foodX:
            self.x -= self.speed
        elif self.x < foodX:
            self.x += self.speed
        elif self.y > foodY:
            self.y -= self.speed
        elif self.y < foodY:
            self.y += self.speed

        self.hunger -= self.hungerDepletion

    def Roam(self):

        num = randint(0, 100)

        if (num >= 20):

            pass

        else:
            self.direction = random.choice(directionList)

        while(True):

            if (self.direction == 'N' and self.y > self.speed):

                self.y -= self.speed
                break

            elif (self.direction == 'S' and self.y < self.window_height):

                self.y += self.speed
                break

            elif (self.direction == 'E' and self.x < self.window_width):

                self.x += self.speed
                break

            elif (self.direction == 'W' and self.x > self.speed):

                self.x -= self.speed
                break

            else:

                self.direction = random.choice(directionList)

        self.hunger -= self.hungerDepletion



