# A-Maze-ing Project 🧩

*Este proyecto ha sido creado como parte del currículo de 42 por gumunoz, savaquer.*

---

**Descripción del Proyecto**

El propósito de este proyecto es el diseño y desarrollo de un sistema completo para la **generación, resolución y visualización de laberintos**. El sistema permite crear laberintos "perfectos" (un solo camino entre dos puntos) o "imperfectos" mediante la configuración de parámetros externos. Además, incluye un sistema único de inyección de patrones estáticos (el número "42") dentro de la estructura generada.

---

**Instrucciones: Compilación e Instalación**

**Requisitos previos**
* Python 3.7 o superior.
* Herramientas de empaquetado: `pip install build`.

**Entorno Virtual (VENV)**
Para garantizar un entorno de ejecución limpio y evitar conflictos con librerías globales, el proyecto utiliza un entorno virtual (`venv`):
* El `Makefile` crea automáticamente la carpeta `venv/` al ejecutar la instalación.
* Se instalan todas las dependencias (como `flake8`, `mypy` o la `mlx`) dentro de este entorno aislado.
* No es necesario activar el entorno manualmente si se utiliza `make`, ya que el script apunta directamente al binario interno.

**Compilación e Instalación**
El proyecto utiliza un `Makefile` para gestionar el entorno virtual y las dependencias de forma automática. Para preparar el entorno virtual e instalar las dependencias necesarias, ejecuta:
`make install`

**Ejecución del programa**
Para generar y visualizar el laberinto utilizando el archivo de configuración `config.txt`:
`make` o `make run`

**Control de Calidad (Linters)**
Para verificar la consistencia del código y tipos (Flake8 y Mypy):
`make lint`

**Limpieza**
Para eliminar el entorno virtual y archivos temporales de caché:
`make clean`

---

**Generación del Paquete (mazegen.tar.gz)**
1. Navega a la carpeta del proyecto.
2. Ejecuta el comando: `python3 -m build`.
3. El archivo solicitado `mazegen.tar.gz` aparecerá dentro de la carpeta `/dist`.

**Ejecución del programa principal (Manual)**
Para generar y visualizar el laberinto configurado en el archivo de texto directamente desde la terminal:
`python3 a_maze_ing.py config.txt`

---

**Archivo de Configuración (config.txt)**

El programa utiliza un archivo de texto plano para definir el comportamiento. Formato: `CLAVE=VALOR`.

| Clave | Descripción | Ejemplo |
| :--- | :--- | :--- |
| **WIDTH** | Ancho del laberinto (entero positivo). | `WIDTH=30` |
| **HEIGHT** | Alto del laberinto (entero positivo). | `HEIGHT=20` |
| **SEED** | Semilla para replicabilidad (opcional). | `SEED=12345` |
| **ENTRY** | Coordenadas x,y de entrada (exactamente 2). | `ENTRY=0,0` |
| **EXIT** | Coordenadas x,y de salida (exactamente 2). | `EXIT=29,19` |
| **PERFECT** | `True` (camino único) o `False` (ciclos). | `PERFECT=True` |
| **OUTPUT_FILE** | Nombre del archivo de guardado. | `OUTPUT_FILE=maze.txt` |

---

**Algoritmos Utilizados**

**1. Generación: Randomized Backtracking (DFS)**
Se utiliza una búsqueda en profundidad para tallar los pasillos del laberinto.
* **Garantía de Perfección**: Crea un árbol de expansión que asegura que no hay celdas aisladas.
* **Estructura**: Genera pasillos largos y complejos.
* **Restricción 3x3**: Al avanzar paso a paso entre celdas adyacentes, el algoritmo impide por diseño la formación de áreas vacías de 3x3.

**2. Resolución: Breadth First Search (BFS)**
Para calcular la solución óptima (el camino más corto entre entrada y salida), el programa implementa un algoritmo de búsqueda en anchura.
* **Optimización**: A diferencia de DFS, BFS garantiza encontrar el camino más corto en un grafo sin pesos.
* **Visualización**: Se activa mediante la tecla 'S' en el visualizador gráfico.

---

**Módulo Reutilizable: mazegenerator**

El módulo es totalmente autónomo y robusto:
* **Replicabilidad**: El uso de `random.Random(seed)` asegura resultados idénticos con la misma semilla.
* **Patrón 42**: Función `_inject_42()` que reserva celdas antes de la generación para formar el patrón si el tamaño es suficiente.

---

**Recursos y Bibliografía**

**Referencias y Tutoriales**
* **Algoritmos**: Tutoriales de YouTube sobre *Depth First Search* (DFS) para generación y *Breadth First Search* (BFS) para resolución.
* **Gráficos**: Documentación de la librería **MiniLibX (MLX)** para la gestión de ventanas y buffers de imagen.
* **Tutoriales MLX**: Guías de la comunidad de 42 para el manejo de eventos de teclado y colores.
  
---

**Uso de Inteligencia Artificial (IA)**
Se utilizó **Gemini (IA)** como asistente de programación en:
* **Verificaciones**: Lógica estricta para que el programa falle si se introducen datos incoherentes.
* **Docstrings**: Creación de documentación interna siguiendo estándares de Python.
* **Dudas Técnicas**: Resolución de problemas sobre la implementación de BFS para la solución y estructuración del paquete.
* **Readmes**: Estructuración y formato técnico de la documentación del proyecto.
