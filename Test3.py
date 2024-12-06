import math
import os
import time
import colorsys
from math import sin, cos, sqrt

# Global rotation angles
A, B, C = 0, 0, 0
cubesize = 10
screen_width = 80
screen_height = 30
K2 = 40
K1 = 25

# Light settings
light_radius = 30
light_intensity = 3.5
light_theta1, light_phi1 = 0, math.pi / 4
light_theta2, light_phi2 = 0, math.pi / 3

def normalize(vector):
    length = sqrt(sum(i * i for i in vector))
    return (vector[0] / length, vector[1] / length, vector[2] / length)

def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def update_light_direction(delta_theta, delta_phi):
    global light_theta1, light_phi1, light_theta2, light_phi2

    light_theta1 += delta_theta
    light_phi1 += 0.2 * math.sin(light_theta1)
    light_phi1 = max(math.pi / 6, min(light_phi1, 5 * math.pi / 6))

    light_theta2 -= delta_theta
    light_phi2 -= 0.2 * math.sin(light_theta2)
    light_phi2 = max(math.pi / 6, min(light_phi2, 5 * math.pi / 6))

    x1 = light_radius * sin(light_phi1) * cos(light_theta1)
    y1 = light_radius * sin(light_phi1) * sin(light_theta1)
    z1 = light_radius * cos(light_phi1)
    x2, y2, z2 = -x1, -y1, -z1

    light_direction1 = normalize((x1, y1, z1))
    light_direction2 = normalize((x2, y2, z2))

    return light_direction1, light_direction2

def calculate_surface(cubeX, cubeY, cubeZ, zbuffer, screen_pixels, light_directions):
    world_x = calculate_x(cubeX, cubeY, cubeZ)
    world_y = calculate_y(cubeX, cubeY, cubeZ)
    world_z = calculate_z(cubeX, cubeY, cubeZ)

    surface_normal = normalize((cubeX, cubeY, cubeZ))
    light_intensity_factor = 0

    for light in light_directions:
        distance = sqrt(sum(coord ** 2 for coord in light))
        attenuation = 1 / (1 + distance ** 2)
        intensity = max(0, dot_product(surface_normal, normalize(light))) * light_intensity * attenuation
        light_intensity_factor += intensity

    light_intensity_factor /= 2

    # Ensure a minimum light intensity to avoid too dark colors
    light_intensity_factor = max(0.1, light_intensity_factor)  # Prevent dark colors

    z = world_z + K2
    ooz = 1 / z
    xp = int(screen_width / 2 + K1 * ooz * world_x * 2)
    yp = int(screen_height / 2 - K1 * ooz * world_y)

    if 0 <= xp < screen_width and 0 <= yp < screen_height:
        pixel_position = xp + yp * screen_width
        if ooz > zbuffer[pixel_position]:
            zbuffer[pixel_position] = ooz

            # Convert intensity to a color using HSV
            # Here, we use green as the primary color and adjust brightness
            hue = 0.33  # Green in HSV color space
            saturation = 1.0
            value = min(1, light_intensity_factor)  # Cap the intensity at 1 for full brightness
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

            # Adjust color to add some white light blending
            r = min(1, r + light_intensity_factor * 0.3)
            g = min(1, g + light_intensity_factor * 0.3)
            b = min(1, b + light_intensity_factor * 0.3)

            # Convert to ANSI RGB color codes
            r, g, b = int(r * 255), int(g * 255), int(b * 255)

            # ANSI escape code for the calculated color
            color_code = f"\033[38;2;{r};{g};{b}m"

            # Assign the colored character to the screen
            luminance_chars = ".,-~:;=!*#$@"  # Set of characters representing brightness levels
            char_index = int(light_intensity_factor * (len(luminance_chars) - 1))
            screen_pixels[pixel_position] = f"{color_code}{luminance_chars[min(char_index, len(luminance_chars) - 1)]}\033[0m"

def calculate_x(i, j, k):
    return (j * sin(A) * sin(B) * cos(C)) - (k * cos(A) * sin(B) * cos(C)) + \
           (j * cos(A) * sin(C)) + (k * sin(A) * sin(C)) + (i * cos(B) * cos(C))

def calculate_y(i, j, k):
    return (j * cos(A) * cos(C)) + (k * sin(A) * cos(C)) - \
           (j * sin(A) * sin(B) * sin(C)) + (k * cos(A) * sin(B) * sin(C)) - \
           (i * cos(B) * sin(C))

def calculate_z(i, j, k):
    return (k * cos(A) * cos(B)) - ((j * sin(A) * cos(B)) + (i * sin(B)))

def main():
    clear_command = "cls" if os.name == "nt" else "clear"
    while True:
        zbuffer = [-float('inf')] * (screen_width * screen_height)
        screen_pixels = [' '] * (screen_width * screen_height)
        
        light_directions = update_light_direction(0.03, 0.02)
        
        for cubeX in range(-cubesize, cubesize):
            for cubeY in range(-cubesize, cubesize):
                for side in (-cubesize, cubesize):
                    calculate_surface(cubeX, cubeY, side, zbuffer, screen_pixels, light_directions)
                    calculate_surface(side, cubeY, cubeX, zbuffer, screen_pixels, light_directions)
                    calculate_surface(cubeX, side, cubeY, zbuffer, screen_pixels, light_directions)

        os.system(clear_command)
        print("\n".join("".join(screen_pixels[i * screen_width:(i + 1) * screen_width]) for i in range(screen_height)))

        global A, C
        A += 0.05
        C += 0.05

        fps = 1 / 0.03
        print(f"FPS: {fps:.2f}")

        time.sleep(0.03)

if __name__ == "__main__":
    main()
