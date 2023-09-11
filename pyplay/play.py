from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Awaitable, Iterator, NewType

from pyplay.action import Action, Assertion
from pyplay.name import Name

Description = NewType('Description', str)
Part = Awaitable[Description]


@dataclass(frozen=True)
class Act:
    character: Name
    action: Action

    def narration(self) -> str:
        if isinstance(self.action, Assertion):
            return f'{self.character} asserted {self.action}'

        return f'{self.character} {self.action}'


class Character:
    def __init__(self, name: Name, play: Play):
        self._name = name
        self._play = play

    def performs(self, *actions: Action) -> Character:
        for action in actions:
            self._play.append_act(
                Act(character=self._name, action=action)
            )
        return self

    def asserts(self, *assertions) -> Character:
        return self.performs(*assertions)


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
