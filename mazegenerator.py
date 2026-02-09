import random


class MazeGenerator():
    def __init__(
        self, width: int,
            height: int, seed: int,
            exit=None, perfect: bool = True,
            entry: tuple[int, int] = (0, 0)):
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

    def _inject_42(self):
        """Sella el número 42 como un bloque sólido de paredes."""
        # Definimos el tamaño mínimo necesario (10x7 para el número + margen)
        min_w, min_h = 15, 10

        if self.width < min_w or self.height < min_h:
            print(
                f"Error: El tamaño del laberinto ({self.width}x{self.height})"
                f"es demasiado pequeño para el patrón '42'.")
            print("El patrón será omitido.")
            return

        off_x = (self.width - 10) // 2
        off_y = (self.height - 7) // 2

        # Coordenadas que forman el dibujo del "42"
        puntos = [
            # El 4
            (0, 0), (0, 1), (0, 2), (1, 2),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
            # El 2
            (5, 0), (6, 0), (7, 0), (7, 1),
            (7, 2), (6, 2), (5, 2), (5, 3), (5, 4), (6, 4), (7, 4)
        ]

        for dx, dy in puntos:
            nx, ny = off_x + dx, off_y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                # 15 = Todas las paredes cerradas (bloque sólido)
                self.grid[nx][ny] = 15
                # Lo marcamos como visitado para que el generador
                # y el solver lo ignoren
                self.visited[nx][ny] = True

    def generate_step(self) -> bool:
        """
        Ejecuta un único paso del algoritmo.
        Devuelve True si el laberinto sigue en construcción,
        False si ha terminado.
        """
        if not self.stack:
            return False

        cx, cy = self.stack[-1]
        neighbors = []

        # Direcciones: 1:N, 2:E, 4:S, 8:W
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

    def generate(self):
        """
        Generación instantánea

        :param self: Description
        """
        while self.generate_step():
            pass

    def solve(self):
        """Encuentra el camino desde entry hasta exit usando DFS."""
        stack = [(self.entry, "")]
        visited = set()

        while stack:
            (cx, cy), path = stack.pop()
            if (cx, cy) == self.exit:
                return path

            if (cx, cy) not in visited:
                visited.add((cx, cy))
            # Norte (1), Este (2), Sur (4), Oeste (8)
            moves = [
                (cx, cy - 1, 1, 'N'),
                (cx + 1, cy, 2, 'E'),
                (cx, cy + 1, 4, 'S'),
                (cx - 1, cy, 8, 'W')
            ]

            for nx, ny, bit, direction in moves:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Si NO hay pared en esa dirección (bit no activo)
                    if not (self.grid[cx][cy] & bit):
                        if (nx, ny) not in visited:
                            stack.append(((nx, ny), path + direction))
        return "NO_SOLUTION"

    def save(self, filename: str):
        """Exporta al formato oficial con la solución real calculada."""
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

    def regenerate(self):
        """Reinicia el estado y genera un laberinto
        nuevo con una semilla aleatoria."""
        self.seed = random.randint(0, 999999)  # Nueva semilla
        self._rng = random.Random(self.seed)
        # Reset de la estructura
        self.grid = [
            [15 for _ in range(self.height)] for _ in range(self.width)]
        self.visited = [
            [False for _ in range(self.height)] for _ in range(self.width)]
        self._inject_42()  # Aseguramos el sello del 42
        self.stack = [self.entry]
        self.generate()  # Ejecuta el algoritmo de nuevo

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
