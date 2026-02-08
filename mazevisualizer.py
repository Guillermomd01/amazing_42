import sys

try:
    from mlx.mlx import Mlx
except ImportError:
    print("Error importing mlx")
    sys.exit(1)

import random


class MazeVisualizer():
    def __init__(self, maze, tile_size=30):
        self.maze = maze
        self.tile_size = tile_size
        self.show_solution = False

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        if not self.mlx_ptr:
            print(
                "Error: No se pudo conectar con el servidor gráfico"
                "(MLX_INIT falló)")
            sys.exit(1)
        self.win_w = self.maze.width * self.tile_size
        self.win_h = self.maze.height * self.tile_size
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "Amazeing - 42 project")

        self.wall_color = 0xFFFFFF
        self.entry_color = 0x00FF00
        self.exit_color = 0xFF0000
        self.solu_color = 0x00FFFF

    def _draw_line(self, x1, y1, x2, y2, color):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if x1 == x2:  # Línea vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr, x1, y, color)
        elif y1 == y2:  # Línea horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr, x, y1, color)

    def draw_path(self):
        "Dibuja la solución"
        path = self.maze.solve()
        if path == "NO_SOLUTION":
            return

        cx, cy = self.maze.entry
        tile_size = self.tile_size

        for move in path:
            start_x = cx * tile_size + tile_size // 2
            start_y = cy * tile_size + tile_size // 2
            if move == 'N':
                cy -= 1
            elif move == 'S':
                cy += 1
            elif move == 'E':
                cx += 1
            elif move == 'W':
                cy -= 1
            end_x = cx * tile_size + tile_size // 2
            end_y = cy * tile_size + tile_size // 2
            self._draw_line(start_x, start_y, end_x, end_y, self.solu_color)

    def render(self):
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                px = x * self.tile_size
                py = y * self.tile_size
                cell_value = self.maze.grid[x][y]
                if cell_value & 1:
                    self._draw_line(
                        px, py, px + self.tile_size, py, self.wall_color)
                if cell_value & 2:
                    self._draw_line(
                        px + self.tile_size, py, px + self.tile_size,
                        py + self.tile_size, self.wall_color)
                if cell_value & 4:
                    self._draw_line(
                        px, py + self.tile_size, px + self.tile_size,
                        py + self.tile_size, self.wall_color)
                if cell_value & 8:
                    self._draw_line(
                        px, py, px, py + self.tile_size, self.wall_color)
        if self.show_solution:
            self.draw_path()

    def change_wall_color(self) -> None:
        """
        Cambair el color de las paredes aleatoriamente

        :param self: Description
        """
        colors = [
            0xFF8C00,
            0x8A2BE2,
            0xFF00FF,
            0xFFD700,
            0x1E90FF,
            0xFF69B4,
            0x32CD32,
            0x4B0082,
            0x7FFF00,
            0x0000FF
        ]
        wall = random.choice(colors)
        while wall == self.wall_color:
            wall = random.choice(colors)
        self.wall_color = wall
        self.render()
        if self.show_solution:
            self.show_solution = False
            self.draw_path()

    def handle_keys(self, keycode, param=None):
        """
        Registra los movimientos por teclado y actua en consecuencia

        :param self: Description
        :param keycode: Description
        :param param: Description
        """
        # ESC: Salir
        if keycode == 53 or keycode == 65307:
            sys.exit(0)
        # S: show solution
        elif keycode == 115:
            self.show_solution = not self.show_solution
            self.render()
        # R: Regenerate maze
        elif keycode == 114:
            print("Regenerating maze...")
            self.maze.regenerate()
            self.render()
        # C: cambiar color de walls
        elif keycode == 99:
            self.change_wall_color()
        return 0

    def run(self):
        self.mlx.mlx_key_hook(self.win_ptr, self.handle_keys, None)
        self.render()
        self.mlx.mlx_loop(self.mlx_ptr)
