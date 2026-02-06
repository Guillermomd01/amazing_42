import mlx


class MazeVisualizer():
    def __init__(self, maze, tile_size=30):
        self.maze = maze
        self.tile_size = tile_size

        self.mlx_ptr = mlx.init()
        self.win_w = self.maze.width * self.tile_size
        self.win_h = self.maze.height * self.tile_size

        self.win_ptr = mlx.new_window(
            self.mlx_ptr, self.win_w, self.win_h, "Amazeing - 42 project")
        self.wall_color = 0xFFFFFF
        self.entry_color = 0x00FF00
        self.exit_color = 0xFF0000

    def _draw_line(self, x1, y1, x2, y2, color):
        if x1 == x2:
            for y in range(min(y1, y2), max(x1, x2)):
                mlx.pixel.put(self.mlx_ptr, self.win_ptr, x1, y, color)
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)):
                mlx.pixel_put(self.mlx_ptr, self.win_ptr, x, y1, color)

    def render(self):
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

    def close_window(self, keycode):
        if keycode in [53, 65307]:
            exit(0)

    def run(self):
        self.render()
        mlx.key_hook(self.win_ptr, self.close_window)
        mlx.loop(self.mlx.ptr)
