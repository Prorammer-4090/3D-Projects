
import os
import math as m

A, B, C = 0, 0, 0

cubeWidth = 20
width, height = 160, 44
zBuffer = [0.0] * (width * height * 4)
buffer = [' '] * (width * height)
backgroundASCIICode = ' '
horizontalOffset = 0.0
K1 = 40

distanceFromCam = 100
incrementSpeed = 0.6

def calculateX(i, j, k):
    return (j * m.sin(A) * m.sin(B) * m.cos(C) -
            k * m.cos(A) * m.sin(B) * m.cos(C) +
            j * m.cos(A) * m.sin(C) +
            k * m.sin(A) * m.sin(C) +
            i * m.cos(B) * m.cos(C))

def calculateY(i, j, k):
    return (j * m.cos(A) * m.cos(C) +
            k * m.sin(A) * m.cos(C) -
            j * m.sin(A) * m.sin(B) * m.sin(C) +
            k * m.cos(A) * m.sin(B) * m.sin(C) -
            i * m.cos(B) * m.sin(C))

def calculateZ(i, j, k):
    return (k * m.cos(A) * m.cos(B) -
            j * m.sin(A) * m.cos(B) +
            i * m.sin(B))

def calculateForSurface(cubeX: float, cubeY: float, cubeZ: float, ch: str):
    x = calculateX(cubeX, cubeY, cubeZ)
    y = calculateY(cubeX, cubeY, cubeZ)
    z = calculateZ(cubeX, cubeY, cubeZ) + distanceFromCam

    ooz = 1/z

    xp = int(width/2 - 2 * cubeWidth + horizontalOffset + K1 * ooz * x * 2)
    yp = int(height/2 + K1 * ooz * y)

    idx = xp + yp * width
    if (idx >= 0 and idx < width * height):
        if (ooz > zBuffer[idx]):
            zBuffer[idx] = ooz
            buffer[idx] = ch

while(True):
    for i in range(width * height):
        buffer[i] = backgroundASCIICode
        zBuffer[i] = 0.0

    for cube_x in range(-int(cubeWidth), int(cubeWidth)):
        for cube_y in range(-int(cubeWidth), int(cubeWidth)):
            calculateForSurface(cube_x, cube_y, -cubeWidth, '@')
            calculateForSurface(cubeWidth, cube_y, cube_x, '$')
            calculateForSurface(-cubeWidth, cube_y, -cube_x, '~')
            calculateForSurface(-cube_x, cube_y, cubeWidth, '#')
            calculateForSurface(cube_x, -cubeWidth, -cube_y, ';')
            calculateForSurface(cube_x, cubeWidth, cube_y, '+')

    # cubeX = -cubeWidth
    # while cubeX < cubeWidth:
    #     cubeX += incrementSpeed
    #     cubeY = -cubeWidth
    #     while cubeY < cubeWidth:
    #         cubeY += incrementSpeed
    #         calculateForSurface(cubeX, cubeY, -cubeWidth, '@')
    #         calculateForSurface(cubeWidth, cubeY, cubeX, '$')
    #         calculateForSurface(-cubeWidth, cubeY, -cubeX, '~')
    #         calculateForSurface(-cubeX, cubeY, cubeWidth, '#')
    #         calculateForSurface(cubeX, -cubeWidth, -cubeY, ';')
    #         calculateForSurface(cubeX, cubeWidth, cubeY, '+')

    os.system("cls" if os.name == 'nt' else 'clear')
    for k in range(width * height):
        print(buffer[k], end='' if k % width != 0 else '\n')

    A += 0.4
    B += 0.4
