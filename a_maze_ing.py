from mazegenerator import MazeGenerator
from mazevisualizer import MazeVisualizer
import random


if __name__ == "__main__":
    # 1. Configuramos el producto
    maze = MazeGenerator(15, 15, seed=random.randint(0, 999))

    # generacion txt
    # 4. Validamos el resultado
    maze.generate()
    maze.display_numeric()
    maze.display_ascii()
    maze.save("maze_test.txt")
    print("\n [OK]")

    visualizer = MazeVisualizer(maze, tile_size=25)
    visualizer.run_animated()
