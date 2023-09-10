from __future__ import annotations

from abc import ABC, abstractmethod

from pyplay.actor import Actor
from pyplay.play_notes import PlayNotes


class Action(ABC):
    @abstractmethod
    async def execute(
        self,
        actor: Actor,
        play_notes: PlayNotes,
    ) -> None:
        """Executes an action and returns a description of the executed action."""

    def __str__(self):
        return self.__class__.__name__
