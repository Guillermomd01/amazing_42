import random
from typing import Optional
from collections import deque


class MazeGenerator():
    """
    Generates and solves mazes using a randomized backtracking algorithm.
    """

    def __init__(
            self, width: int,
            height: int,
            exit: tuple[int, int],
            perfect: bool = True,
            entry: tuple[int, int] = (0, 0),
            seed: Optional[int] = None):
        """Initialize the maze dimensions, entry/exit points, and grid."""
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry
        self.exit = exit if exit is not None else (width - 1, height - 1)

        self._rng = random.Random(seed)

        self.grid = [[15 for _ in range(height)] for _ in range(width)]
        self.visited = [[False for _ in range(height)] for _ in range(width)]

        self._inject_42()
        self.stack = [self.entry]

    def _inject_42(self) -> None:
        """Injects a static '42' pattern into the grid."""
        min_w, min_h = 15, 10
        if self.width < min_w or self.height < min_h:
            print(
                f"Error: Size {self.width}x{self.height} "
                "is insufficient for '42' pattern.")
            return

        rel_points = [
            # 4
            (0, 0), (0, 1), (0, 2), (1, 2),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
            # 2
            (5, 0), (6, 0), (7, 0), (7, 1),
            (7, 2), (6, 2), (5, 2), (5, 3), (5, 4), (6, 4), (7, 4)
        ]

        base_x = (self.width - 10) // 2
        base_y = (self.height - 7) // 2

        candidates = [
            (base_x, base_y),
            (base_x + 1, base_y),
            (base_x - 1, base_y),
            (base_x, base_y + 1),
            (base_x, base_y - 1),
            (base_x + 2, base_y),
            (base_x - 2, base_y)
        ]

        chosen_offset = None

        for off_x, off_y in candidates:
            collision = False
            for dx, dy in rel_points:
                nx, ny = off_x + dx, off_y + dy
                if (nx, ny) == self.entry or (nx, ny) == self.exit:
                    collision = True
                    break
            if not collision:
                chosen_offset = (off_x, off_y)
                break

        if chosen_offset:
            off_x, off_y = chosen_offset
            for dx, dy in rel_points:
                nx, ny = off_x + dx, off_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.grid[nx][ny] = 15
                    self.visited[nx][ny] = True
            msg = (f"'42' pattern injected successfully "
                   f"at {chosen_offset}.")
            print(msg)
        else:
            print("Could not find a free position for '42' pattern.")

    def generate_step(self) -> bool:
        """Processes a single step of the maze generation algorithm."""
        if not self.stack:
            return False

        cx, cy = self.stack[-1]
        neighbors = []

        directions = [
            (0, -1, 1, 4),
            (1, 0, 2, 8),
            (0, 1, 4, 1),
            (-1, 0, 8, 2)]

        for dx, dy, bit, opp in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[nx][ny]:
                    neighbors.append((nx, ny, bit, opp))

        if neighbors:
            nx, ny, bit, opp = self._rng.choice(neighbors)
            self.grid[cx][cy] &= ~bit
            self.grid[nx][ny] &= ~opp
            self.visited[nx][ny] = True
            self.stack.append((nx, ny))
        else:
            self.stack.pop()

        return True

    def generate(self) -> None:
        """Generates the entire maze instantly."""
        while self.generate_step():
            pass
        if not self.perfect:
            self.add_paths()

    def add_paths(self) -> None:
        """Breaks random walls to create multiple paths in the maze."""
        for _ in range(10):
            x = self._rng.randint(1, self.width - 2)
            y = self._rng.randint(1, self.height - 2)

        if self.grid[x][y] & 2:
            self.grid[x][y] &= ~2
            self.grid[x + 1][y] &= ~8

    def solve(self) -> str:
        """Finds the shortest path from entry to exit using BFS."""
        queue = deque([(self.entry, "")])
        visited = {self.entry}

        while queue:
            (cx, cy), path = queue.popleft()

            if (cx, cy) == self.exit:
                return path

            moves = [
                (cx, cy - 1, 1, 'N'),
                (cx + 1, cy, 2, 'E'),
                (cx, cy + 1, 4, 'S'),
                (cx - 1, cy, 8, 'W')
            ]

            for nx, ny, bit, direction in moves:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (self.grid[cx][cy] & bit):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append(((nx, ny), path + direction))
        return "NO_SOLUTION"

    def save(self, filename: str) -> None:
        """Saves the maze layout and its solution to a file."""
        solution = self.solve()
        with open(filename, 'w') as f:
            for y in range(self.height):
                line = "".join(
                    hex(self.grid[x][y])[2:].upper() for x in range(self.width)
                )
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            f.write(f"{solution}\n")

    def regenerate(self) -> None:
        """Resets the grid and generates a new random maze."""
        self.seed = random.randint(0, 999999)
        self._rng = random.Random(self.seed)
        self.grid = [
            [15 for _ in range(self.height)] for _ in range(self.width)]
        self.visited = [
            [False for _ in range(self.height)] for _ in range(self.width)]
        self._inject_42()
        self.stack = [self.entry]
        self.visited[self.entry[0]][self.entry[1]] = True

    def display_ascii(self) -> None:
        """Prints an ASCII representation of the maze in the console."""
        print("#" * (self.width * 2 + 1))

        for y in range(self.height):
            line = "#"
            for x in range(self.width):
                wall_bottom = "_" if self.grid[x][y] & 4 else " "
                wall_right = "|" if self.grid[x][y] & 2 else " "
                line += wall_bottom + wall_right
            print(line)
