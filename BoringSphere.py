import os
import time
import math

def generate_sphere(radius, rotation_x, rotation_y, light_theta, light_phi, light_radius, light_intensity, screen_width, screen_height, scale_x=1.0, scale_y=1.0):
    """
    Generate a 3D sphere using spherical coordinates, rotating it and applying lighting effects.
    """
    # Define the characters used for different light intensities
    chars = '.,-~:;=!*#$@'

    # Calculate light direction based on light_radius, light_theta, and light_phi
    light_x = light_radius * math.sin(light_phi) * math.cos(light_theta)
    light_y = light_radius * math.sin(light_phi) * math.sin(light_theta)
    light_z = light_radius * math.cos(light_phi)

    # Precompute rotation cosines and sines
    cos_rx, sin_rx = math.cos(rotation_x), math.sin(rotation_x)
    cos_ry, sin_ry = math.cos(rotation_y), math.sin(rotation_y)

    zbuffer = [0 for _ in range(screen_height * screen_width)]
    screen_pixels = [' ' for _ in range(screen_height * screen_width)]

    # Iterate over the spherical coordinates
    for phi in range(0, 628, 7):
        for theta in range(0, 628, 2):
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

            # Calculate light intensity based on light vector and surface normal
            dot = max(0, nx * light_x + ny * light_y + nz * light_z) * light_intensity

            # Map intensity to character
            luminance_index = max(0, min(len(chars) - 1, int(dot * (len(chars) - 1))))

            # Convert to screen space
            xp = int(screen_width / 2 + scale_x * x_rot)
            yp = int(screen_height / 2 - scale_y * y_rot)

            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                pixel_position = xp + screen_width * yp
                if zbuffer[pixel_position] < z_rot:
                    zbuffer[pixel_position] = z_rot
                    screen_pixels[pixel_position] = chars[luminance_index]

    screen = [''.join(screen_pixels[i * screen_width:(i + 1) * screen_width]) for i in range(screen_height)]
    return screen

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    radius = 10
    rotation_speed_x = 0.05
    rotation_speed_y = 0.1
    light_rotation_speed = 0.05

    scale_x = 2.0  # Horizontal scaling
    scale_y = 1.0  # Vertical scaling

    screen_width = 80
    screen_height = 24

    rotation_x = 0
    rotation_y = 0
    light_theta = 0
    light_phi = math.pi / 4

    # New light properties
    light_radius = 1.5  # Distance of light from the center of the sphere
    light_intensity = 1.2  # Controls brightness, >1 increases brightness

    try:
        while True:
            start_time = time.time()

            # Update light position dynamically
            light_theta = math.sin(time.time() * 1.0) * math.pi * 2
            light_phi = math.cos(time.time() * 1.0) * math.pi

            # Generate the sphere with dynamic lighting
            screen = generate_sphere(radius, rotation_x, rotation_y, light_theta, light_phi, light_radius, light_intensity, screen_width, screen_height, scale_x, scale_y)
            clear_screen()

            for line in screen:
                print(line)

            rotation_x += rotation_speed_x
            rotation_y += rotation_speed_y

            elapsed_time = time.time() - start_time
            fps = 1 / elapsed_time if elapsed_time > 0 else 0
            print(f"\nFPS: {fps:.2f}")

            time.sleep(0.03)

    except KeyboardInterrupt:
        print("\nAnimation stopped.")

if __name__ == "__main__":
    main()
