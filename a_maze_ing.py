from mazegenerator import MazeGenerator
from mazevisualizerprueba import MazeVisualizer
import random


if __name__ == "__main__":
    # 1. Creamos el objeto, pero NO llamamos a maze.generate() todavía
    maze = MazeGenerator(20, 20, seed=random.randint(0, 999))

    # 2. El visualizador se encargará de llamar a generate_step() frame a frame
    visualizer = MazeVisualizer(maze, tile_size=25)

    print("Iniciando motor gráfico... Pulsa ESC para salir, R para reiniciar.")
    visualizer.run_animated()

    """
    maze.display_numeric()
    maze.display_ascii()
    maze.save("maze_test.txt")
    print("\n [OK]")"""
