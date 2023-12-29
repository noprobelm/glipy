Simulate cellular automaton directly to the terminal

## Usage

usage: `tca [-h] [-r REFRESH_RATE] [-d DURATION] [-x] [-n] [--scenario SCENARIO | --rle RLE | --url URL]`

| Option           | Default Value                                                 |
|------------------|---------------------------------------------------------------|
| `--refresh-rate` | `60`                                                          |
| `--duration`     | `0` (infinitely run the simulation)                           |
| `--debug`        | `False` (Disabled rendering and captures performance metrics) |
| `--no-render`    | `False`                                                       |
| `--scenario`     | Runs a specified scenario from the `scenarios` module         |
| `--rle`          | Runs a specified `.rle` from a local path                     |
| `--url`          | Runs a specified `.rle` a remote URL                          |

## Available scenarios
- `conway_1`: A simple game of life simulation where each cell has an equal chance to 'spawn' as 'alive' 'dead'
- `conway_2`: Each cell has a 10% chance of spawning as alive

## Creating your own game
- Select a `Cell` type from the `cell` module (or make your own; it must adhere to the `Cell` protocol)
- Select a `CellState` type from the `states` module (or make your own; it should derive itself from the `CellState` class)
- Create a new scenario in the `scenarios` module following the existing boilerplate code
- Run the sim!

## Examples
### Conway's Game of Life
![Conway's Game of Life](conway.gif)
