from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Type

from pyplay.ability import Abilities
from pyplay.name import Name


class ExecutedAction:
    """Describes an action that was executed."""


T = TypeVar('T')


@dataclass(frozen=True)
class ActorAction(Generic[T]):
    actor_name: Name
    executed_action: T


Y = TypeVar('Y')


class ActorActions(Generic[T]):
    def __init__(self, actor_actions: list[ActorAction[T]]):
        self._actor_actions = actor_actions

    def by_action_type(self, action_type: Type[Y]) -> ActorActions[Y]:
        return ActorActions(
            [
                actor_action for actor_action in self._actor_actions
                if isinstance(actor_action.executed_action, action_type)
            ]
        )

    def by_actor(self, actor_name: Name) -> ActorActions[T]:
        return ActorActions(
            [
                actor_action for actor_action in self._actor_actions
                if actor_action.actor_name == actor_name
            ]
        )

    def first(self) -> T:
        return self._actor_actions[0].executed_action


class Action(ABC):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions,
    ) -> ExecutedAction:
        """Executes an action and returns a description of the executed action."""
