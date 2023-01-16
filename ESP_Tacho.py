# importing required library
import pygame
import numpy as np
import time
from threading import Thread
import serial
from serial.tools.list_ports_windows import comports
import sys 
from time import perf_counter

# activate the pygame library .
pygame.init()
X = 600
Y = 600
ARROW_SIZE = 20
ARROW_POS = (X/2 - ARROW_SIZE/2, 0)

light_grey = (160, 160, 160)

angles = []
port = ""
ports = [a for (a, b, c) in comports(include_links=None)]
if(len(ports) == 1):
    port = ports[0]
elif(len(ports) == 0):
    print("no port was found")
    sys.exit()
else:
    # inquirer herre
    pass
def generate_angles():
    print("Available ports:")
    serial_port = serial.Serial()
    serial_port.baudrate = 115200
    serial_port.port = port
    serial_port.timeout = 0.01
    serial_port.open()
    angle = 0
    while(status):
        # angle = random.randint(0,359)
        read_val = serial_port.readline()
        # print(read_val)
        try:
            read_val = int(read_val[:len(read_val)-2])
        except ValueError:
            continue
        #print(read_val) # check how many bytes to read
        angles.append(read_val)
    serial_port.close()

def draw_rotated_line(surface, angle):
    # http://www.physicsbootcamp.org/Position-of-a-Circular-Motion.html#:~:text=2%20Position%20and%20Displacement%20on%20a%20Circle&text=x%3DRcos%CE%B8%2C%20y%3DRsin%CE%B8.
    # Position and Displacement on a Circle
    start = (X/2, Y/2)
    color = "red"
    thickness = 3

    # calculating end position from angle
    # -90 weil oben die 0 ist
    angle = (angle-100) / 360 * 2 * np.pi # convert to radians

    x = X/2 * np.cos(angle) + X/2 
    y = X/2 * np.sin(angle) + X/2
    end = (x, y);
    pygame.draw.line(surface, color, start, end, thickness)
    


# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))
 
# set the pygame window name
pygame.display.set_caption('speedometer')
 
# create a surface object, image is drawn on it.
imp = pygame.image.load("bootleg_scale.jpg").convert()
imp = pygame.transform.scale(imp, (X,Y))
 
# Using blit to copy content from one surface to other
scrn.blit(imp, (0, 0))


# paint screen one time
pygame.display.update()
status = True
thread = Thread(target=generate_angles)
thread.start()
ergebnis = []
ergebnisCounter = 0 
start = perf_counter();
while (status):
 
  # iterate over the list of Event objects
  # that was returned by pygame.event.get() method.
    for i in pygame.event.get():
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if i.type == pygame.QUIT:
            status = False 
    if len(angles) >= 1:
        angle = angles.pop(0)
        if len(angles) > 100:
            angle = angles.pop()
            angles = []
        # Alternative
        # angle = angles.pop()
        #angles = []
        scrn.fill(light_grey)
        scrn.blit(imp, (0,0))
        draw_rotated_line(scrn, angle)
        pygame.display.update()
        ergebnisCounter += 1
    if(len(angles) > 0):
        ergebnis.append(1)
    else:
        ergebnis.append(0)

print(str(len(angles)) + " Werte wurden noch nicht geupdatet von insgesamt " + str(ergebnisCounter))
print("Durchschnittlich befanden sich " + str(sum(ergebnis) / len(ergebnis)) + "Werte in der Warteschlange auf ihre Anzeige")
print(f"{ergebnisCounter} Updates in ca {int(perf_counter() - start)} s")
# deactivates the pygame library
pygame.quit()