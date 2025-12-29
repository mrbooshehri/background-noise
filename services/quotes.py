from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Quote:
    text: str
    author: str


class QuoteService:
    def __init__(self) -> None:
        self._last_quote = Quote("Stay focused and keep going.", "Unknown")

    def fetch(self, timeout: float = 5.0) -> Quote:
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=timeout)
            response.raise_for_status()
            payload = response.json()
            if not payload:
                return self._last_quote
            entry = payload[0]
            text = entry.get("q")
            author = entry.get("a")
            if not text or not author:
                return self._last_quote
            self._last_quote = Quote(text, author)
        except (requests.RequestException, ValueError, KeyError):
            return self._last_quote
        return self._last_quote

    @property
    def last_quote(self) -> Quote:
        return self._last_quote
