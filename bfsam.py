import random
import matplotlib.pyplot as plt

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

def solve_maze(maze, start, end):
    def is_valid(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

    def dfs(x, y, path, paths):
        if (x, y) == end:
            path.append((x, y))
            paths.append(list(path))
            path.pop()
            return

        if is_valid(x, y):
            maze[x][y] = 2  # Mark as visited
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(x + dx, y + dy, path + [(x, y)], paths)

            maze[x][y] = 0  # Mark as unvisited

    paths = []
    dfs(start[0], start[1], [], paths)

    if not paths:
        print("No path found!")
        return []

    return paths


def print_maze(maze):
    for row in maze:
        print(" ".join(["1" if cell == 1 else "0" if cell == 0 else "X" if cell == 4 else " " for cell in row]))

def plot_maze(maze, paths, start, end):
    plt.figure(figsize=(len(maze[0]) / 2, len(maze) / 2))

    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] == 1:
                plt.fill_between([y, y + 1], len(maze) - x, len(maze) - x - 1, color='black')
            elif maze[x][y] == 4:
                plt.fill_between([y, y + 1], len(maze) - x, len(maze) - x - 1, color='blue')
            else:
                # Use light grey color for empty cells
                plt.fill_between([y, y + 1], len(maze) - x, len(maze) - x - 1, color='lightgrey')

    # Represent the start and end states with different colors
    start_x, start_y = start
    end_x, end_y = end
    plt.fill_between([start_y, start_y + 1], len(maze) - start_x, len(maze) - start_x - 1, color='green')
    plt.fill_between([end_y, end_y + 1], len(maze) - end_x, len(maze) - end_x - 1, color='red')

    # Define a list of colors for paths
    path_colors = ['purple', 'orange', 'pink', 'cyan', 'magenta', 'lime', 'gold', 'blue', 'brown', 'teal']

    # Represent the paths as lines with different colors
    for i, path in enumerate(paths):
        x_values, y_values = zip(*path)
        color = path_colors[i % len(path_colors)]
        plt.plot([y + 0.5 for y in y_values], [len(maze) - x - 0.5 for x in x_values], color=color, linewidth=2)

    plt.xlim(0, len(maze[0]))
    plt.ylim(0, len(maze))
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    try:
        rows, cols = 10, 10
        maze, start, end = generate_maze(rows, cols)

        print("Maze:")
        print_maze(maze)

        paths = solve_maze(maze, start, end)

        if paths:
            print("Paths:")
            for i, path in enumerate(paths, start=1):
                print(f"Path {i}:")
                for x, y in path:
                    maze[x][y] = 4  # Mark the path in the maze
                    print(f"({x}, {y})->", end="")
                print(f"({end[0]}, {end[1]})")
                print("\n")
                # Reset path marks
                for x, y in path:
                    maze[x][y] = 0

        plot_maze(maze, paths, start, end)

    except ValueError as e:
        print(f"Error: {e}")