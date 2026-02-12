# A-Maze-ing Project 🧩

*This project has been created as part of the 42 curriculum by gumunoz and savaquer.*

---

**Project Description**

The goal of this project is the design and development of a comprehensive system for **maze generation, solving, and visualization**. The engine allows for the creation of "perfect" mazes (a single unique path between two points) or "imperfect" mazes through external configuration parameters. Additionally, it features a unique static pattern injection system that embeds the number "42" into the generated structure.

---

**Project Management**

Regarding task distribution, we decided to divide the project by objectives, with both members working on each. This approach ensures that every team member masters the core pillars: algorithms, the graphics engine, and parsing.

**Instructions: Compilation and Installation**

**Prerequisites**
* Python 3.7 or higher.
* Packaging tools: `pip install build`.

**Virtual Environment (VENV)**
To ensure a clean execution environment and avoid conflicts with global libraries, the project utilizes a virtual environment (`venv`):
* The `Makefile` automatically creates the `venv/` folder upon installation.
* All dependencies (such as `flake8`, `mypy`, or the `mlx` library) are installed within this isolated environment.
* There is no need to activate the environment manually if using `make`, as the script points directly to the internal binary.

**Compilation and Installation**
The project uses a `Makefile` to handle the virtual environment and dependencies automatically. To prepare the virtual environment and install necessary dependencies, run:
`make install`

**Running the Program**
To generate and visualize the maze using the `config.txt` configuration file:
`make` or `make run`

**Quality Control (Linters)**
To verify code consistency and typing (Flake8 and Mypy):
`make lint`

**Cleanup**
To remove the virtual environment and temporary cache files:
`make clean`

---

**Package Generation (mazegen.tar.gz)**
1. Navigate to the project folder.
2. Run the command: `python3 -m build`.
3. The requested file `mazegen.tar.gz` will appear inside the `/dist` folder.

**Manual Execution**
To generate and visualize the maze directly from the terminal using the configuration file:
`python3 a_maze_ing.py config.txt`

---

**Configuration File (config.txt)**

The program uses a plain text file to define its behavior. Format: `KEY=VALUE`.

| Key | Description | Example |
| :--- | :--- | :--- |
| **WIDTH** | Maze width (positive integer). | `WIDTH=30` |
| **HEIGHT** | Maze height (positive integer). | `HEIGHT=20` |
| **SEED** | Seed for replicability (optional). | `SEED=12345` |
| **ENTRY** | Entry x,y coordinates (exactly 2). | `ENTRY=0,0` |
| **EXIT** | Exit x,y coordinates (exactly 2). | `EXIT=29,19` |
| **PERFECT** | `True` (unique path) or `False` (cycles). | `PERFECT=True` |
| **OUTPUT_FILE** | Name of the output save file. | `OUTPUT_FILE=maze.txt` |

---

**Core Algorithms**

**1. Generation: Randomized Backtracking (DFS)**
A Depth-First Search is used to carve the maze corridors.
* **Guaranteed Perfection**: Creates a spanning tree that ensures no isolated cells.
* **Structure**: Generates long, complex corridors.
* **3x3 Constraint**: By moving step-by-step between adjacent cells, the algorithm is designed to prevent the formation of empty 3x3 areas.

**2. Solving: Breadth-First Search (BFS)**
To calculate the optimal solution (the shortest path between entry and exit), the program implements a BFS algorithm.
* **Optimization**: Unlike DFS, BFS guarantees finding the shortest path in an unweighted graph.
* **Visualization**: Activated by pressing the 'S' key in the graphical visualizer.

---

**Reusable Module: mazegenerator**

The module is completely autonomous and robust:
* **Replicability**: The use of `random.Random(seed)` ensures identical results with the same seed.
* **42 Pattern**: The `_inject_42()` function reserves cells before generation to form the pattern if the dimensions allow.

---

**Resources and Bibliography**

**References and Tutorials**
* **Algorithms**: YouTube tutorials on *Depth First Search* (DFS) for generation and *Breadth First Search* (BFS) for solving.
* **Graphics**: **MiniLibX (MLX)** library documentation for window management and image buffers.
* **MLX Tutorials**: 42 community guides for keyboard event handling and color management.
  
---

**Use of Artificial Intelligence (AI)**
**Gemini (AI)** was used as a programming assistant for:
* **Validation**: Strict logic to ensure the program fails gracefully if inconsistent data is provided.
* **Docstrings**: Creation of internal documentation following Python standards.
* **Technical Inquiries**: Problem-solving regarding BFS implementation for the solution and package structuring.
* **Readmes**: Structuring and technical formatting of the project documentation.