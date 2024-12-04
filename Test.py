import math
import os
import time
from math import sin, cos, sqrt

# Global rotation angles
A, B, C = 0, 0, 0
cubesize = 10
screen_width = 80
screen_height = 30
K2 = 40
K1 = 25

# Light configuration
light_radius = 20  # Radius of light's orbit around the cube
light_intensity = 1.3  # Adjust light intensity (multiplier)

# Primary light source
light_direction1 = (0, 0, -1)  # Initial direction of light (towards viewer)
light_theta1 = 0    # Azimuthal angle
light_phi1 = math.pi / 4  # Polar angle (start from 45 degrees)

# Secondary light source
light_direction2 = (0, -1, 0)  # Initial direction of second light
light_theta2 = 0    # Azimuthal angle
light_phi2 = math.pi / 3  # Polar angle 

def normalize(vector):
    """Normalize a 3D vector."""
    length = sqrt(sum(i * i for i in vector))
    return (vector[0] / length, vector[1] / length, vector[2] / length)

def dot_product(v1, v2):
    """Compute dot product of two 3D vectors."""
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def vector_subtract(v1, v2):
    """Subtract two vectors."""
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

def main():
    clear_command = "cls" if os.name == "nt" else "clear"

    while True:
        # Reset buffers
        zbuffer = [-float('inf')] * (screen_width * screen_height)
        screen_pixels = [' '] * (screen_width * screen_height)

        # Loop through the cube surfaces and apply lighting calculations
        cubeX = -cubesize
        while cubeX < cubesize:
            cubeX += 0.6
            cubeY = -cubesize
            while cubeY < cubesize:
                cubeY += 0.6
                calculate_surface(cubeX, cubeY, -cubesize, zbuffer, screen_pixels)
                calculate_surface(cubesize, cubeY, cubeX, zbuffer, screen_pixels)
                calculate_surface(-cubesize, cubeY, -cubeX, zbuffer, screen_pixels)
                calculate_surface(-cubeX, cubeY, cubesize, zbuffer, screen_pixels)
                calculate_surface(cubeX, -cubesize, -cubeY, zbuffer, screen_pixels)
                calculate_surface(cubeX, cubesize, cubeY, zbuffer, screen_pixels)

        # Clear the terminal and render the frame
        os.system(clear_command)
        for i in range(screen_height):
            row = "".join(screen_pixels[i * screen_width:(i + 1) * screen_width])
            print(row)

        # Increment rotation angles
        global A, C
        A += 0.05
        C += 0.05

        # Update light positions
        update_light_direction(0.1, 0.05)

        time.sleep(0.03)

def calculate_surface(cubeX, cubeY, cubeZ, zbuffer, screen_pixels):
    """Calculate projection and render points on a surface."""
    world_x = calculate_x(cubeX, cubeY, cubeZ)
    world_y = calculate_y(cubeX, cubeY, cubeZ)
    world_z = calculate_z(cubeX, cubeY, cubeZ)

    # Compute the vector from the surface to the light sources
    surface_normal = normalize((cubeX, cubeY, cubeZ))
    
    # Calculate lighting from two light sources
    light_intensity_factor1 = max(0, dot_product(surface_normal, normalize(light_direction1))) * light_intensity
    light_intensity_factor2 = max(0, dot_product(surface_normal, normalize(light_direction2))) * light_intensity
    
    # Combine light intensities (averaging for softer lighting)
    light_intensity_factor = (light_intensity_factor1 + light_intensity_factor2) / 2

    # Project to 2D screen space
    z = world_z + K2
    ooz = 1 / z
    xp = int(screen_width / 2 + K1 * ooz * world_x * 2)
    yp = int(screen_height / 2 - K1 * ooz * world_y)

    if 0 <= xp < screen_width and 0 <= yp < screen_height:
        pixel_position = xp + yp * screen_width
        if ooz > zbuffer[pixel_position]:
            zbuffer[pixel_position] = ooz
            luminance_chars = ".,-~:;=!*#$@"
            char_index = int(light_intensity_factor * (len(luminance_chars) - 1))
            screen_pixels[pixel_position] = luminance_chars[min(char_index, len(luminance_chars) - 1)]

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

def update_light_direction(delta_theta, delta_phi):
    """Update light direction for two light sources to simulate dynamic spherical orbits."""
    global light_direction1, light_theta1, light_phi1, light_direction2, light_theta2, light_phi2

    # Update first light source
    light_theta1 += delta_theta * 2
    light_phi1 += delta_phi
    light_phi1 += 0.5 * math.sin(light_theta1)
    light_phi1 = max(math.pi/6, min(light_phi1, 5*math.pi/6))
    
    # Update second light source (with offset)
    light_theta2 += delta_theta * 1.5
    light_phi2 += delta_phi * 0.8
    light_phi2 += 0.4 * math.sin(light_theta2)
    light_phi2 = max(math.pi/6, min(light_phi2, 5*math.pi/6))

    # Dynamic radius for more interesting movement
    actual_radius1 = light_radius * (1 + 0.3 * math.sin(light_theta1))
    actual_radius2 = light_radius * (1 + 0.3 * math.sin(light_theta2))

    # Calculate light directions
    x1 = actual_radius1 * math.sin(light_phi1) * math.cos(light_theta1)
    y1 = actual_radius1 * math.sin(light_phi1) * math.sin(light_theta1)
    z1 = actual_radius1 * math.cos(light_phi1)
    
    x2 = actual_radius2 * math.sin(light_phi2) * math.cos(light_theta2)
    y2 = actual_radius2 * math.sin(light_phi2) * math.sin(light_theta2)
    z2 = actual_radius2 * math.cos(light_phi2)

    # Set the new light directions (normalized)
    light_direction1 = normalize((x1, y1, z1))
    light_direction2 = normalize((x2, y2, z2))

if __name__ == "__main__":
    main()