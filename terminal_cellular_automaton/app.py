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


class FilteredDirectoryTree(DirectoryTree, inherit_bindings=False):
    BINDINGS = [
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
        Binding("up", "cursor_up", "Cursor Up", show=False),
        Binding("down", "cursor_down", "Cursor Down", show=False),
        Binding("0", "scroll_home", "Scroll Home", show=False),
        Binding("enter", "select_cursor", "Open file/path", show=True),
        Binding("-", "path_up", "Path Up", show=True),
    ]

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name.startswith(".")]

    def on_directory_tree_directory_selected(
        self, selected: DirectoryTree.DirectorySelected
    ) -> None:
        self.path = selected.path

    def action_path_up(self) -> None:
        self.path = Path(self.path).parent


class AutomatonRenderer(Static, can_focus=True):
    """A widget to display elapsed time."""

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

    def render(self) -> Automaton:
        return self.automaton


class WorkArea(Screen):
    BINDINGS = [
        Binding("h", "hide_directory_tree", "Toggle Tree"),
        Binding("space", "toggle_automaton", "Play/Pause", show=True, priority=True),
        Binding("o", "evolve_automaton", "Step", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield FilteredDirectoryTree(os.path.join(Path(__file__).parent, "data/rle/"))
        yield AutomatonRenderer()
        yield Footer()

    def action_toggle_automaton(self) -> None:
        automaton = self.query_one(AutomatonRenderer)
        automaton.action_toggle()

    def action_evolve_automaton(self) -> None:
        automaton = self.query_one(AutomatonRenderer)
        automaton.action_evolve()

    def action_hide_directory_tree(self) -> None:
        directory_tree = self.query_one(FilteredDirectoryTree)
        directory_tree.visible = not directory_tree.visible

    def on_directory_tree_file_selected(
        self, selected: DirectoryTree.FileSelected
    ) -> None:
        try:
            match selected.path.suffix:
                case ".rle":
                    pattern = patterns.ConwayPattern.from_rle(selected.path)
                case ".life":
                    pattern = patterns.ConwayPattern.from_life(selected.path)
                case _:
                    return
        except ValueError:
            return

        automaton = self.query_one(AutomatonRenderer)
        automaton.action_clear()
        automaton.action_spawn(pattern)
        automaton.update()


class AutomatonApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "styles.tcss"
    SCREENS = {"work_area": WorkArea()}

    def on_mount(self) -> None:
        self.push_screen("work_area")
        logging.debug("Logged via TextualHandler")


def main() -> None:
    app = AutomatonApp()
    app.run()
