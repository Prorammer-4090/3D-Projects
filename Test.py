import math
import os
import time
from math import sin, cos, sqrt

# Global rotation angles (for rotating the cube)
A, B, C = 0, 0, 0
cubesize = 10  # Size of the cube
screen_width = 80  # Width of the terminal screen
screen_height = 30  # Height of the terminal screen
K2 = 40  # Depth scaling factor
K1 = 25  # Projection scaling factor

# Light configuration
light_radius = 30  # Radius of light's orbit around the cube
light_intensity = 3.5  # Intensity of the light (brightness)

# Primary light source direction (initial direction pointing towards the viewer)
light_direction1 = (0, 0, -1)  
light_theta1 = 0  # Azimuthal angle for the first light
light_phi1 = math.pi / 4  # Polar angle for the first light (start from 45 degrees)

# Secondary light source direction (initial direction for the second light)
light_direction2 = (0, -1, 0)  
light_theta2 = 0  # Azimuthal angle for the second light
light_phi2 = math.pi / 3  # Polar angle for the second light

# Function to normalize a 3D vector (make its length equal to 1)
def normalize(vector):
    """Normalize a 3D vector."""
    length = sqrt(sum(i * i for i in vector))  # Calculate vector length
    return (vector[0] / length, vector[1] / length, vector[2] / length)  # Normalize each component

# Function to calculate the dot product of two 3D vectors
def dot_product(v1, v2):
    """Compute dot product of two 3D vectors."""
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

# Function to subtract two vectors
def vector_subtract(v1, v2):
    """Subtract two vectors."""
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

# Main function to run the program
def main():
    clear_command = "cls" if os.name == "nt" else "clear"  # Command to clear screen based on OS

    while True:
        # Reset buffers (z-buffer for depth and screen buffer for pixel data)
        zbuffer = [-float('inf')] * (screen_width * screen_height)
        screen_pixels = [' '] * (screen_width * screen_height)

        # Loop through the surfaces of the cube and apply lighting calculations
        cubeX = -cubesize
        while cubeX < cubesize:
            cubeX += 0.6
            cubeY = -cubesize
            while cubeY < cubesize:
                cubeY += 0.6
                # Render all six cube faces
                calculate_surface(cubeX, cubeY, -cubesize, zbuffer, screen_pixels)  # Front face
                calculate_surface(cubesize, cubeY, cubeX, zbuffer, screen_pixels)  # Back face
                calculate_surface(-cubesize, cubeY, -cubeX, zbuffer, screen_pixels)  # Left face
                calculate_surface(-cubeX, cubeY, cubesize, zbuffer, screen_pixels)  # Right face
                calculate_surface(cubeX, -cubesize, -cubeY, zbuffer, screen_pixels)  # Bottom face
                calculate_surface(cubeX, cubesize, cubeY, zbuffer, screen_pixels)  # Top face

        # Clear the terminal and render the frame
        os.system(clear_command)
        for i in range(screen_height):
            row = "".join(screen_pixels[i * screen_width:(i + 1) * screen_width])
            print(row)

        # Increment rotation angles for continuous rotation
        global A, C
        A += 0.05
        C += 0.05

        # Update light positions for dynamic lighting effects
        update_light_direction(0.1, 0.05)

        time.sleep(0.03)  # Slow down the loop for visual smoothness

# Function to calculate the surface and its lighting on the cube
def calculate_surface(cubeX, cubeY, cubeZ, zbuffer, screen_pixels):
    """Calculate projection and render points on a surface."""
    world_x = calculate_x(cubeX, cubeY, cubeZ)
    world_y = calculate_y(cubeX, cubeY, cubeZ)
    world_z = calculate_z(cubeX, cubeY, cubeZ)

    # Compute the vector from the surface to the light sources (normal vector)
    surface_normal = normalize((cubeX, cubeY, cubeZ))

    distance1 = sqrt(light_direction1[0]**2 + light_direction1[1]**2 + light_direction1[2]**2)
    distance2 = sqrt(light_direction2[0]**2 + light_direction2[1]**2 + light_direction2[2]**2)

    attenuation1 = 1 / (1 + distance1**2)
    attenuation2 = 1 / (1 + distance2**2)

    # Modify light intensity factors to include attenuation
    light_intensity_factor1 = max(0, dot_product(surface_normal, normalize(light_direction1))) * light_intensity * attenuation1
    light_intensity_factor2 = max(0, dot_product(surface_normal, normalize(light_direction2))) * light_intensity * attenuation2

    # Combine the light intensities from both light sources
    light_intensity_factor = (light_intensity_factor1 + light_intensity_factor2) / 2

    # Project the 3D coordinates onto 2D screen space (perspective projection)
    z = world_z + K2  # Add depth offset
    ooz = 1 / z  # Inverse of z for perspective
    xp = int(screen_width / 2 + K1 * ooz * world_x * 2)  # Horizontal projection
    yp = int(screen_height / 2 - K1 * ooz * world_y)  # Vertical projection

    # Check if the projected pixel is within screen boundaries
    if 0 <= xp < screen_width and 0 <= yp < screen_height:
        pixel_position = xp + yp * screen_width
        if ooz > zbuffer[pixel_position]:  # Update z-buffer if closer to the camera
            zbuffer[pixel_position] = ooz
            luminance_chars = ".,-~:;=!*#$@"  # Set of characters representing brightness levels
            char_index = int(light_intensity_factor * (len(luminance_chars) - 1))
            screen_pixels[pixel_position] = luminance_chars[min(char_index, len(luminance_chars) - 1)]

# Functions to calculate the x, y, z coordinates of the cube surfaces after rotation
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

# Function to update light directions to simulate rotation around the cube
def update_light_direction(delta_theta, delta_phi):
    """Update light direction for two light sources to simulate smooth spherical orbits."""
    global light_direction1, light_theta1, light_phi1, light_direction2, light_theta2, light_phi2

    # Update first light source
    light_theta1 += delta_theta * 0.5
    light_phi1 += delta_phi * 0.3
    light_phi1 += 0.2 * math.sin(light_theta1 * 0.5)
    light_phi1 = max(math.pi/4, min(light_phi1, 3*math.pi/4))  # Keep within 45° to 135° range
    
    # Update second light source with inverse direction
    light_theta2 += delta_theta * 0.4
    light_phi2 += delta_phi * 0.25
    light_phi2 += 0.2 * math.sin(light_theta2 * 0.5)
    light_phi2 = max(math.pi/4, min(light_phi2, 3*math.pi/4))  # Keep within 45° to 135° range

    # Calculate the actual radii for the light sources
    actual_radius = light_radius * (1 + 0.1 * math.sin(light_theta1))

    # Calculate the 3D positions of the lights
    x1 = actual_radius * math.sin(light_phi1) * math.cos(light_theta1)
    y1 = actual_radius * math.sin(light_phi1) * math.sin(light_theta1)
    z1 = actual_radius * math.cos(light_phi1)
    
    # The second light is positioned exactly opposite to the first
    x2 = -x1
    y2 = -y1
    z2 = -z1

    # Normalize the light directions and set them
    light_direction1 = normalize((x1, y1, z1))
    light_direction2 = normalize((x2, y2, z2))

# Run the main program
if __name__ == "__main__":
    main()
