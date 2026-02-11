from mazegenerator import MazeGenerator
from mazevisualizer import MazeVisualizer
from parseo import MazeConfig

if __name__ == "__main__":
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
