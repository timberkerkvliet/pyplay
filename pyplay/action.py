from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.name import Name
from pyplay.resource import Resources

T = TypeVar('T', bound=ExecutedAction)


class Action(Generic[T], ABC):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_resources: Resources,
        action_history: ActorActions,
    ) -> T:
        """Executes an action and returns a description of the executed action."""
