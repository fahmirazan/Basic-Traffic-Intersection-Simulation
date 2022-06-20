import random
import time
import threading
import pygame
import sys

speeds = {'car': random.randint(1.0, 5.0)}


x = {'right':[0,0,0], 'left':[1400,1400,1400]}    
y = {'right':[348,370,398], 'left':[498,466,436]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car'}
directionNumbers = {0:'right'}

stoppingGap = 1 
movingGap = 1 

pygame.init()
simulation = pygame.sprite.Group()
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)
            
        if(direction=='right'):
            temp = self.image.get_rect().width + stoppingGap    
            x[direction][lane] -= temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        a=random.randint(1,10)
        if(self.direction=='right'):
            if(self.crossed==0):
                self.crossed = 1
            if((self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):                
                self.x += self.speed +  a


def generateVehicles():
    while(True):
        lane_number = (1)
        temp = random.randint(0,99)
        direction_number = 0
        dist = [25,50,75,100]
        if(temp<dist[0]):
            direction_number = 0
        Vehicle(lane_number, vehicleTypes[0], direction_number, directionNumbers[0])
        time.sleep(0.2)

class Main:
    thread1 = threading.Thread(name="initialization", args=())
    thread1.daemon = True
    thread1.start()


    black = (0, 0, 0)
    white = (255, 255, 255)

 
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)


    background = pygame.image.load('images/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())
    thread2.daemon = True
    thread2.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))

        for vehicle in simulation:  
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()
        pygame.display.update()


Main()