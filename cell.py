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
        self.stamina = 100
        self.resting = False


    def Pos(self):
        return self.x, self.y

    def setState(self, state):
        self.resting = state

    def MoveToFood(self, slopeX, slopeY):
        if(slopeX > slopeY):
            if(slopeX > 0):
                self.x += self.speed
            elif(slopeX < 0):
                self.y -= self.speed
        else:
            if (slopeY > 0):
                self.y += self.speed
            elif (slopeY < 0):
                self.x -= self.speed

    def StaminaMove(self):
        self.stamina -= 10

    def StaminaRest(self):
        self.stamina += 10


    def Roam(self):

        num = randint(0, 100)

        if (num >= 40):

            pass

        else:
            self.direction = random.choice(directionList)

        if (self.direction == 'N' and self.y > self.speed):

            self.y -= self.speed

        elif (self.direction == 'S' and self.y < self.height):

            self.y += self.speed

        elif (self.direction == 'E' and self.x < self.width):

            self.x += self.speed

        elif (self.direction == 'W' and self.x > self.speed):

            self.x -= self.speed

        else:

            print('border reached')


