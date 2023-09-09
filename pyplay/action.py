from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pyplay.ability import Abilities
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.name import Name


T = TypeVar('T', bound=ExecutedAction)


class Action(Generic[T], ABC):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions,
    ) -> T:
        """Executes an action and returns a description of the executed action."""
