#!/usr/bin/env python

from time import sleep
import os
import RPi.GPIO as GPIO
import subprocess
import datetime
import pygame
from pygame.locals import *


#setup pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN)

#setup variables
count = 0
up = False
down = False
command = ""
filename = ""
#camera_pause  = "650"
camera_pause  = "1000"

print("Raspberry Pi - Point & Shoot Camera v2.2")
print("-with pygame and screen, and messaging")



running = True;


pygame.init()
#screen = pygame.display.set_mode((725,92))
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

width, height = screen.get_size()

background = pygame.image.load("/home/pi/camera/homeimage.jpeg");
background.convert_alpha()
background = pygame.transform.scale(background,(width,height))



screen.blit(background,(0,0),(0,0,width,height))

#logo = pygame.image.load("rpilogo.jpeg");
logo = pygame.image.load("/home/pi/camera/raspberrypilogo.png")

logo = pygame.transform.scale(logo,(150,200))

screen.blit(logo,(20,0))


font = pygame.font.SysFont("verdana", 65, bold=1)

font2 = pygame.font.SysFont("verdana", 55, bold=0)
textsurface = font.render("Raspberry Pi", 1, pygame.Color(255,255,255))
screen.blit(textsurface,(20,280))
textsurface = font2.render("Point & Shoot Camera", 1, pygame.Color(255,255,255))
screen.blit(textsurface,(20,350))

 

def takepic(imageName):
    writemessage("taking photo...")
    command = "sudo raspistill -o " + imageName + " -q 100 -rot 270 -t " + camera_pause
    print(command)

    os.system(command)
    writemessage("loading photo...")

def loadpic(imageName):
    print("loading image: " + imageName)
    
    background = pygame.image.load(imageName);
    background.convert_alpha()
    background = pygame.transform.scale(background,(width,height))
    screen.blit(background,(0,0),(0,0,width,height))

    font = pygame.font.SysFont("verdana", 40, bold=0)
    textsurface = font.render(imageName, 1, pygame.Color(0,0,0))
    screen.blit(textsurface,(20,0))

    logo = pygame.image.load("/home/pi/camera/raspberrypilogo.png")
    logo = pygame.transform.scale(logo,(75,100))
    screen.blit(logo,(20,300))
    

def movepic(imageName):
    command = "sudo mv " + imageName + " /home/pi/camera/images/" + imageName
    print(command)
    os.system(command)

    
def writemessage(message):
    screen.fill(pygame.Color(0,0,0))
    #screen.blit(background,(0,0),(0,0,width,height))
    font = pygame.font.SysFont("verdana", 50, bold=1)
    textsurface = font.render(message, 1, pygame.Color(255,255,255))
    screen.blit(textsurface,(35,40))
    pygame.display.update()


    
while running:
    if(up == True):
        if(GPIO.input(24)==False):
            print("button 24 pressed")
            now = datetime.datetime.now()
            timeString = now.strftime("%Y-%m-%d_%H:%M:%S")
            print("request received: " + timeString)
            filename = "photo-" + timeString + ".jpg"
            takepic(filename)
            loadpic(filename)
            movepic(filename)
            
    up = GPIO.input(24)
    count = count + 1
    
    pygame.display.update()
    sleep(.1)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            running = False
            

    
    
#never hit
print("end of loop");


    
    
