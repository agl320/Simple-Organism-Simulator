import random
from random import randint

directionList = ['N', 'S', 'E', 'W']


class Cell:
    def __init__(self, x, y, direction, radius, speed, width, height):
        self.x = x
        self.y = y
        self.direction = direction
        self.radius = radius
        self.speed = speed
        self.width = width
        self.height = height


    def Pos(self):
        return self.x, self.y


    def MoveToFood(self, foodX, foodY):
        if(self.x > foodX):
            self.x -= self.speed
        elif(self.x < foodX):
            self.x += self.speed
        elif(self.y > foodY):
            self.y -= self.speed
        elif(self.y < foodY):
            self.y += self.speed


    def Roam(self):

        num = randint(0, 100)

        if (num >= 40):

            pass

        else:
            self.direction = random.choice(directionList)

        while(True):

            if (self.direction == 'N' and self.y > self.speed):

                self.y -= self.speed
                break

            elif (self.direction == 'S' and self.y < self.height):

                self.y += self.speed
                break

            elif (self.direction == 'E' and self.x < self.width):

                self.x += self.speed
                break

            elif (self.direction == 'W' and self.x > self.speed):

                self.x -= self.speed
                break

            else:

                self.direction = random.choice(directionList)


