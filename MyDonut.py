import os
import time
from math import sin, cos

def main():
    a = 0  # Initial rotation angle around the X-axis
    b = 0  # Initial rotation angle around the Z-axis    
    screen_height = 24
    screen_width = 80

    clear_command = "cls" if os.name == "nt" else "clear"

    while True:
        start_time = time.time()  # Start FPS timing
        zbuffer = [0 for _ in range(screen_height * screen_width)]
        screen_pixels = [' ' for _ in range(screen_height * screen_width)]
        
        phi = 0
        while phi < 6.28:
            phi += 0.07
            theta = 0
            while theta < 6.28:
                theta += 0.02
                sinA = sin(a)
                cosA = cos(a)
                cosB = cos(b)
                sinB = sin(b)

                costheta = cos(theta)
                sintheta = sin(theta)
                cosphi = cos(phi)
                sinphi = sin(phi)

                circlex = 2 + costheta
                circley = sintheta

                x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
                y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
                z = cosA * circlex * sinphi + circley * sinA + 5
                z_inverse = 1 / z

                xp = int(40 + 30 * z_inverse * x)
                yp = int(12 - 15 * z_inverse * y)

                pixel_position = xp + screen_width * yp

                L = cosphi * costheta * sinB - cosA * sinphi * costheta - sinA * sintheta + cosB * (cosA * sintheta - sinphi * costheta * sinA)
                if L > 0 and 0 <= pixel_position < len(screen_pixels):
                    if z_inverse > zbuffer[pixel_position]:
                        zbuffer[pixel_position] = z_inverse
                        luminance_index = L * 8
                        screen_pixels[pixel_position] = '.,-~:;=!*#$@'[int(luminance_index)]
        
        os.system(clear_command)
        for index, char in enumerate(screen_pixels):
            if index % screen_width == 0:
                print()
            else:
                print(char, end='')

        a += 0.07
        b += 0.02

        # Calculate FPS
        elapsed_time = time.time() - start_time
        fps = 1 / elapsed_time
        print(f"\nFPS: {fps:.2f}")
        
        # Add a small delay to stabilize frame rate
        time.sleep(0.03)

if __name__ == "__main__":
    main()
