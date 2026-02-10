
import sys
from typing import Dict, Tuple


class MazeConfig:
    """
    Clase encargada de parsear, validar y almacenar la configuración
    necesaria para la generación del laberinto.
    """

    def __init__(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo
        # Atributos que se llenarán tras la carga
        self.width: int = 0
        self.height: int = 0
        self.seed: int = 0
        self.output_file: str = ""
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.is_perfect: bool = False

        # Ejecutamos el flujo de carga al instanciar
        datos_crudos = self._leer_archivo()
        self._procesar_y_validar(datos_crudos)

    def _leer_archivo(self) -> Dict[str, str]:
        """Lee el archivo y extrae los pares clave-valor."""
        config: Dict[str, str] = {}
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea or linea.startswith("#"):
                        continue

                    if "=" in linea:
                        clave, valor = linea.split("=", 1)
                        config[clave.strip().upper()] = valor.strip()
        except FileNotFoundError:
            print(f"Error: El archivo '{self.nombre_archivo}' no existe.")
            sys.exit(1)
        return config

    def _procesar_y_validar(self, config: Dict[str, str]) -> None:
        """Transforma los datos crudos en atributos
        de clase y aplica lógica de negocio."""
        try:
            self.width = int(config.get("WIDTH", -1))
            self.height = int(config.get("HEIGHT", -1))
            self.seed = int(config.get("SEED", -1))
            self.output_file = config.get("OUTPUT_FILE", "maze.txt")
            self.is_perfect = config.get("PERFECT", "False").lower() == "true"

            # Procesamiento de coordenadas
            self.entry = self._parsear_coordenadas(config.get("ENTRY", ""))
            self.exit = self._parsear_coordenadas(config.get("EXIT", ""))

        except (ValueError, IndexError):
            print(
                "Error: Formato de datos inválido en el"
                "archivo de configuración.")
            sys.exit(1)

        self._validar_logica()

    def _parsear_coordenadas(self, texto: str) -> Tuple[int, int]:
        """Helper para convertir 'x,y' en una tupla de enteros."""
        partes = texto.split(",")
        return (int(partes[0].strip()), int(partes[1].strip()))

    def _validar_logica(self) -> None:
        """Aplica las reglas de negocio del laberinto."""
        # 1. Dimensiones
        if self.width <= 0 or self.height <= 0:
            print("Error: El ancho y alto deben ser mayores a 0.")
            sys.exit(1)

        # 2. Límites de Entrada/Salida
        ex, ey = self.entry
        sx, sy = self.exit

        fuera = (ex < 0 or ex >= self.width or ey < 0 or ey >= self.height or
                 sx < 0 or sx >= self.width or sy < 0 or sy >= self.height)

        if fuera:
            print("Error: ENTRY o EXIT están fuera de los límites.")
            sys.exit(1)

        # 3. Diferencia (Requisito IV.4)
        if self.entry == self.exit:
            print("Error: La entrada y la salida deben ser diferentes.")
            sys.exit(1)


# --- Ejemplo de uso si se ejecuta directamente ---
if __name__ == "__main__":
    if len(sys.argv) == 2:
        maze_config = MazeConfig(sys.argv[1])
        maze_config.mostrar_resumen()
    else:
        print("Uso: python3 parseo.py config.txt")
