from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pyplay.actor_action import PlayNotes, Note
from pyplay.name import Name
from pyplay.resource import Resources

T = TypeVar('T', bound=Note)


class Action(ABC):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_resources: Resources,
        play_notes: PlayNotes,
    ) -> list[Note]:
        """Executes an action and returns a description of the executed action."""
