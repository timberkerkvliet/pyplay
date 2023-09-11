from __future__ import annotations

from abc import abstractmethod

from pyplay.actor import Actor
from pyplay.notes import Note
from pyplay.stage import Stage


class Asserted(Note):
    def __init__(self, description: str):
        self._description = description

    def __str__(self):
        return f'asserted {self._description}'


class FailedToAssert(Note):
    def __init__(self, description: str):
        self._description = description

    def __str__(self):
        return f'failed to assert {self._description}'


class Assertion:
    @abstractmethod
    async def execute(self, actor: Actor, stage: Stage) -> None:
        ...

    def __str__(self):
        return self.__class__.__name__
