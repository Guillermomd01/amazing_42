import sys

try:
    from mlx.mlx import Mlx
except ImportError:
    sys.exit(1)


class MazeVisualizer():
    def __init__(self, maze, tile_size=25):
        self.maze = maze
        self.tile_size = tile_size
        self.is_generating = False  # Estado para controlar la animación
        self.solution_path = ""      # Almacena la solución para dibujarla

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_w = self.maze.width * self.tile_size
        self.win_h = self.maze.height * self.tile_size
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "Amazeing Premium v2")

        self.img = self.mlx.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)
        raw_data = self.mlx.mlx_get_data_addr(self.img)
        self.img_data, self.bpp, self.size_line, self.endian = raw_data

        self.wall_color = 0xFFFFFF
        self.solu_color = 0xFF0000  # Rojo vibrante para la solución

        self.render()

    def _put_pixel(self, x, y, color):
        if 0 <= x < self.win_w and 0 <= y < self.win_h:
            offset = (y * self.size_line) + (x * (self.bpp // 8))
            self.img_data[offset] = color & 0xFF
            self.img_data[offset + 1] = (color >> 8) & 0xFF
            self.img_data[offset + 2] = (color >> 16) & 0xFF
            self.img_data[offset + 3] = 0xFF

    def render(self):
        """Dibuja el laberinto y, si existe, la solución."""
        # Limpiar fondo (Negro)
        for i in range(len(self.img_data)):
            self.img_data[i] = 0

        # Dibujar Laberinto
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                px, py = x * self.tile_size, y * self.tile_size
                val = self.maze.grid[x][y]
                if val & 1:  # N
                    for i in range(self.tile_size):
                        self._put_pixel(px + i, py, self.wall_color)
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

        # Dibujar Solución si ha sido activada ('S')
        if self.solution_path:
            self._draw_solution()

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img, 0, 0)
        self.mlx.mlx_do_sync(self.mlx_ptr)

    def _draw_solution(self):
        """Traza una línea visual para la solución."""
        cx, cy = self.maze.entry
        for move in self.solution_path:
            # Dibujamos un punto en el centro de la celda actual
            center = self.tile_size // 2
            px, py = cx * self.tile_size + center, cy * self.tile_size + center

            # Marcamos el camino (un pequeño cuadrado central)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    self._put_pixel(px + dx, py + dy, self.solu_color)

            if move == 'N':
                cy -= 1
            elif move == 'E':
                cx += 1
            elif move == 'S':
                cy += 1
            elif move == 'W':
                cx -= 1

    def animation_hook(self, *args):
        """Bucle de animación: solo actúa si is_generating es True."""
        if self.is_generating:
            if self.maze.generate_step():
                self.render()
            else:
                self.is_generating = False  # Terminó la generación
        return 0

    def handle_keys(self, keycode, *args):
        # ESC (53 en Mac, 65307 en Linux)
        if keycode in [53, 65307]:
            # Cierre limpio para evitar el error de callback
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            sys.exit(0)

        # 'G' para Generar (keycode 103)
        elif keycode == 103:
            self.is_generating = True

        # 'S' para Solución (keycode 115)
        elif keycode == 115:
            self.solution_path = self.maze.solve()
            self.render()

        # 'R' para Reiniciar (keycode 114)
        elif keycode == 114:
            self.is_generating = False
            self.solution_path = ""
            self.maze.regenerate()
            self.render()

        # 'C' para Color
        elif keycode == 99:
            self.change_wall_color()

        return 0

    def run_animated(self):
        self.mlx.mlx_key_hook(self.win_ptr, self.handle_keys, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animation_hook, None)
        self.mlx.mlx_loop(self.mlx_ptr)
