import random
from typing import Optional
from collections import deque

class MazeGenerator():
    def __init__(
        self, width: int,
            height: int,
            exit: tuple[int, int],
            perfect: bool = True,
            entry: tuple[int, int] = (0, 0),
            seed: Optional[int] = None):
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
        """Sella el número 42 buscando una
        ubicación que no pise la entrada/salida."""
        # Tamaño mínimo para que el dibujo quepa con margen
        min_w, min_h = 15, 10
        if self.width < min_w or self.height < min_h:
            print(
                f"Error: Tamaño {self.width}x{self.height} "
                f"insuficiente para el '42'.")
            return

        # Coordenadas relativas que forman el dibujo del "42"
        puntos_relativos = [
            # El 4
            (0, 0), (0, 1), (0, 2), (1, 2),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
            # El 2
            (5, 0), (6, 0), (7, 0), (7, 1),
            (7, 2), (6, 2), (5, 2), (5, 3), (5, 4), (6, 4), (7, 4)
        ]

        # Calculamos el centro ideal
        base_x = (self.width - 10) // 2
        base_y = (self.height - 7) // 2

        # Lista de candidatos a "offset"
        candidatos = [
            (base_x, base_y),
            (base_x + 1, base_y),
            (base_x - 1, base_y),
            (base_x, base_y + 1),
            (base_x, base_y - 1),
            (base_x + 2, base_y),
            (base_x - 2, base_y)
        ]

        offset_elegido = None

        # Buscamos el primer candidato que no choque con entrada ni salida
        for off_x, off_y in candidatos:
            choque = False
            for dx, dy in puntos_relativos:
                nx, ny = off_x + dx, off_y + dy
                if (nx, ny) == self.entry or (nx, ny) == self.exit:
                    choque = True
                    break

            if not choque:
                offset_elegido = (off_x, off_y)
                break

        # Si encontramos un sitio, "quemamos" el 42 en el mapa
        if offset_elegido:
            off_x, off_y = offset_elegido
            for dx, dy in puntos_relativos:
                nx, ny = off_x + dx, off_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # 15 en decimal es 'F' en hex (todas las paredes)
                    self.grid[nx][ny] = 15
                    # MUY IMPORTANTE: Marcar como visitado para que el
                    # generador no pase por aquí y lo borre
                    self.visited[nx][ny] = True
            print(
                f"Patrón '42' inyectado con éxito en offset {offset_elegido}.")
        else:
            print("No se encontró una posición libre para el patrón '42'.")

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
        if not self.perfect:
            self.add_paths()

    def add_paths(self):
        """
        Rompe algunos muros al azar para crear varios caminos.
        """
        for _ in range(10):
            x = self._rng.randint(1, self.width - 2)
            y = self._rng.randint(1, self.height - 2)

        # Si el muro Este está cerrado (valor 2), lo abrimos
        if self.grid[x][y] & 2:
            self.grid[x][y] &= ~2      # Quita muro este de la celda actual
            self.grid[x+1][y] &= ~8    # Quita muro oeste de la celda de al lado

    def solve(self):
        """Encuentra el camino más CORTO desde entry hasta exit usando BFS."""
        # Usamos una cola (deque) para BFS: (posición_actual, camino_recorrido)
        queue = deque([(self.entry, "")])
        visited = {self.entry}

        while queue:
            (cx, cy), path = queue.popleft()

            if (cx, cy) == self.exit:
                return path

            # Direcciones: Norte(1), Este(2), Sur(4), Oeste(8)
            moves = [
                (cx, cy - 1, 1, 'N'),
                (cx + 1, cy, 2, 'E'),
                (cx, cy + 1, 4, 'S'),
                (cx - 1, cy, 8, 'W')
            ]

            for nx, ny, bit, direction in moves:
                # 1. Verificar límites del tablero
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # 2. Verificar si NO hay muro en esa dirección
                    if not (self.grid[cx][cy] & bit):
                        # 3. Si no ha sido visitado, es un candidato para el camino más corto
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append(((nx, ny), path + direction))
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
        self.seed = random.randint(0, 999999)
        self._rng = random.Random(self.seed)
        # Reset de la estructura
        self.grid = [
            [15 for _ in range(self.height)] for _ in range(self.width)]
        self.visited = [
            [False for _ in range(self.height)] for _ in range(self.width)]
        self._inject_42()
        self.stack = [self.entry]
        self.visited[self.entry[0]][self.entry[1]] = True

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
