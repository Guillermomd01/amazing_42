import os
import sys
try:
    from mlx.mlx import Mlx
except ImportError:
    sys.exit(1)


class MazeVisualizer():
    def __init__(self, maze, tile_size=25):
        self.maze = maze
        self.tile_size = tile_size
        self.solution_path = ""

        # Generamos el laberinto ANTES de mostrar nada
        self.maze.generate()

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_w = self.maze.width * self.tile_size
        self.win_h = self.maze.height * self.tile_size
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "Amazeing Premium v2")

        self.img = self.mlx.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)
        raw_data = self.mlx.mlx_get_data_addr(self.img)
        self.img_data, self.bpp, self.size_line, self.endian = raw_data

        self.wall_color = 0xFFFFFF  # Paredes blancas
        self.start_color = 0x00FF00  # Verde (Inicio)
        self.exit_color = 0xFF0000  # Rojo (Salida)
        self.solu_color = 0x00FFFF  # Cian (Camino de solución)

        self.render()

    def _put_pixel(self, x, y, color):
        if 0 <= x < self.win_w and 0 <= y < self.win_h:
            offset = (y * self.size_line) + (x * (self.bpp // 8))
            self.img_data[offset] = color & 0xFF
            self.img_data[offset + 1] = (color >> 8) & 0xFF
            self.img_data[offset + 2] = (color >> 16) & 0xFF
            self.img_data[offset + 3] = 0xFF

    def _fill_cell(self, x, y, color):
        """Rellena el interior de una celda con un color."""
        px, py = x * self.tile_size, y * self.tile_size
        # Dejamos un margen de 2 píxeles para no tapar las paredes
        for i in range(2, self.tile_size - 2):
            for j in range(2, self.tile_size - 2):
                self._put_pixel(px + i, py + j, color)

    def render(self):
        # Limpiar fondo
        for i in range(len(self.img_data)):
            self.img_data[i] = 0

        # Dibujar puntos de Inicio y Fin
        self._fill_cell(
            self.maze.entry[0], self.maze.entry[1], self.start_color)
        self._fill_cell(
            self.maze.exit[0], self.maze.exit[1], self.exit_color)

        # Dibujar Paredes
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                px, py = x * self.tile_size, y * self.tile_size
                val = self.maze.grid[x][y]
                if val & 1:  # N
                    for i in range(self.tile_size):
                        self._put_pixel(
                            px + i, py, self.wall_color)
                if val & 2:  # E
                    for i in range(self.tile_size):
                        self._put_pixel(
                            px + self.tile_size - 1, py + i, self.wall_color)
                if val & 4:  # S
                    for i in range(self.tile_size):
                        self._put_pixel(
                            px + i, py + self.tile_size - 1, self.wall_color)
                if val & 8:  # W
                    for i in range(self.tile_size):
                        self._put_pixel(px, py + i, self.wall_color)

        # Dibujar Solución si existe
        if self.solution_path:
            self._draw_solution()

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img, 0, 0)

    def _draw_solution(self):
        cx, cy = self.maze.entry
        center = self.tile_size // 2
        for move in self.solution_path:
            px, py = cx * self.tile_size + center, cy * self.tile_size + center
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    self._put_pixel(px + dx, py + dy, self.solu_color)
            if move == 'N':
                cy -= 1
            elif move == 'E':
                cx += 1
            elif move == 'S':
                cy += 1
            elif move == 'W':
                cx -= 1

    def handle_keys(self, keycode, *args):
        # ESC para salir
        if keycode in [53, 65307]:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            os._exit(0)

        # 'S' para Solución (keycode 115 o 1)
        elif keycode in [115, 1, 83]:
            self.solution_path = self.maze.solve()
            self.render()

        # 'R' para Reiniciar y Generar nuevo (keycode 114 o 15)
        elif keycode in [114, 15, 82]:
            self.solution_path = ""
            self.maze.regenerate()
            self.maze.generate()  # Lo generamos al instante
            self.render()

        return 0

    def run_animated(self):
        self.mlx.mlx_key_hook(self.win_ptr, self.handle_keys, None)
        self.mlx.mlx_loop(self.mlx_ptr)
