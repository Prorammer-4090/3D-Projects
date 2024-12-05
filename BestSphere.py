import os
import time
import math

# Function to generate the 3D sphere with lighting and rotation
def generate_sphere(radius, rotation_x, rotation_y, light_theta, light_phi, light_radius, light_intensity, screen_width, screen_height, scale_x=1.0, scale_y=1.0):
    chars = '.,-~:;=!*#$@'  # Characters for shading based on light intensity
    ambient_light = 0.1  # Constant ambient light
    specular_power = 32  # Controls sharpness of specular highlights

    # Calculate light position based on spherical coordinates
    light_x = light_radius * math.sin(light_phi) * math.cos(light_theta)
    light_y = light_radius * math.sin(light_phi) * math.sin(light_theta)
    light_z = light_radius * math.cos(light_phi)

    # Normalize light vector
    light_magnitude = math.sqrt(light_x ** 2 + light_y ** 2 + light_z ** 2)
    light_x /= light_magnitude
    light_y /= light_magnitude
    light_z /= light_magnitude

    zbuffer = [-float('inf')] * (screen_width * screen_height)  # Z-buffer for depth sorting
    screen_pixels = [' '] * (screen_width * screen_height)  # Screen pixel buffer

    # Loop over spherical coordinates to generate each point
    for phi in range(0, 628, 7):  # phi angle (latitude) loop
        for theta in range(0, 628, 2):  # theta angle (longitude) loop
            phi_rad = phi / 100  # Convert phi to radians
            theta_rad = theta / 100  # Convert theta to radians

            # 3D coordinates of the point on the sphere
            x = radius * math.sin(phi_rad) * math.cos(theta_rad)
            y = radius * math.sin(phi_rad) * math.sin(theta_rad)
            z = radius * math.cos(phi_rad)

            # Apply rotation around Y-axis
            x_rot = x * math.cos(rotation_y) - z * math.sin(rotation_y)
            z_rot_y = x * math.sin(rotation_y) + z * math.cos(rotation_y)

            # Apply rotation around X-axis
            y_rot = y * math.cos(rotation_x) - z_rot_y * math.sin(rotation_x)
            z_rot = y * math.sin(rotation_x) + z_rot_y * math.cos(rotation_x)


            # Normalize the normal vector at the current point
            nx, ny, nz = x_rot / radius, y_rot / radius, z_rot / radius

            # Backface culling: discard points facing away from the viewer
            if nz > 0:
                # Diffuse lighting: dot product between normal and light direction
                dot_light_normal = max(0, nx * light_x + ny * light_y + nz * light_z)
                
                # Light attenuation for points behind the sphere
                attenuation = 1.0 if dot_light_normal > 0 else 0.2  
                diffuse = dot_light_normal * light_intensity * attenuation

                # Specular highlights: reflection of light
                reflection = max(0, 2 * dot_light_normal * nz - light_z)
                specular = (reflection ** specular_power) * light_intensity if dot_light_normal > 0 else 0

                # Total light intensity (ambient + diffuse + specular)
                light_intensity_final = ambient_light + diffuse + specular
                light_intensity_final = max(0, min(1, light_intensity_final))  # Clamp to [0, 1]
                luminance_index = int(light_intensity_final * (len(chars) - 1))  # Map to character index

                # Project the 3D point onto the 2D screen
                xp = int(screen_width / 2 + scale_x * x_rot)
                yp = int(screen_height / 2 - scale_y * y_rot)

                # Render the point if it is on the screen
                if 0 <= xp < screen_width and 0 <= yp < screen_height:
                    pixel_position = xp + screen_width * yp
                    if zbuffer[pixel_position] < z_rot:  # Ensure that the nearest point is drawn
                        zbuffer[pixel_position] = z_rot
                        screen_pixels[pixel_position] = chars[luminance_index]  # Assign character based on intensity

    # Return the 2D representation of the sphere
    return [''.join(screen_pixels[i * screen_width:(i + 1) * screen_width]) for i in range(screen_height)]

# Function to clear the terminal screen (works across platforms)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main function to control animation and rendering
def main():
    radius = 12  # Radius of the sphere
    rotation_speed_x = 0.05  # Speed of rotation around the X-axis
    rotation_speed_y = 0.03  # Speed of rotation around the Y-axis
    light_rotation_speed = 0.2  # Speed of light rotation

    scale_x = 2.0  # Horizontal scaling factor (for aspect ratio)
    scale_y = 1.0  # Vertical scaling factor (for aspect ratio)
    screen_width = 80  # Terminal screen width
    screen_height = 24  # Terminal screen height

    # Initial rotation angles for the sphere and light
    rotation_x = 0
    rotation_y = 0
    light_theta = 0
    light_phi = math.pi / 4  # Start at 45 degrees from the vertical

    light_radius = 3.0  # Distance of the light from the sphere
    light_intensity = 1.5  # Light intensity

    try:
        while True:
            start_time = time.time()  # Record the start time for FPS calculation

            # Update light rotation angles
            light_theta += light_rotation_speed
            light_phi += light_rotation_speed * 0.8

            # Generate the sphere and render it
            sphere = generate_sphere(radius, rotation_x, rotation_y, light_theta, light_phi, light_radius, light_intensity, screen_width, screen_height, scale_x, scale_y)
            clear_screen()  # Clear the screen before rendering
            for line in sphere:  # Print each line of the sphere to the terminal
                print(line)

            # Calculate and display FPS (frames per second)
            elapsed_time = time.time() - start_time
            fps = 1 / elapsed_time
            print(f"\nFPS: {fps:.2f}")

            # Update rotation angles for the next frame
            rotation_x += rotation_speed_x
            rotation_y += rotation_speed_y

            time.sleep(0.03)  # Control animation speed
    except KeyboardInterrupt:  # Graceful exit on keyboard interrupt
        print("\nAnimation stopped.")

# Start the program
if __name__ == "__main__":
    main()
