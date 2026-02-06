import random
import numpy as np


class MazeGenerator():
    def __init__(
        self, width: int, height: int, seed: int,
            exit=None,
            perfect: bool = True,
            entry: tuple[int, int] = (0, 0)):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry
        if exit is None:
            self.exit = (width - 1, height - 1)
        else:
            self.exit = exit
        self._rng = random.Random(seed)
        self.grid = np.full((self.width, self.height), 15)
        self.visited = np.full((self.width, self.height), False)
        self.stack = [self.entry]

        if self.width <= 8 or self.height <= 4:
            return
        form_4 = [
            (0, 4), (0, 3), (0, 2),
            (0, 2), (1, 2), (2, 2),
            (2, 4), (2, 3), (2, 2), (2, 0)]
        form_2 = [
            (0, 4), (1, 4), (2, 4),
            (2, 4), (2, 3), (2, 2),
            (2, 2), (1, 2), (0, 2),
            (0, 2), (0, 1), (0, 0),
            (0, 0), (1, 0), (2, 0)
        ]
        start_x = (self.width - 8) // 2
        start_y = (self.height - 4) // 2
        for x, y in form_4:
            x_real = start_x + x
            y_real = start_y + y
            self.visited[x_real][y_real] = True
        for x, y in form_2:
            x_real = start_x + 4 + x
            y_real = start_y + 4 + y
            self.visited[x_real][y_real] = True

    def generate(self):
        while self.stack:
            curr_x, curr_y = self.stack[-1]
            neighbour_validate = []
            candidates_neighbour = [
                ((curr_x, curr_y - 1), 1),
                ((curr_x + 1, curr_y), 2),
                ((curr_x, curr_y + 1), 4),
                ((curr_x - 1, curr_y), 8)
            ]
            for (x, y), n in candidates_neighbour:
                if 0 <= x < self.width and 0 <= y < self.height:
                    if not self.visited[x][y]:
                        neighbour_validate.append(((x, y), n))
            if neighbour_validate:
                opossite_walls = {
                    1: 4,
                    2: 8,
                    4: 1,
                    8: 2
                }
                (x, y), bit = self._rng.choice(neighbour_validate)
                op_bit = opossite_walls[bit]
                self.grid[curr_x][curr_y] &= ~bit
                self.grid[x][y] &= ~op_bit
                self.visited[x][y] = True
                self.stack.append((x, y))
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

            # 2. El manual exige una línea vacía antes de los metadatos
            f.write("\n")

            # 3. Coordenadas de entrada y salida [cite: 149]
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")

            # 4. El camino más corto (N, E, S, W)
            f.write("SOLVE_PATH_HERE\n")

    def display_numeric(self):
        """Muestra la matriz cruda de bits en hexadecimal."""
        print("\n--- [DIAGNÓSTICO: MATRIZ DE BITS] ---")
        for y in range(self.height):
            for x in range(self.width):
                # Formateamos a un dígito hexadecimal en mayúsculas
                print(f"{self.grid[x][y]:X}", end=" ")
            print()

    def display_ascii(self):
        """Representación visual del laberinto en la terminal."""
        print("\n--- [VISTA PREVIA DEL PRODUCTO] ---")
        # Techo del laberinto
        print("#" * (self.width * 2 + 1))

        for y in range(self.height):
            line = "#"
            for x in range(self.width):
                # Si el bit del SUR (4) está activo, hay una pared abajo
                wall_bottom = "_" if self.grid[x][y] & 4 else " "

                # Si el bit del ESTE (2) está activo, hay una pared
                # a la derecha
                wall_right = "|" if self.grid[x][y] & 2 else " "

                line += wall_bottom + wall_right
            print(line)
