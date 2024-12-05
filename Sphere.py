import os
import time
import math

def generate_sphere(radius, rotation_x, rotation_y, light_theta, light_phi, screen_width, screen_height, scale_x=1.0, scale_y=1.0):
    """
    Generate a 3D sphere using spherical coordinates, rotating it and applying lighting effects.
    """
    # Define the characters used for different light intensities
    chars = '.,-~:;=!*#$@'

    # Precompute light direction based on theta and phi
    light_x = math.sin(light_phi) * math.cos(light_theta)
    light_y = math.sin(light_phi) * math.sin(light_theta)
    light_z = math.cos(light_phi)

    # Precompute rotation cosines and sines
    cos_rx, sin_rx = math.cos(rotation_x), math.sin(rotation_x)
    cos_ry, sin_ry = math.cos(rotation_y), math.sin(rotation_y)

    zbuffer = [0 for _ in range(screen_height * screen_width)]
    screen_pixels = [' ' for _ in range(screen_height * screen_width)]

    # Iterate over the spherical coordinates
    for phi in range(0, 628, 7):  # Increase step for faster rendering
        for theta in range(0, 628, 2):  # Increase step for faster rendering
            # Convert to radians
            phi_rad = phi / 100
            theta_rad = theta / 100

            # Spherical to Cartesian conversion
            x = radius * math.sin(phi_rad) * math.cos(theta_rad)
            y = radius * math.sin(phi_rad) * math.sin(theta_rad)
            z = radius * math.cos(phi_rad)

            # Apply rotation transformations
            x_rot = x * cos_ry - z * sin_ry
            z_rot = x * sin_ry + z * cos_ry
            y_rot = y * cos_rx - z_rot * sin_rx
            z_rot = y * sin_rx + z_rot * cos_rx

            # Normalize the normal vector
            nx, ny, nz = x_rot / radius, y_rot / radius, z_rot / radius

            # Calculate light intensity
            dot = max(0, nx * light_x + ny * light_y + nz * light_z)

            # Map intensity to character
            luminance_index = max(0, min(len(chars) - 1, int(dot * (len(chars) - 1))))

            # Convert to screen space
            xp = int(screen_width / 2 + scale_x * x_rot)
            yp = int(screen_height / 2 - scale_y * y_rot)

            # Make sure xp and yp are within valid bounds
            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                pixel_position = xp + screen_width * yp
                if zbuffer[pixel_position] < z_rot:  # Z-buffering
                    zbuffer[pixel_position] = z_rot
                    screen_pixels[pixel_position] = chars[luminance_index]

    # Create the final screen output
    screen = [''.join(screen_pixels[i * screen_width:(i + 1) * screen_width]) for i in range(screen_height)]

    return screen

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    radius = 10
    rotation_speed_x = 0.05
    rotation_speed_y = 0.1
    light_rotation_speed = 0.1

    scale_x = 2.0  # Horizontal scaling
    scale_y = 1.0  # Vertical scaling

    screen_width = 80
    screen_height = 24

    rotation_x = 0
    rotation_y = 0
    light_theta = 0  # Horizontal angle (light's movement around the sphere)
    light_phi = math.pi / 4  # Vertical angle (light's position from top to bottom)
    
    try:
        while True:
            start_time = time.time()  # Start FPS timing

            # Slower dynamic movement of the light (reduced speed using multipliers)
            light_theta = math.sin(time.time()*0.9) * math.pi * 2  # Reduced speed for horizontal movement
            light_phi = math.cos(time.time()*0.9) * math.pi  # Reduced speed for vertical movement
            
            # Generate the sphere based on screen dimensions
            screen = generate_sphere(radius, rotation_x, rotation_y, light_theta, light_phi, screen_width, screen_height, scale_x, scale_y)
            clear_screen()

            # Print the screen buffer
            for line in screen:
                print(line)

            # Update rotation angles
            rotation_x += rotation_speed_x
            rotation_y += rotation_speed_y

            # Calculate FPS
            elapsed_time = time.time() - start_time
            fps = 1 / elapsed_time if elapsed_time > 0 else 0
            print(f"\nFPS: {fps:.2f}")
            
            # Add a small delay to stabilize frame rate
            time.sleep(0.03)
    
    except KeyboardInterrupt:
        print("\nAnimation stopped.")

if __name__ == "__main__":
    main()
