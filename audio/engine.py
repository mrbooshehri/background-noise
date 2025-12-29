from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


@dataclass
class SoundSpec:
    key: str
    name: str
    file_path: Path
    channel: int
    volume: float = 0.5


class AudioEngine:
    def __init__(self, specs: Iterable[SoundSpec]) -> None:
        self.specs = list(specs)
        self._initialized = False
        self._available = True
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._channels: Dict[str, pygame.mixer.Channel] = {}
        self._missing: set[str] = set()

    @property
    def available(self) -> bool:
        return self._available

    @property
    def missing(self) -> set[str]:
        return set(self._missing)

    def init(self) -> None:
        if self._initialized:
            return
        try:
            pygame.mixer.init()
        except pygame.error:
            self._available = False
            return
        for spec in self.specs:
            if not spec.file_path.exists():
                self._missing.add(spec.key)
                continue
            try:
                self._sounds[spec.key] = pygame.mixer.Sound(spec.file_path.as_posix())
            except pygame.error:
                self._missing.add(spec.key)
                continue
            self._channels[spec.key] = pygame.mixer.Channel(spec.channel)
            self._channels[spec.key].set_volume(spec.volume)
        self._initialized = True

    def start(self, key: str) -> None:
        if not self._available or key in self._missing:
            return
        self.init()
        sound = self._sounds.get(key)
        channel = self._channels.get(key)
        if sound is None or channel is None:
            return
        channel.play(sound, loops=-1)

    def stop(self, key: str) -> None:
        if not self._available or key in self._missing:
            return
        channel = self._channels.get(key)
        if channel is None:
            return
        channel.stop()

    def set_volume(self, key: str, volume: float) -> None:
        if not self._available or key in self._missing:
            return
        channel = self._channels.get(key)
        if channel is None:
            return
        channel.set_volume(volume)

    def shutdown(self) -> None:
        if not self._initialized:
            return
        pygame.mixer.quit()
        self._initialized = False
