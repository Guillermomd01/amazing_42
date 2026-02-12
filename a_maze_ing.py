from mazegenerator import MazeGenerator
from mazevisualizer import MazeVisualizer
from parser import MazeConfig
import sys
import os


def main() -> None:
    file_required = "config.txt"

    if len(sys.argv) != 2:
        print("ERROR: wrong number of arguments")
        sys.exit(2)

    file_argument = os.path.basename(sys.argv[1])

    if file_argument != file_required:
        print("ERROR: config.txt not found ")
        sys.exit(1)

    config = MazeConfig("config.txt")

    maze = MazeGenerator(
        config.width, config.height,
        config.exit, config.is_perfect,
        config.entry, config.seed)
    maze. generate()
    # maze.display_numeric()
    maze.display_ascii()
    maze.save(config.output_file)
    print("\n [OK]")

    visualizer = MazeVisualizer(maze, tile_size=25)

    print("Iniciando motor gráfico...")
    print(
        "Pulsa ESC para salir, R para reiniciar,"
        "S para mostrar/ocultar la solución y "
        "C para cambiar el color de los muros.")
    visualizer.run_animated()


if __name__ == "__main__":
    main()
