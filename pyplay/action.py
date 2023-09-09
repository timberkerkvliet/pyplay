from abc import ABC, abstractmethod
from dataclasses import dataclass

from pyplay.ability import Abilities
from pyplay.name import Name


class ExecutedAction:
    """Describes an action that was executed."""


@dataclass(frozen=True)
class ActorAction:
    actor_name: Name
    executed_action: ExecutedAction


class ActorActions:
    def __init__(self, actor_actions: list[ActorAction]):
        self._actor_actions = actor_actions


class Action(ABC):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions,
    ) -> ExecutedAction:
        """Executes an action and returns a description of the executed action."""
