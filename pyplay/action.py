from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pyplay.name import Name
from pyplay.play_notes import PlayNotes
from pyplay.resource import Resources


class Action(ABC):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_resources: Resources,
        play_notes: PlayNotes,
    ) -> None:
        """Executes an action and returns a description of the executed action."""
