from __future__ import annotations

from typing import Callable, Iterator

from pyplay.act import Act
from pyplay.character import Character
from pyplay.name import Name


CharacterCall = Callable[[Name], Character]


class Play:
    def __init__(self):
        self._acts: list[Act] = []

    def append_act(self, act: Act) -> None:
        self._acts.append(act)

    def character(self, name: Name) -> Character:
        return Character(name=name, play=self)

    def __iter__(self) -> Iterator[Act]:
        return iter(self._acts)
