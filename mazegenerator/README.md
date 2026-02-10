# MazeGenerator

## Description

MazeGenerator is a class reusable for generating and solvig mazes. This class use "42" pattern at the middle of maze and create perfect and imperfect maze with a seed


## Installation

Install the package

```bash
pip install poneraqui.tar
```

# Usage

## Import the package

```python
from mazegenerator import MazeGenerator
```

### Create a instance

```python
maze = MazeGenerator(
    width=20,
	height=15,
    entry=(0, 0),
	exit=(19, 14),
    perfect=True,        # True = unique path
    seed=42
)
```

### Generate maze

```python
maze.generate()
```

### SOlve maze

```python
maze.solve()
```

### Display numeric maze in terminal

```python
maze.display_numeric()
```

### Display ascii maze in terminal

```python
maze.display_ascii()
```

## Data Structure

To maximize efficiency and minimize memory footprint, the maze is stored in self.grid as a 2D matrix of integers. Each integer acts as a bit-mask representing the wall configuration for that specific cell:


| Bit | Direction | Value (Binary) |
| :---: | :--- | :--- |
| 0 | **North** | `0001` |
| 1 | **East** | `0010` |
| 2 | **South** | `0100` |
| 3 | **West** | `1000` |

## Parameters

| Parameter   | Type             | Default  | Description                                                                                    |
| ----------- | ---------------- | -------- | ---------------------------------------------------------------------------------------------- |
| `width`     | `int`            | —        | Maze grid width                                                                                |
| `height`    | `int`            | —        | Maze grid height                                                                               |
| `entry`     | `tuple[int,int]` | `(0,0)`   | Starting coordinates (row, col)                                                                |
| `exit`      | `tuple[int,int]` | —        | Exit coordinates (row, col)                                                                    |
| `perfect`   | `bool`           | —        | True = unique solution; False = imperfect maze with extra solutions |
| `seed`      | `Optional[int]`  | `None`   | Optional random seed to reproduce the same maze                                                |