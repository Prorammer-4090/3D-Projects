import os
import time
from math import sin, cos

# Global rotation angles
A, B, C = 0, 0, 0
cubesize = 10
screen_width = 80
screen_height = 30
K2 = 40
K1 = 25

def main():
    clear_command = "cls" if os.name == "nt" else "clear"

    while True:
        # Reset buffers
        zbuffer = [-float('inf')] * (screen_width * screen_height)
        screen_pixels = [' '] * (screen_width * screen_height)

        cubeX = -cubesize
        while cubeX < cubesize:
            cubeX += 0.6
            cubeY = -cubesize
            while cubeY < cubesize:
                cubeY += 0.6
                # Draw 6 cube faces using different characters
                calculate_surface(cubeX, cubeY, -cubesize, '@', zbuffer, screen_pixels)
                calculate_surface(cubesize, cubeY, cubeX, '$', zbuffer, screen_pixels)
                calculate_surface(-cubesize, cubeY, -cubeX, '#', zbuffer, screen_pixels)
                calculate_surface(-cubeX, cubeY, cubesize, '~', zbuffer, screen_pixels)
                calculate_surface(cubeX, -cubesize, -cubeY, ';', zbuffer, screen_pixels)
                calculate_surface(cubeX, cubesize, cubeY, '+', zbuffer, screen_pixels)

        # Clear and render frame
        os.system(clear_command)
        for i in range(screen_height):
            row = "".join(screen_pixels[i * screen_width:(i + 1) * screen_width])
            print(row)

        # Increment rotation angles
        global A, C
        A += 0.05
        C += 0.05

        time.sleep(0.03)

def calculate_surface(cubeX, cubeY, cubeZ, ch, zbuffer, screen_pixels):
    """Calculate projection and render points on a surface."""
    x = calculate_x(cubeX, cubeY, cubeZ)
    y = calculate_y(cubeX, cubeY, cubeZ)
    z = calculate_z(cubeX, cubeY, cubeZ) + K2

    ooz = 1 / z  # One over Z (depth inversion)
    xp = int(screen_width / 2 + K1 * ooz * x*2)
    yp = int(screen_height / 2 - K1 * ooz * y)

    if 0 <= xp < screen_width and 0 <= yp < screen_height:
        pixel_position = xp + yp * screen_width
        if ooz > zbuffer[pixel_position]:
            zbuffer[pixel_position] = ooz
            luminance_index = int(ooz * 8)  # Shading based on depth
            screen_pixels[pixel_position] = ch

def calculate_x(i, j, k):
    global A, B, C
    return (j * sin(A) * sin(B) * cos(C)) - (k * cos(A) * sin(B) * cos(C)) + \
           (j * cos(A) * sin(C)) + (k * sin(A) * sin(C)) + (i * cos(B) * cos(C))

def calculate_y(i, j, k):
    global A, B, C
    return (j * cos(A) * cos(C)) + (k * sin(A) * cos(C)) - \
           (j * sin(A) * sin(B) * sin(C)) + (k * cos(A) * sin(B) * sin(C)) - \
           (i * cos(B) * sin(C))

def calculate_z(i, j, k):
    global A, B, C
    return (k * cos(A) * cos(B)) - ((j * sin(A) * cos(B)) + (i * sin(B)))

if __name__ == "__main__":
    main()
