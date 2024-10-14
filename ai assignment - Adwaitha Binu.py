import random
import matplotlib.pyplot as plt
from collections import deque

def generate_maze(rows, cols):
    if rows < 3 or cols < 3:
        raise ValueError("Maze dimensions must be at least 3x3.")

    maze = [[1] * cols for _ in range(rows)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def get_neighbors(x, y):
        neighbors = [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]
        random.shuffle(neighbors)
        return [(nx, ny) for nx, ny in neighbors if is_valid(nx, ny)]

    def remove_wall_between(x1, y1, x2, y2):
        maze[(x1 + x2) // 2][(y1 + y2) // 2] = 0

    for x in range(0, cols, 2):
        maze[0][x] = 0

    start = (0, 1)
    end = (rows - 1, cols - 2)

    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0

    stack = [start]

    while stack:
        current_x, current_y = stack[-1]
        neighbors = get_neighbors(current_x, current_y)
        unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if is_valid(nx, ny) and maze[nx][ny] == 1]

        if unvisited_neighbors:
            next_x, next_y = unvisited_neighbors[0]
            remove_wall_between(current_x, current_y, next_x, next_y)
            maze[next_x][next_y] = 0
            stack.append((next_x, next_y))
        else:
            stack.pop()

    return maze, start, end

def bfs(maze, start, end):
    def is_valid(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

    queue = deque([(start, [start])])

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                maze[new_x][new_y] = 2  # Mark as visited
                new_path = path + [(new_x, new_y)]
                queue.append(((new_x, new_y), new_path))

    return None

def print_maze(maze):
    for row in maze:
        print(" ".join(["1" if cell == 1 else "0" if cell == 0 else "X" if cell == 4 else " " for cell in row]))

def plot_maze(maze, path, start, end):
    plt.figure(figsize=(len(maze[0]) / 2, len(maze) / 2))

    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] == 1:
                plt.fill_between([y, y + 1], len(maze) - x, len(maze) - x - 1, color='black')
            elif maze[x][y] == 4:
                plt.fill_between([y, y + 1], len(maze) - x, len(maze) - x - 1, color='blue')
            else:
                plt.fill_between([y, y + 1], len(maze) - x, len(maze) - x - 1, color='lightgrey')

    start_x, start_y = start
    end_x, end_y = end
    plt.fill_between([start_y, start_y + 1], len(maze) - start_x, len(maze) - start_x - 1, color='green')
    plt.fill_between([end_y, end_y + 1], len(maze) - end_x, len(maze) - end_x - 1, color='red')

    for x, y in path:
        plt.fill_between([y, y + 1], len(maze) - x, len(maze) - x - 1, color='blue')

    plt.xlim(0, len(maze[0]))
    plt.ylim(0, len(maze))
    #plt.gca().invert_yaxis()
    plt.axis('off')
    plt.show()

try:
    rows, cols = 10, 10
    maze, start, end = generate_maze(rows, cols)

    print("Maze:")
    print_maze(maze)

    path = bfs(maze, start, end)

    if path:
        print("Path:")
        print(path)

        for x, y in path:
            maze[x][y] = 4

        plot_maze(maze, path, start, end)

except ValueError as e:
    print(f"Error: {e}")