import math
import time

screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.02
illumination = ".,-~:;=!*#$@"

A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))

def render_frame(A, B):
    cos_A, sin_A = math.cos(A), math.sin(A)
    cos_B, sin_B = math.cos(B), math.sin(B)

    output = [[" " for _ in range(screen_size)] for _ in range(screen_size)]
    zbuffer = [[0 for _ in range(screen_size)] for _ in range(screen_size)]

    for phi in range(0, int(2 * math.pi / phi_spacing)):
        cos_phi = math.cos(phi * phi_spacing)
        sin_phi = math.sin(phi * phi_spacing)
        
        for theta in range(0, int(2 * math.pi / theta_spacing)):
            cos_theta = math.cos(theta * theta_spacing)
            sin_theta = math.sin(theta * theta_spacing)

            circle_x = R2 + R1 * cos_theta
            circle_y = R1 * sin_theta

            x = (cos_B * cos_phi + sin_A * sin_B * sin_phi) * circle_x - cos_A * sin_B * circle_y
            y = (sin_B * cos_phi - sin_A * cos_B * sin_phi) * circle_x + cos_A * cos_B * circle_y
            z = K2 + cos_A * sin_phi * circle_x + sin_A * circle_y

            ooz = 1 / z if z != 0 else 0
            xp = int(screen_size / 2 + K1 * ooz * x)
            yp = int(screen_size / 2 - K1 * ooz * y)

            L = cos_phi * cos_theta * sin_B - cos_A * sin_phi * cos_theta - sin_A * sin_theta + cos_B * (cos_A * sin_theta - sin_phi * cos_theta * sin_A)

            if L > 0:
                L_index = int(round(L * 8))
                if L_index >= 0 and L_index < len(illumination):
                    if ooz > zbuffer[xp][yp]:
                        zbuffer[xp][yp] = ooz
                        output[xp][yp] = illumination[L_index]

    return output

def pprint(array):
    """Pretty print the frame."""
    for row in array:
        print("".join(row))

if __name__ == "__main__":
    while True:
        A += theta_spacing
        B += phi_spacing
        print("\x1b[H")
        pprint(render_frame(A, B))
        time.sleep(0.03)  # Add a small delay to make the animation smoother