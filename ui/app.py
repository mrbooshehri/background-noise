from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer

from audio.engine import AudioEngine, SoundSpec
from services.quotes import QuoteService
from ui.quote_panel import QuotePanel
from ui.sound_panel import SoundPanel, SoundState


@dataclass
class SoundConfig:
    key: str
    name: str
    filename: str


SOUND_CONFIGS = [
    SoundConfig("sea", "Sea", "sea.ogg"),
    SoundConfig("fire", "Fire", "fire.ogg"),
    SoundConfig("gull", "Sea Gull", "gull.ogg"),
    SoundConfig("rain", "Rain", "rain.ogg"),
    SoundConfig("lightning", "Lightning", "lightning.ogg"),
    SoundConfig("cafe", "Busy Cafe", "cafe.ogg"),
]

SOUND_LAYOUT = [
    ["sea", "gull", "lightning"],
    [],
    ["fire", "rain", "cafe"],
]


class AmbientNoiseApp(App):
    CSS = """
    Screen {
        background: #0f1a18;
        color: #f4f1de;
    }

    Vertical {
        height: 100%;
    }

    .quote-panel {
        border: tall #445566;
        padding: 1 2;
        height: 1fr;
        content-align: center middle;
        align: center middle;
    }

    .sound-panel {
        border: tall #2f4f4f;
        padding: 1 2;
        height: 9;
    }

    .panel-title {
        text-style: bold;
        color: #f2cc8f;
        margin-bottom: 1;
    }

    .sound-row {
        height: 1;
        width: 100%;
        text-align: center;
    }

    .quote-text {
        text-style: italic;
        margin-bottom: 1;
        text-align: center;
        width: 100%;
    }

    .quote-author {
        color: #d4a373;
        text-align: center;
        width: 100%;
    }
    """

    BINDINGS = [
        ("up", "select_previous", "Previous sound"),
        ("down", "select_next", "Next sound"),
        ("left", "volume_down", "Volume down"),
        ("right", "volume_up", "Volume up"),
        ("space", "toggle", "Toggle sound"),
        ("r", "refresh_quote", "Refresh quote"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        root = Path(__file__).resolve().parents[1]
        sound_dir = root / "audio" / "sounds"

        self._sound_states = []
        specs = []
        for index, config in enumerate(SOUND_CONFIGS):
            file_path = sound_dir / config.filename
            available = file_path.exists()
            self._sound_states.append(
                SoundState(
                    key=config.key,
                    name=config.name,
                    volume=0.5,
                    playing=False,
                    available=available,
                )
            )
            specs.append(
                SoundSpec(
                    key=config.key,
                    name=config.name,
                    file_path=file_path,
                    channel=index,
                    volume=0.5,
                )
            )

        self._audio_engine = AudioEngine(specs)
        self._quote_service = QuoteService()
        self._sound_panel = SoundPanel(
            self._sound_states, SOUND_LAYOUT, classes="sound-panel"
        )
        self._quote_panel = QuotePanel(classes="quote-panel")

    def compose(self) -> ComposeResult:
        yield Vertical(self._quote_panel, self._sound_panel)
        yield Footer()

    async def on_mount(self) -> None:
        self._audio_engine.init()
        missing = self._audio_engine.missing
        if missing:
            for index, state in enumerate(self._sound_states):
                if state.key in missing:
                    state.available = False
                    self._sound_panel.update_row(index)
        await self._refresh_quote()

    def on_shutdown(self) -> None:
        self._audio_engine.shutdown()

    def _selected_state(self) -> tuple[int, SoundState] | None:
        index = self._sound_panel.selected_index()
        if index is None:
            return None
        return index, self._sound_states[index]

    def _adjust_volume(self, delta: float) -> None:
        selected = self._selected_state()
        if not selected:
            return
        index, state = selected
        new_volume = max(0.0, min(1.0, state.volume + delta))
        if new_volume == state.volume:
            return
        state.volume = new_volume
        self._audio_engine.set_volume(state.key, new_volume)
        self._sound_panel.update_row(index)

    def action_volume_down(self) -> None:
        self._adjust_volume(-0.05)

    def action_volume_up(self) -> None:
        self._adjust_volume(0.05)

    def action_select_previous(self) -> None:
        self._sound_panel.move_selection(-1)

    def action_select_next(self) -> None:
        self._sound_panel.move_selection(1)

    def action_toggle(self) -> None:
        selected = self._selected_state()
        if not selected:
            return
        index, state = selected
        if not state.available:
            return
        state.playing = not state.playing
        if state.playing:
            self._audio_engine.start(state.key)
        else:
            self._audio_engine.stop(state.key)
        self._sound_panel.update_row(index)

    async def action_refresh_quote(self) -> None:
        await self._refresh_quote()

    async def _refresh_quote(self) -> None:
        self._quote_panel.set_quote("Loading...", "")
        quote = await asyncio.to_thread(self._quote_service.fetch)
        self._quote_panel.set_quote(quote.text, quote.author)
