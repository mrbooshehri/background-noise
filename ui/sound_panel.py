from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static


@dataclass
class SoundState:
    key: str
    name: str
    volume: float
    playing: bool
    available: bool


class SoundPanel(Vertical):
    def __init__(
        self,
        sounds: List[SoundState],
        layout: Iterable[Iterable[str]],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._sounds = sounds
        self._layout = [list(group) for group in layout]
        self._labels: List[Static] = []
        self._selected_index = 0
        self._index_by_key = {state.key: idx for idx, state in enumerate(sounds)}

    def compose(self) -> ComposeResult:
        yield Static("Ambient Noise Mixer", classes="panel-title")
        for _ in self._layout:
            label = Static("", classes="sound-row")
            self._labels.append(label)
            yield label

    def on_mount(self) -> None:
        self._refresh_rows()

    def selected_index(self) -> int:
        return self._selected_index

    def move_selection(self, delta: int) -> None:
        if not self._sounds:
            return
        self._selected_index = (self._selected_index + delta) % len(self._sounds)
        self._refresh_rows()

    def update_row(self, index: int) -> None:
        if 0 <= index < len(self._sounds):
            self._refresh_rows()

    @staticmethod
    def _volume_bar(volume: float, width: int = 16) -> str:
        filled = int(round(volume * width))
        filled = max(0, min(width, filled))
        return "█" * filled + "░" * (width - filled)

    def _format_entry(self, state: SoundState, selected: bool) -> Text:
        percent = int(round(state.volume * 100))
        bar = self._volume_bar(state.volume)
        indicator = ">" if selected else " "
        label = f"{indicator} {state.name:<9} [{bar}] {percent:2d}%"
        text = Text(label.ljust(36))
        if state.playing:
            text.stylize("bold #4aa3df")
        elif not state.available:
            text.stylize("dim")
        return text

    def _refresh_rows(self) -> None:
        for label, group in zip(self._labels, self._layout, strict=False):
            entries: List[Text] = []
            for key in group:
                index = self._index_by_key.get(key)
                if index is None:
                    continue
                entries.append(
                    self._format_entry(
                        self._sounds[index],
                        index == self._selected_index,
                    )
                )
            if entries:
                row = Text("   ").join(entries)
            else:
                row = Text("")
            label.update(row)
