from textual.app import App, ComposeResult, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Static
from . import state, cell, automaton
from . import patterns


from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree


class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name.startswith(".")]

    def on_directory_tree_file_selected(self):
        pass


import logging
from textual.logging import TextualHandler

logging.basicConfig(
    level=logging.INFO,
    handlers=[TextualHandler()],
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Automaton(Static):
    """A widget to display elapsed time."""

    auto = automaton.Automaton(cell.MooreCell, state.ConwayState(False))
    pulsar = patterns.Pulsar()
    sparker = patterns.ConwayPattern.from_rle(
        "/home/noprobelm/workshop/released/tca/terminal_cellular_automaton/data/rle/p11dominosparkeron56p27.rle"
    )
    auto.spawn(auto.midpoint - sparker.midpoint, sparker)
    generation = reactive(auto.generation)
    started = False

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_automaton = self.set_interval(
            1 / 10, self.evolve_automaton, pause=True
        )

    def evolve_automaton(self):
        self.auto.evolve()
        self.generation = self.auto.generation

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.started = True
        self.update_automaton.resume()

    def stop(self):
        """Method to stop the time display updating."""
        self.started = False
        self.update_automaton.pause()

    def evolve(self):
        self.auto.evolve()
        self.update()

    def watch_automaton(self) -> None:
        """Called when the time attribute changes."""
        self.update(self.auto)

    def render(self):
        return self.auto


class AutomatonApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("h", "hide_directory_tree", "Hide Directory Tree"),
        ("p", "toggle_automaton", "Toggle"),
        ("o", "evolve", "Step"),
    ]

    def on_mount(self) -> None:
        logging.debug("Logged via TextualHandler")

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Footer()
        yield FilteredDirectoryTree("./", classes="box1")
        yield Automaton(classes="box2")

    def action_toggle_automaton(self):
        automaton = self.query_one(Automaton)
        if automaton.started is True:
            automaton.stop()
        elif automaton.started is False:
            automaton.start()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_hide_directory_tree(self) -> None:
        directory_tree = self.query_one(FilteredDirectoryTree)
        directory_tree.visible = not directory_tree.visible

    def action_evolve(self) -> None:
        automaton = self.query_one(Automaton)
        if automaton.started is False:
            automaton.evolve()


def main():
    app = AutomatonApp()
    app.run()
