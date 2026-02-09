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

    def _put_pixel_fast(self, x, y, color):
        """Escribe directamente en la memoria de la imagen
        (Rendimiento Extremo)"""
        if x < 0 or x >= self.win_w or y < 0 or y >= self.win_h:
            return

        # Calcular la posición en el array de bytes
        index = (y * self.size_line) + (x * 4)

        # Descomponemos el color en bytes (Blue, Green, Red, Alpha)
        # Nota: MLX suele usar Little Endian (BGRA)
        b = color & 0xFF
        g = (color >> 8) & 0xFF
        r = (color >> 16) & 0xFF
        a = 0

        # Escribimos en el buffer
        self.img_data[index] = b
        self.img_data[index + 1] = g
        self.img_data[index + 2] = r
        self.img_data[index + 3] = a

    def _clear_image(self):
        """Limpia el lienzo (rellena de negro)"""
        # Una forma rápida de borrar es rellenar el array con 0
        # Aunque para mantenerlo simple,
        # podemos no hacer nada si sobreescribimos todo
        # O usar un bucle simple si es necesario.
        # Por rendimiento, asumimos redibujado.
        pass

    def _draw_line(self, x1, y1, x2, y2, color):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if x1 == x2:  # Línea vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self._put_pixel_fast(x1, y, color)
        elif y1 == y2:  # Línea horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self._put_pixel_fast(x, y1, color)

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
        # 1. Limpiamos la imagen (Pintamos todo de negro primero es una opción,
        # pero aquí simplemente dibujamos encima)
        # Para limpiar "bien", podríamos rellenar self.img_data con ceros,
        # pero para el MVP basta con asegurar que dibujamos lo necesario.

        # Limpieza manual rápida (opcional, consume CPU pero asegura limpieza)
        # self.img_data[:] = bytes(len(self.img_data))

        # 2. Dibujamos el laberinto en el BUFFER (No en la ventana)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                px = x * self.tile_size
                py = y * self.tile_size
                cell_value = self.maze.grid[x][y]

                # Pared Norte
                if cell_value & 1:
                    self._draw_line(
                        px, py, px + self.tile_size, py, self.wall_color)
                # Pared Este
                if cell_value & 2:
                    self._draw_line(
                        px + self.tile_size, py, px + self.tile_size, py +
                        self.tile_size, self.wall_color)
                # Pared Sur
                if cell_value & 4:
                    self._draw_line(
                        px, py + self.tile_size, px + self.tile_size, py +
                        self.tile_size, self.wall_color)
                # Pared Oeste
                if cell_value & 8:
                    self._draw_line(
                        px, py, px, py + self.tile_size, self.wall_color)

        if self.show_solution:
            self.draw_path()

        # 3. EL GRAN FINAL: Empujamos la imagen completa
        # a la ventana de una vez
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
        if self.maze.generate_step():
            self.render()
        else:
            # Una vez terminado, podemos desactivar el hook
            # para ahorrar energía
            self.mlx.mlx_loop_hook(self.mlx_ptr, None, None)
            print("Generación completada con éxito.")
        return 0

    def handle_keys(self, keycode, param=None):
        # ESC
        if keycode == 53 or keycode == 65307:
            sys.exit(0)
        # S: show solution
        elif keycode == 115:
            self.show_solution = not self.show_solution
            self.render()
        # R: Regenerate
        elif keycode == 114:
            print("Regenerating maze...")
            self.maze.regenerate()
            # Limpiamos buffer visual (truco rápido: pintar
            # un cuadro negro gigante o reiniciar imagen)
            # Para este MVP, simplemente redibujamos encima.
            self.render()
        # C: Change color wall
        elif keycode == 99:
            self.change_wall_color()
        return 0

    def run_animated(self):
        self.mlx.mlx_key_hook(self.win_ptr, self.handle_keys, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animation_hook, None)
        self.mlx.mlx_loop(self.mlx_ptr)
