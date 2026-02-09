import sys
from typing import Dict

def cargar_configuracion(nombre_archivo: str) -> Dict[str, str]:
    """
    Lee el archivo de configuración y devuelve un diccionario con los datos.
    Usa un gestor de contexto (with) para evitar fugas de memoria (Requisito III.1).
    """
    config: Dict[str, str] = {}
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                # Saltamos comentarios o líneas vacías
                if not linea or linea.startswith("#"):
                    continue
                
                if "=" in linea:
                    # Dividimos solo por el primer '='
                    clave, valor = linea.split("=", 1)
                    config[clave.strip()] = valor.strip()
                else:
                    print(f"Aviso: Línea ignorada (formato incorrecto): {linea}")
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        sys.exit(1)
    
    return config

def main() -> None:
    # IV.2 Uso: El programa debe recibir el archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    nombre_archivo = sys.argv[1]
    config = cargar_configuracion(nombre_archivo)

    # --- TRANSFORMACIÓN Y VALIDACIÓN (Bloque try-except Requisito III.1) ---
    try:
        # Extraemos datos con .get() y valores por defecto para evitar que explote
        width: int = int(config.get("WIDTH", -1))
        height: int = int(config.get("HEIGHT", -1))
        seed: int = int(config.get("SEED", -1))
        output_file: str = config.get("OUTPUT_FILE", "maze.txt")
        
        # Procesamos ENTRY (x,y)
        raw_entry = config.get("ENTRY", "")
        partes_entry = raw_entry.split(",")
        ent_x: int = int(partes_entry[0].strip())
        ent_y: int = int(partes_entry[1].strip())

        # Procesamos EXIT (x,y)
        raw_exit = config.get("EXIT", "")
        partes_exit = raw_exit.split(",")
        exit_x: int = int(partes_exit[0].strip())
        exit_y: int = int(partes_exit[1].strip())

        # PERFECT debe ser booleano (IV.3)
        is_perfect: bool = config.get("PERFECT", "False").lower() == "true"

    except (ValueError, IndexError):
        print("Error: Formato de datos inválido en el archivo de configuración.")
        print("Asegúrate de que WIDTH, HEIGHT y SEED sean números, y ENTRY/EXIT tengan el formato x,y")
        sys.exit(1)

    # --- VALIDACIÓN LÓGICA (Requisitos IV.3 y IV.4) ---

    # 1. Dimensiones positivas
    if width <= 0 or height <= 0:
        print("Error: El ancho y alto del laberinto deben ser mayores a 0.")
        sys.exit(1)

    # 2. Entrada y salida dentro de los límites
    fuera_limites = (
        ent_x < 0 or ent_x >= width or ent_y < 0 or ent_y >= height or
        exit_x < 0 or exit_x >= width or exit_y < 0 or exit_y >= height
    )
    if fuera_limites:
        print("Error: La entrada (ENTRY) o salida (EXIT) están fuera del laberinto.")
        sys.exit(1)

    # 3. Entrada y salida deben ser diferentes (IV.4)
    if ent_x == exit_x and ent_y == exit_y:
        print("Error: La entrada y la salida deben ser celdas diferentes.")
        sys.exit(1)

    # Si todo está OK
    print(f"--- Configuración cargada correctamente ---")
    print(f"Dimensiones: {width}x{height}")
    print(f"Semilla: {seed}")
    print(f"Archivo de salida: {output_file}")
    print(f"¿Es perfecto?: {is_perfect}")

if __name__ == "__main__":
    main()