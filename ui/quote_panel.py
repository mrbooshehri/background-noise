from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static


class QuotePanel(Vertical):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._quote_text = Static("Loading quote...", classes="quote-text")
        self._quote_author = Static("", classes="quote-author")

    def compose(self) -> ComposeResult:
        yield self._quote_text
        yield self._quote_author

    def set_quote(self, text: str, author: str) -> None:
        self._quote_text.update(f'"{text}"')
        self._quote_author.update(f"— {author}")
