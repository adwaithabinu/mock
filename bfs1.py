import random
from collections import deque

# Constants for maze cells
WALL = 0
EMPTY = 1
VISITED = 2
PATH = 3

# Maze dimensions
MAZE_SIZE = 10

# Generate an empty maze
def generate_empty_maze(size):
    return [[EMPTY] * size for _ in range(size)]

# Maze generation using randomized Prim's algorithm
def generate_maze(size):
    maze = generate_empty_maze(size)

    def is_valid(x, y):
        return 0 <= x < size and 0 <= y < size

    def add_walls(x, y):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny) and maze[nx][ny] == EMPTY:
                maze[nx][ny] = WALL
                maze[x + dx // 2][y + dy // 2] = WALL
                add_walls(nx, ny)

    # Start generating walls from a random point
    start_x, start_y = random.randint(0, size - 1), random.randint(0, size - 1)
    maze[start_x][start_y] = WALL
    add_walls(start_x, start_y)

    return maze

# Breadth-First Search to find all paths
def find_paths(maze):
    start = (0, 0)
    end = (MAZE_SIZE - 1, MAZE_SIZE - 1)
    queue = deque([([start], start)])

    paths = []
    while queue:
        path, (x, y) = queue.popleft()

        if (x, y) == end:
            paths.append(path)
        else:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE and maze[nx][ny] == EMPTY:
                    maze[nx][ny] = VISITED
                    new_path = path + [(nx, ny)]
                    queue.append((new_path, (nx, ny)))

    return paths

# Main function
if __name__ == "_main_":
    maze = generate_maze(MAZE_SIZE)
    paths = find_paths(maze)

    if not paths:
        print("No path found from start to end.")
    else:
        for i, path in enumerate(paths):
            print(f"Path {i + 1}: {path}")