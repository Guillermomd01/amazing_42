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
            print("Error: Fallo crítico en el motor gráfico (MLX_INIT).")
            sys.exit(1)

        self.win_w = self.maze.width * self.tile_size
        self.win_h = self.maze.height * self.tile_size
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "Amazeing - 42 project")

        # --- MEJORA DE PRODUCTO: SISTEMA DE IMAGEN (BUFFER) ---
        # Creamos una imagen en memoria para dibujar sin lag
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)

        # Obtenemos la dirección de memoria para escribir píxeles
        # a la velocidad de la luz
        # data es un memoryview, bpp es bits por pixel, size_line
        # es el ancho en bytes
        raw_data = self.mlx.mlx_get_data_addr(self.img)
        self.img_data, self.bpp, self.size_line, self.endian = raw_data

        # Colores corporativos
        self.bg_color = 0x000000  # Fondo negro elegante
        self.wall_color = 0xFFFFFF
        self.entry_color = 0x00FF00
        self.exit_color = 0xFF0000
        self.solu_color = 0x00FFFF
        self.render()

    def _put_pixel_fast(self, x, y, color):
        """Escribe directamente en la memoria de la imagen
        (Rendimiento Extremo)"""
        if 0 <= x < self.win_w and 0 <= y < self.win_h:
            idx = (y * self.size_line) + (x * 4)
            self.img_data[idx] = color & 0xFF
            self.img_data[idx + 1] = (color >> 8) & 0xFF
            self.img_data[idx + 2] = (color >> 16) & 0xFF

    def _clear_image(self):
        """Limpia el lienzo (rellena de negro)"""
        # Una forma rápida de borrar es rellenar el array con 0
        # Aunque para mantenerlo simple,
        # podemos no hacer nada si sobreescribimos todo
        # O usar un bucle simple si es necesario.
        # Por rendimiento, asumimos redibujado.
        for i in range(len(self.img_data)):
            self.img_data[i] = 0

    def draw_path(self):
        "Dibuja la ruta premium de solución"
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
                cx -= 1
            end_x = cx * tile_size + tile_size // 2
            end_y = cy * tile_size + tile_size // 2
            self._draw_line(start_x, start_y, end_x, end_y, self.solu_color)

    def render(self):
        self._clear_image()
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                px, py = x * self.tile_size, y * self.tile_size
                val = self.maze.grid[x][y]
                # Dibujar paredes
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

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img, 0, 0)

    def change_wall_color(self) -> None:
        """Cambiar el color de las paredes para refrescar
        el look del producto"""
        colors = [
            0xFF8C00, 0x8A2BE2, 0xFF00FF, 0xFFD700, 0x1E90FF, 0xFF69B4,
            0x32CD32, 0x4B0082, 0x7FFF00, 0x0000FF]
        wall = random.choice(colors)
        while wall == self.wall_color:
            wall = random.choice(colors)
        self.wall_color = wall
        self.render()

    def animation_hook(self, param=None):
        """
        Este es el 'corazón' de la animación. Se ejecuta en cada frame.
        """
        # Intentamos dar un paso en la generación
        if self.maze.stack:
            if self.maze.generate_step():
                self.render()
        return 0

    def handle_keys(self, keycode, *args):
        # ESC
        if keycode == 53 or keycode == 65307:
            sys.exit(0)
        # S: show solution
        elif keycode == 115:
            self.show_solution = not self.show_solution
            self.render()
        # R: Regenerate
        elif keycode == 114 or keycode == 31:
            print("Regenerating maze...")
            self.maze.regenerate()
            # Limpiamos buffer visual (truco rápido: pintar
            # un cuadro negro gigante o reiniciar imagen)
            # Para este MVP, simplemente redibujamos encima.
            self.render()
        # C: Change color wall
        elif keycode == 99 or keycode == 46:
            self.change_wall_color()
        return 0

    def run_animated(self):
        self.mlx.mlx_key_hook(self.win_ptr, self.handle_keys, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animation_hook, None)
        self.mlx.mlx_loop(self.mlx_ptr)
