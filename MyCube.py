import os
import time
from math import sin, cos

# Constants
CUBE_SIZE = 10
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 30
K2 = 40
K1 = 20
ROTATE_SPEED = 0.05
SLEEP_TIME = 0.03

# Function to initialize the rotation angles
def init_rotation():
    return 0, 0, 0  # A, B, C angles

# Main rendering function
def main():
    clear_command = "cls" if os.name == "nt" else "clear"

    # Initialize rotation angles
    A, B, C = init_rotation()

    while True:
        # Reset buffers
        zbuffer = [-float('inf')] * (SCREEN_WIDTH * SCREEN_HEIGHT)
        screen_pixels = [' '] * (SCREEN_WIDTH * SCREEN_HEIGHT)

        # Iterate through the cube's grid points
        for cubeX in frange(-CUBE_SIZE, CUBE_SIZE, 0.6):
            for cubeY in frange(-CUBE_SIZE, CUBE_SIZE, 0.6):
                # Draw 6 cube faces using different characters
                draw_cube_faces(cubeX, cubeY, -CUBE_SIZE, '@', zbuffer, screen_pixels, A, B, C)
                draw_cube_faces(CUBE_SIZE, cubeY, cubeX, '$', zbuffer, screen_pixels, A, B, C)
                draw_cube_faces(-CUBE_SIZE, cubeY, -cubeX, '#', zbuffer, screen_pixels, A, B, C)
                draw_cube_faces(-cubeX, cubeY, CUBE_SIZE, '~', zbuffer, screen_pixels, A, B, C)
                draw_cube_faces(cubeX, -CUBE_SIZE, -cubeY, ';', zbuffer, screen_pixels, A, B, C)
                draw_cube_faces(cubeX, CUBE_SIZE, cubeY, '+', zbuffer, screen_pixels, A, B, C)

        # Clear and render the frame
        os.system(clear_command)
        render_frame(screen_pixels)

        # Increment rotation angles
        A += ROTATE_SPEED
        C += ROTATE_SPEED

        time.sleep(SLEEP_TIME)

# Function to generate floating-point ranges for iteration
def frange(start, stop, step):
    while start < stop:
        yield round(start, 2)
        start += step

# Function to draw cube faces
def draw_cube_faces(cubeX, cubeY, cubeZ, char, zbuffer, screen_pixels, A, B, C):
    x = calculate_x(cubeX, cubeY, cubeZ, A, B, C)
    y = calculate_y(cubeX, cubeY, cubeZ, A, B, C)
    z = calculate_z(cubeX, cubeY, cubeZ, A, B, C) + K2

    ooz = 1 / z  # Inverse of depth (1/z)
    xp = int(SCREEN_WIDTH / 2 + K1 * ooz * x * 2)
    yp = int(SCREEN_HEIGHT / 2 - K1 * ooz * y)

    if 0 <= xp < SCREEN_WIDTH and 0 <= yp < SCREEN_HEIGHT:
        pixel_position = xp + yp * SCREEN_WIDTH
        if ooz > zbuffer[pixel_position]:
            zbuffer[pixel_position] = ooz
            screen_pixels[pixel_position] = char

# 3D rotation functions
def calculate_x(i, j, k, A, B, C):
    return (j * sin(A) * sin(B) * cos(C)) - (k * cos(A) * sin(B) * cos(C)) + \
           (j * cos(A) * sin(C)) + (k * sin(A) * sin(C)) + (i * cos(B) * cos(C))

def calculate_y(i, j, k, A, B, C):
    return (j * cos(A) * cos(C)) + (k * sin(A) * cos(C)) - \
           (j * sin(A) * sin(B) * sin(C)) + (k * cos(A) * sin(B) * sin(C)) - \
           (i * cos(B) * sin(C))

def calculate_z(i, j, k, A, B, C):
    return (k * cos(A) * cos(B)) - ((j * sin(A) * cos(B)) + (i * sin(B)))

# Function to render the frame
def render_frame(screen_pixels):
    for i in range(SCREEN_HEIGHT):
        row = "".join(screen_pixels[i * SCREEN_WIDTH:(i + 1) * SCREEN_WIDTH])
        print(row)

if __name__ == "__main__":
    main()
