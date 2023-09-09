from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pyplay.name import Name


class ExecutedAction:
    """Describes an action that was executed."""


T = TypeVar('T', bound=ExecutedAction)
Y = TypeVar('Y', bound=ExecutedAction)


@dataclass(frozen=True)
class ActorAction(Generic[T]):
    actor_name: Name
    executed_action: T


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

    def last(self) -> T:
        return self._actor_actions[-1].executed_action

    def one(self) -> T:
        if len(self._actor_actions) != 1:
            raise Exception

        return self.first()

    def add(self, author: Name, action: ExecutedAction) -> None:
        self._actor_actions.append(
            ActorAction(
                actor_name=author,
                executed_action=action
            )
        )
