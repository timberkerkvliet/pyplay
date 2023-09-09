from __future__ import annotations

from abc import ABC, abstractmethod

from pyplay.ability import Abilities
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.name import Name


class Action(ABC):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions,
    ) -> ExecutedAction:
        """Executes an action and returns a description of the executed action."""
