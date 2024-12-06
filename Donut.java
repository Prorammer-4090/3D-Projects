public class Donut {
    public static void main(String[] args) {
        double a = 0;
        double b = 0;
        int screenHeight = 24;
        int screenWidth = 80;
        int R1 = 1;
        int R2 = 2;
        int K2 = 5;
        String chars = ".,-~:;=!*#$@";

        while (true) {
            long startTime = System.currentTimeMillis();  // Start FPS timing
            System.out.print("\033[H");  // Move cursor to top left
            System.out.flush();
            
            double[] zBuffer = new double[screenHeight * screenWidth];
            char[] screenPixels = new char[screenHeight * screenWidth];
            
            for (int i = 0; i < screenPixels.length; i++) {
                screenPixels[i] = ' ';
                zBuffer[i] = 0;
            }

            for (double phi = 0; phi < Math.PI * 2; phi += 0.07) {
                for (double theta = 0; theta < Math.PI * 2; theta += 0.02) {
                    double sinA = Math.sin(a), cosA = Math.cos(a);
                    double sinB = Math.sin(b), cosB = Math.cos(b);
                    double cosTheta = Math.cos(theta), sinTheta = Math.sin(theta);
                    double cosPhi = Math.cos(phi), sinPhi = Math.sin(phi);

                    double circleX = R2 + R1 * cosTheta;
                    double circleY = R1 * sinTheta;

                    double x = circleX * (cosB * cosPhi + sinA * sinB * sinPhi) - circleY * cosA * sinB;
                    double y = circleX * (sinB * cosPhi - sinA * cosB * sinPhi) + circleY * cosA * cosB;
                    double z = cosA * circleX * sinPhi + circleY * sinA + K2;
                    double zInverse = 1 / z;

                    int xp = (int) (screenWidth / 2 + 30 * x * zInverse);
                    int yp = (int) (screenHeight / 2 - 15 * y * zInverse);
                    int pixelPosition = xp + screenWidth * yp;

                    double N = cosPhi * cosTheta * sinB - cosA * sinPhi * cosTheta - sinA * sinTheta + cosB * (cosA * sinTheta - sinPhi * cosTheta * sinA);
                    if (pixelPosition >= 0 && pixelPosition < screenHeight * screenWidth && zInverse > zBuffer[pixelPosition] && N > 0) {
                        zBuffer[pixelPosition] = zInverse;
                        int luminanceIndex = (int) (N * 8);
                        screenPixels[pixelPosition] = chars.charAt(Math.max(0, Math.min(luminanceIndex, chars.length() - 1)));
                    }
                }
            }

            StringBuilder output = new StringBuilder();
            output.append("\033[38;2;0;255;0m");  // Set green color
            for (int i = 0; i < screenPixels.length; i++) {
                if (i % screenWidth == 0) output.append("\n");
                output.append(screenPixels[i]);
            }
            output.append("\033[0m");  // Reset color
            
            // Append FPS counter at the bottom
            long elapsedTime = System.currentTimeMillis() - startTime;
            double fps = 1000.0 / elapsedTime;
            output.append(String.format("\n\033[38;2;0;255;0mFPS: %.2f\033[0m", fps));
            
            System.out.print(output);

            a += 0.07;
            b += 0.02;

            // Add frame delay to control animation speed
            try {
                Thread.sleep(30);  // 30 milliseconds
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
