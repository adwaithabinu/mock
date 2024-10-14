import pygame
import random
from collections import deque

# Define maze dimensions
WIDTH, HEIGHT = 10, 10

# Define cell types
EMPTY = 0
BLOCKED = 1
START = 2
END = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED= (255, 0, 0)

# Create a maze grid
maze = [[EMPTY] * WIDTH for _ in range(HEIGHT)]

# Define start and end points
start = (1, 1)
end = (WIDTH - 1, HEIGHT - 1)

# Generate the maze using Prim's algorithm
def generate_maze():
    # Initialize the maze with blocked cells
    for y in range(HEIGHT):
        for x in range(WIDTH):
            maze[y][x] = BLOCKED

    # Initialize variables
    stack = [(1, 1)]
    maze[1][1] = EMPTY

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < WIDTH and 0 < ny < HEIGHT and maze[ny][nx] == BLOCKED:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            mx, my = (nx + x) // 2, (ny + y) // 2
            maze[my][mx] = EMPTY
            maze[ny][nx] = EMPTY
            stack.append((nx, ny))
        else:
            stack.pop()

generate_maze()
maze[start[1]][start[0]] = START
maze[end[1]][end[0]] = END

# Initialize Pygame
pygame.init()
SCREEN_SIZE = (WIDTH * 50, HEIGHT * 50)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Maze Solver")

# Breadth-First Search to find paths
def bfs(maze, start, end):
    queue = deque([start])
    came_from = {}
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = came_from[(x, y)]
            path.append(start)
            path.reverse()
            return path
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and maze[ny][nx] == EMPTY and (nx, ny) not in came_from:
                queue.append((nx, ny))
                came_from[(nx, ny)] = (x, y)
    
    return []

# Find and print the path
path = bfs(maze, start, end)

if path:
    for x, y in path:
        maze[x][y] = GREEN

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the maze
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if maze[y][x] == BLOCKED:
                pygame.draw.rect(screen, BLACK, (x * 50, y * 50, 50, 50))
            elif maze[y][x] == START or maze[y][x] == END:
                pygame.draw.rect(screen, RED, (x * 50, y * 50, 50, 50))
            elif maze[y][x] == GREEN:
                 pygame.draw.rect(screen, GREEN, (x * 50, y * 50, 50, 50))
            else:
                pygame.draw.rect(screen, WHITE, (x * 50, y * 50, 50, 50))

    pygame.display.flip()


# Wait for user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
