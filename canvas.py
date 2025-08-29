import pygame
from collections import deque

pygame.init()
width, height = (600, 600)
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vector Drawing")

clock = pygame.time.Clock()
running = True

# Cursor
cursor = [width // 2, height // 2]

# Queue to store incoming vectors
vector_buffer = deque()

# Fill background once
window.fill((255, 255, 255))

# Example: add some vectors manually
vector_buffer.append((50, 0))   # move right
vector_buffer.append((0, 50))   # move down
vector_buffer.append((-50, 0))  # move left
vector_buffer.append((0, -50))  # move up


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If there’s something in the buffer, draw it
    if vector_buffer:
        dx, dy = vector_buffer.popleft()   # take one vector
        new_pos = [cursor[0] + dx, cursor[1] + dy]

        pygame.draw.line(window, (255, 0, 0), cursor, new_pos, 5)
        cursor = new_pos  # update position

    pygame.display.update()
    clock.tick(60)

pygame.quit()
