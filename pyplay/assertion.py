from __future__ import annotations

from abc import ABC, abstractmethod

from pyplay.ability import Abilities
from pyplay.action import Action
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.name import Name


class AssertedSuccessfully(ExecutedAction):
    def __str__(self):
        return 'asserted successfully'


class FailedToAssert(ExecutedAction):
    def __init__(self, description: str):
        self._description = description

    def __str__(self):
        return f'failed to {self._description}'


class Assertion:
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> None:
        ...
