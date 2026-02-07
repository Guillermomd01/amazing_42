import random
import sys


class MazeGenerator():
    def __init__(self, width: int, height: int, seed: int, exit=None, perfect: bool = True, entry: tuple[int, int] = (0, 0)):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry
        self.exit = exit if exit is not None else (width - 1, height - 1)
        
        self._rng = random.Random(seed)
        
        self.grid = [[15 for _ in range(height)] for _ in range(width)]
        self.visited = [[False for _ in range(height)] for _ in range(width)]
        
        self.stack = [self.entry]
        self._pre_mark_42()

    def _pre_mark_42(self):
        """Marca el área central como visitada para que el algoritmo genere el laberinto alrededor."""
        if self.width <= 10 or self.height <= 8:
            return
        
        start_x = (self.width - 8) // 2
        start_y = (self.height - 6) // 2
        
        for dx in range(8):
            for dy in range(6):
                if 0 <= start_x + dx < self.width and 0 <= start_y + dy < self.height:
                    self.visited[start_x + dx][start_y + dy] = True

    def generate(self):
        while self.stack:
            curr_x, curr_y = self.stack[-1]
            self.visited[curr_x][curr_y] = True
            
            neighbours = []
            # 1: Norte, 2: Este, 4: Sur, 8: Oeste
            directions = [
                (curr_x, curr_y - 1, 1, 4),
                (curr_x + 1, curr_y, 2, 8),
                (curr_x, curr_y + 1, 4, 1),
                (curr_x - 1, curr_y, 8, 2)
            ]
            
            for nx, ny, bit, op_bit in directions:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.visited[nx][ny]:
                        neighbours.append((nx, ny, bit, op_bit))
            
            if neighbours:
                nx, ny, bit, op_bit = self._rng.choice(neighbours)
                self.grid[curr_x][curr_y] &= ~bit
                self.grid[nx][ny] &= ~op_bit
                self.visited[nx][ny] = True
                self.stack.append((nx, ny))
            else:
                self.stack.pop()

    def save(self, filename: str):
        """
        Exporta el laberinto al formato oficial requerido.
        """
        with open(filename, 'w') as f:
            # 1. Escribimos la matriz de paredes en hexadecimal
            for y in range(self.height):
                line = ""
                for x in range(self.width):
                    # Convertimos el valor (0-15) a hexadecimal en mayúsculas
                    line += hex(self.grid[x][y])[2:].upper()
                f.write(line + "\n")

            f.write("\n")

            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")

            # 4. El camino más corto (N, E, S, W)
            f.write("SOLVE_PATH_HERE\n")

    def display_numeric(self):
        """Muestra la matriz cruda de bits en hexadecimal."""
        print("\n--- [DIAGNÓSTICO: MATRIZ DE BITS] ---")
        for y in range(self.height):
            for x in range(self.width):
                print(f"{self.grid[x][y]:X}", end=" ")
            print()

    def display_ascii(self):
        """Representación visual del laberinto en la terminal."""
        print("\n--- [VISTA PREVIA DEL PRODUCTO] ---")
        print("#" * (self.width * 2 + 1))

        for y in range(self.height):
            line = "#"
            for x in range(self.width):
                wall_bottom = "_" if self.grid[x][y] & 4 else " "

                wall_right = "|" if self.grid[x][y] & 2 else " "

                line += wall_bottom + wall_right
            print(line)
