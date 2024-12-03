#this is just a fun project to try and interpret someones C project into python syntax back when I was learning C for the first time and already knew python.
#credit to servetgulnaroglu, for the source C code and matrix calculations

from math import sin, cos
from time import sleep

#NOTE: if the cube is jittery, just increase the terminal window size vertically (and horizontally if you are docking your terminal funny). 

A = B = C = 0.0
cubesize = 10
width = 120 
height = 33 
backgroundsymb = ' '
distancefromcam = 100
k1 = 40
incspeed = 0.6
buffer = [] #buffer holds all of the art characters to be printed
Zbuffer = [] #Zbuffer holds all of the Z values for each pixel, determining whether an art character should be placed in the corrisponding buffer index or not
#populate both with empty values, python will complain later if these indexes dont already exist, so we make them here
for i in range(width * height):
    buffer.append(backgroundsymb)
for i in range(width * height * 4):
    Zbuffer.append(0)

def main():
    global A, B, C
    print(f"\x1b[2J") #clear top and bottom of terminal, code begins to execute here    

    while True:
        #populate fresh buffer, overwrites
        for i in range(width * height):
            buffer[i] = (backgroundsymb)
        #populate fresh Zbuffer, overwrites
        for i in range(width * height * 4):
            Zbuffer[i] = (0)
        
        #init vars
        cubeX = -cubesize
        cubeY = -cubesize
        while cubeX < cubesize:
            cubeX += incspeed #i++
            cubeY = -cubesize #reset once inner loop finishes
            while cubeY < cubesize:
                cubeY += incspeed #i++
                calculateForSurface(cubeX, cubeY, -cubesize, '@')
                calculateForSurface(cubesize, cubeY, cubeX, '$')
                calculateForSurface(-cubesize, cubeY, -cubeX, '#')
                calculateForSurface(-cubeX, cubeY, cubesize, '~')
                calculateForSurface(cubeX, -cubesize, -cubeY, ';')
                calculateForSurface(cubeX, cubesize, cubeY, '+')
                
        print(f"\x1b[H") #reset cursor to top left of terminal
        #print cube by reading the contents of buffer
        i = 0
        while i < width * height:
            if i % width != 0:
                print(buffer[i], end='')
            else:
                print()#'\n'
            i += 1
            
        #increment rotation
        A += 0.05
        C += 0.05
        sleep(0.01) #determines cubes "frame rate"        
    #NOTE: main() loops at this point and will never end

def calculateForSurface(cubeX, cubeY, cubeZ, ch):
    x = calculateX(cubeX, cubeY, cubeZ)
    y = calculateY(cubeX, cubeY, cubeZ)
    z = calculateZ(cubeX, cubeY, cubeZ) + distancefromcam

    horizontalOffset = 2 * cubesize
    ooz = 1 / z
    xp = int(width / 2 - horizontalOffset + k1 * ooz * x * 2)
    yp = int(height / 2 + k1 * ooz * y)

    idx = xp + yp * width
    if idx >= 0 and idx < width * height and ooz > Zbuffer[idx]:
        Zbuffer[idx] = ooz
        buffer[idx] = ch

    #These three return the result when the current coords are passed through the resulting transformation matricies of rotating [i, j, k] 
    #(credit: servetgulnaroglu)
def calculateX(i, j, k):
    global A, B, C
    return (j * sin(A) * sin(B) * cos(C)) - (k * cos(A) * sin (B) * cos(C)) + (j * cos(A) * sin(C)) + (k * sin(A) * sin(C)) + (i * cos(B) * cos(C))

def calculateY(i, j, k):
    global A, B, C
    return (j * cos(A) * cos(C)) + (k * sin(A) * cos(C)) - (j * sin(A) * sin(B) * sin(C)) + (k * cos(A) * sin(B) * sin(C)) - (i * cos(B) * sin(C))

def calculateZ(i, j, k):
    global A, B, C
    return (k * cos(A) * cos(B)) - ((j * sin(A) * cos(B)) + (i * sin(B)))


main()