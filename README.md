# GLiPy

`GLiPy` is a [Cellular Automaton](https://en.wikipedia.org/wiki/Cellular_automaton) [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) simulation library written in Python.
	
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

## Using glipy in your project

If you want to create new cell/state rules, extend the existing algorithms driving an automaton's evolution, or use your own rendering tools, you might want to use `glipy` in your own project.

### The Cell and CellState Protocol
The `Cell` and `CellState` classes (see the `cell` and `state` modules) inherit from `Protocol` to provide maximum flexbility. In other words, you do not need to inerit from these classes, or even import them to your project at all. Simply write your own cell or cell state classes which implement the methods defined in the respective protocol class. The `MooreCell` and `ConwayState` classes in each module should be observed as examples on how to do this properly.

### The Automaton class

The `Automaton` class is responsible for driving a simluation. It is generic over `Cell` and `CellState`, meaning it will accept any class which implements the methods necessary to be considered `Cell` or `CellState` as described in the previous section (Of course, this is Python, so `Automaton` will technically accept anything, but if you don't want your static type checker to yell at you, you should implement properly).
## See also

I've implemented some rendering capabilities in a separate project, [glipy-cli](https://github.com/noprobelm/glipy-cli). `glipy-cli` will render Conway's Game of Life simulations in your terminal emulator.
