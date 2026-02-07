from mazegenerator import MazeGenerator
from mazevisualizer import MazeVisualizer

if __name__ == "__main__":
    # 1. Configuramos el producto
    ancho, alto = 50, 50
    maze = MazeGenerator(ancho, alto, seed=123)

    # 2. Preparamos el punto de inicio
    # Marcamos la entrada (0,0) como visitada y la metemos en la pila
    maze.visited[0][0] = True
    maze.stack.append((0, 0))

    # 3. ¡Arrancamos el motor!
    maze.generate()
    # generacion txt
    maze.save("maze_test.txt")
    print("\n [OK]")
    # 4. Validamos el resultado
    maze.display_numeric()
    maze.display_ascii()

    visualizer = MazeVisualizer(maze, tile_size=25)
    visualizer.run()
