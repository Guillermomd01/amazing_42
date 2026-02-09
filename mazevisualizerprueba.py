import sys
import random
try:
    from mlx.mlx import Mlx
except ImportError:
    sys.exit(1)


class MazeVisualizer():
    def __init__(self, maze, tile_size=25):
        self.maze = maze
        self.tile_size = tile_size
        self.show_solution = False

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_w = self.maze.width * self.tile_size
        self.win_h = self.maze.height * self.tile_size
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "Amazeing Premium v2")

        # --- MEJORA TÉCNICA: BUFFER DE ALTO RENDIMIENTO ---
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)
        # Extraemos los parámetros técnicos del buffer
        raw_data = self.mlx.mlx_get_data_addr(self.img)
        self.img_data, self.bpp, self.size_line, self.endian = raw_data

        self.wall_color = 0xFFFFFF
        self.solu_color = 0x00FFFF

        # Render inicial para que no aparezca vacía al arrancar
        self.render()

    def _put_pixel(self, x, y, color):
        """
        Dibuja un píxel directamente en la memoria de video.
        Aplicamos la lógica de offset y canal Alpha aprendida.
        """
        if 0 <= x < self.win_w and 0 <= y < self.win_h:
            # Calculamos la posición exacta en el array de bytes
            offset = (y * self.size_line) + (x * (self.bpp // 8))

            # Formato BGRA (Blue, Green, Red, Alpha)
            self.img_data[offset] = color & 0xFF
            self.img_data[offset + 1] = (color >> 8) & 0xFF
            self.img_data[offset + 2] = (color >> 16) & 0xFF
            self.img_data[offset + 3] = 0xFF  # <-- CRUCIAL: Opacidad total

    def render(self):
        """Dibuja el estado actual del laberinto en el buffer."""
        # Limpiar pantalla (Negro sólido)
        for i in range(len(self.img_data)):
            self.img_data[i] = 0

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                px, py = x * self.tile_size, y * self.tile_size
                val = self.maze.grid[x][y]

                # Dibujado de paredes (1:N, 2:E, 4:S, 8:W)
                if val & 1:  # Norte
                    for i in range(self.tile_size):
                        self._put_pixel(px + i, py, self.wall_color)
                if val & 2:  # Este
                    for i in range(self.tile_size):
                        self._put_pixel(
                            px + self.tile_size - 1, py + i, self.wall_color)
                if val & 4:  # Sur
                    for i in range(self.tile_size):
                        self._put_pixel(
                            px + i, py + self.tile_size - 1, self.wall_color)
                if val & 8:  # Oeste
                    for i in range(self.tile_size):
                        self._put_pixel(px, py + i, self.wall_color)

        # Volcamos el buffer a la ventana y sincronizamos
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img, 0, 0)
        self.mlx.mlx_do_sync(self.mlx_ptr)

    def change_wall_color(self):
        """Cambio de estética instantáneo."""
        colors = [0xFF8C00, 0x8A2BE2, 0xFF00FF, 0xFFD700, 0x1E90FF, 0x32CD32]
        new_color = random.choice(colors)
        while new_color == self.wall_color:
            new_color = random.choice(colors)
        self.wall_color = new_color
        self.render()

    def animation_hook(self, *args):
        """Paso a paso de la generación para un efecto visual impactante."""
        if self.maze.stack:
            if self.maze.generate_step():
                self.render()
        return 0

    def handle_keys(self, keycode, *args):
        # ESC para salir (Soporta Linux/Mac)
        if keycode in [53, 65307]:
            sys.exit(0)
        # 'C' para cambiar color
        elif keycode == 99:
            self.change_wall_color()
        # 'R' para resetear
        elif keycode == 114:
            self.maze.regenerate()
            self.render()
        return 0

    def run_animated(self):
        self.mlx.mlx_key_hook(self.win_ptr, self.handle_keys, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animation_hook, None)
        self.mlx.mlx_loop(self.mlx_ptr)
