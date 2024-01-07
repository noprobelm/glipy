from textual.app import App, ComposeResult, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Static
from . import state, cell, patterns
from .automaton import Automaton

from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree
from textual.binding import Binding
from textual.screen import Screen

import logging
from textual.logging import TextualHandler
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    handlers=[TextualHandler()],
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FilteredDirectoryTree(DirectoryTree):
    BINDINGS = [
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
        Binding("up", "cursor_up", "Cursor Up", show=False),
        Binding("down", "cursor_down", "Cursor Down", show=False),
        Binding("0", "scroll_home", "Scroll Home", show=False),
        Binding("enter", "select_cursor", "Open file/path", show=True),
        Binding("-", "move_up", "Path Up", show=True),
    ]

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name.startswith(".")]

    def on_directory_tree_directory_selected(self, selected):
        self.path = selected.path

    def action_move_up(self):
        self.path = f"{self.path}/../"


class AutomatonRenderer(Static, can_focus=True):
    """A widget to display elapsed time."""

    BINDINGS = [
        Binding("space", "toggle", "Play/Pause", show=True),
        Binding("o", "evolve", "Step"),
    ]

    automaton = Automaton(cell.MooreCell, state.ConwayState())
    generation = reactive(0)
    paused = True

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""

        AutomatonRenderer.automaton = Automaton(
            cell.MooreCell, state.ConwayState(False)
        )
        self.refresh_rate = 10
        self.update_automaton = self.set_interval(
            1 / self.refresh_rate, self.evolve_automaton, pause=self.paused
        )

    def evolve_automaton(self) -> None:
        self.automaton.evolve()
        self.generation = self.automaton.generation

    def action_toggle(self) -> None:
        if self.paused is True:
            self.update_automaton.resume()
        else:
            self.update_automaton.pause()
        self.paused = not self.paused

    def action_evolve(self) -> None:
        if self.paused is False:
            self.action_toggle()
        self.automaton.evolve()
        self.update()

    def action_clear(self) -> None:
        self.automaton.clear()

    def action_spawn(self, pattern) -> None:
        self.automaton.spawn(self.automaton.midpoint - pattern.midpoint, pattern)

    def watch_automaton(self) -> None:
        """Called when the time attribute changes."""
        self.update(self.automaton)

    def render(self):
        return self.automaton


class WorkArea(Screen):
    BINDINGS = [
        Binding("h", "hide_directory_tree", "Toggle Tree"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield FilteredDirectoryTree(os.path.join(Path(__file__).parent, "data/rle/"))
        yield AutomatonRenderer()

        yield Footer()

    def action_toggle_automaton(self):
        automaton = self.query_one(AutomatonRenderer)
        if automaton.paused is False:
            automaton.action_stop()
        elif automaton.paused is True:
            automaton.action_start()

    def action_hide_directory_tree(self) -> None:
        directory_tree = self.query_one(FilteredDirectoryTree)
        directory_tree.visible = not directory_tree.visible

    def action_reduce_refresh_rate(self) -> None:
        automaton = self.query_one(AutomatonRenderer)
        automaton.refresh_rate -= 1

    def on_directory_tree_file_selected(self, selected):
        automaton = self.query_one(AutomatonRenderer)
        automaton.action_clear()
        pattern = patterns.ConwayPattern.from_rle(selected.path)
        automaton.action_spawn(pattern)
        automaton.update()


class AutomatonApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "styles.tcss"
    SCREENS = {"work_area": WorkArea()}

    def on_mount(self) -> None:
        self.push_screen("work_area")
        logging.debug("Logged via TextualHandler")


def main():
    app = AutomatonApp()
    app.run()
