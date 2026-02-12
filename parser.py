import sys
from typing import Dict, Tuple


class MazeConfig:
    """
    Class responsible for parsing, validating, and storing the
    configuration needed for maze generation.
    """

    def __init__(self, file_name: str):
        """Initialize the config by reading and processing the file."""
        self.file_name = file_name
        self.width: int = 0
        self.height: int = 0
        self.seed: int = 0
        self.output_file: str = ""
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.is_perfect: bool = False

        raw_data = self._read_file()
        self._process_and_validate(raw_data)

    def _read_file(self) -> Dict[str, str]:
        """Read the configuration file and extract key-value pairs."""
        config: Dict[str, str] = {}
        try:
            with open(self.file_name, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    if "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip().upper()] = value.strip()
        except FileNotFoundError:
            print(f"Error: The file '{self.file_name}' does not exist.")
            sys.exit(1)
        return config

    def _process_and_validate(self, config: Dict[str, str]) -> None:
        """Convert raw strings into class attributes and types."""
        try:
            self.width = int(config.get("WIDTH", -1))
            self.height = int(config.get("HEIGHT", -1))
            self.seed = int(config.get("SEED", -1))
            self.output_file = config.get("OUTPUT_FILE", "maze.txt")
            self.is_perfect = config.get("PERFECT", "False").lower() == "true"

            self.entry = self._parse_coordinates(config.get("ENTRY", ""))
            self.exit = self._parse_coordinates(config.get("EXIT", ""))

        except (ValueError, IndexError):
            print("Error: Invalid data format in the configuration file.")
            sys.exit(1)

        self._validate_logic()

    def _parse_coordinates(self, text: str) -> Tuple[int, int]:
        """Convert a 'x,y' string into an integer tuple."""
        parts = text.split(",")
        return (int(parts[0].strip()), int(parts[1].strip()))

    def _validate_logic(self) -> None:
        """Apply business rules and maze constraints."""
        if self.width <= 0 or self.height <= 0:
            print("Error: Width and height must be greater than 0.")
            sys.exit(1)

        ex, ey = self.entry
        sx, sy = self.exit

        out_of_bounds = (ex < 0 or ex >= self.width or
                         ey < 0 or ey >= self.height or
                         sx < 0 or sx >= self.width or
                         sy < 0 or sy >= self.height)

        if out_of_bounds:
            print("Error: ENTRY or EXIT are out of grid bounds.")
            sys.exit(1)

        if self.entry == self.exit:
            print("Error: ENTRY and EXIT must be different locations.")
            sys.exit(1)
