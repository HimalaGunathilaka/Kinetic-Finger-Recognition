import pygame
import math
import sys
import serial 
import serial.tools.list_ports

class RotatingCircle:
    def __init__(self, screen, center, radius, angular_speed=0.0, color=(255,0,0)):
        self.screen = screen
        self.center = center
        self.radius = radius
        self.angular_speed = angular_speed
        self.color = color
        self.angle = 0
    
    def update(self):
        self.angle += self.angular_speed
    
    def draw(self):
        # Draw circle outline
        pygame.draw.circle(self.screen, (255, 255, 255), self.center, self.radius, 1)
        
        # Draw 4 rotating points
        for i in range(4):
            theta = self.angle + i * (math.pi / 2)
            x = self.center[0] + self.radius * math.cos(theta)
            y = self.center[1] + self.radius * math.sin(theta)
            pygame.draw.circle(self.screen, self.color, (int(x), int(y)), 8)


# ---------------- MAIN ----------------
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MPU6050 Controlled Rotation")

clock = pygame.time.Clock()

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:
            return port.device
    return None

esp32_port = find_esp32_port()
if esp32_port is None:
    print("⚠️ ESP32 not found. Please connect it.")
    sys.exit()

ser = serial.Serial(esp32_port, 115200, timeout=0.1)

circle = RotatingCircle(screen, (WIDTH//2, HEIGHT//2), 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ser.close()
            sys.exit()
    
    # Read gyro z-axis from serial
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode().strip()
            gx, gy, gz = map(float, line.split(","))
            # use z axis as angular speed (scaled down)
            circle.angular_speed = gz * 0.05   # scale factor to make it smooth
            print(gz)
        except:
            pass  # skip bad lines

    screen.fill((0, 0, 0))
    
    circle.update()
    circle.draw()

    pygame.display.flip()
    clock.tick(60)
