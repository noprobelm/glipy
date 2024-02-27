# GliPy

`GliPy` is a [Cellular Automaton](https://en.wikipedia.org/wiki/Cellular_automaton) [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) simulation library written in Python.

## Features
- Run simulations from `.life`, `.rle` pattern files, or from a remote URL that points to a valid `.rle` (widely available on [LifeWiki](https://conwaylife.com/wiki))
- Create simluations from scratch using the classic rules (B3/S23), or define your own birth/survival rules
- Build entirely new cell and state types from custom rulesets defined by you (see the protocols available in the `cell` and `state` modules)
- Use the built-in renderer to visualize simulations in your terminal emulator
- Import `glipy` into your own projects to connect to other front-ends or run your own simulation analysis

## Planned Features

- [ ] Add support for additional algorithm types
  - [ ] HashLife
  - [ ] QuickLife
- [ ] Add a simple GUI application (CLI/TUI support currently available)

## glipy-cli

Quickly render a random simulation by running `glipy-cli` in your terminal.

`glip-cli` has several command line options
| Option                          | Description                                                                                                                         |
|:--------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
| \<target\> [positional; optional] | If no target is passed, render a random simulation. Accepts paths to .rle/.life, or remote URL to rle format                        |
| -r --refresh-rate               | Specify a refresh rate (generations/second)                                                                                         |
| -g --generations                | The number of generations a simulation should run for (default ∞)                                                                   |
| -c --colors                     | Specify colors for dead/alive cells (accepts hex or [ANSI color codes](https://rich.readthedocs.io/en/stable/appendix/colors.html)) |
| -x --debug                      | Enter debug mode. This will turn off terminal rendering and provide performance metrics after the simulation is terminated          |
| -n --no-render                  | Do not render the simulation (debug will automatically trigger this)                                                                |

## Examples

Random Conway Soup: `glipy-cli`
![Random Conway Simulation](random-conway.gif)

Gosper Glider Gun: `glipy-cli https://conwaylife.com/patterns/gosperglidergun.rle`
![Gosper Glider Gun](gosper-gun.gif)

Cloverleaf Interchange hassled by carnival shuttles: `glipy-cli https://conwaylife.com/patterns/p12cloverleafhassler.rle`
![Cloverleaf Hassler](cloverleaf-interchange.gif)

Use custom colors from ANSI/hex codes: `glipy-cli https://conwaylife.com/patterns/387p132pattern.rle --colors "blue black"`
![387p132](p387p132.gif)

## Using glipy in your project

If you want to create new cell/state rules, extend the existing algorithms driving an automaton's evolution, or use your own rendering tools, you might want to use `glipy` in your own project.

## The Cell and CellState Protocol
The `Cell` and `CellState` classes (see the `cell` and `state` modules) inherit from `Protocol` to provide maximum flexbility. In other words, you do not need to inerit from these classes, or even import them to your project at all. Simply write your own cell or cell state classes which implement the methods defined in the respective protocol class. The `MooreCell` and `ConwayState` classes in each module should be observed as examples on how to do this properly.

### The Automaton class

The `Automaton` class is responsible for driving a simluation. It is generic over `Cell` and `CellState`, meaning it will accept any class which implements the methods necessary to be considered `Cell` or `CellState` as described in the previous section (Of course, this is Python, so `Automaton` will technically accept anything, but if you don't want your static type checker to yell at you, you should implement properly).
