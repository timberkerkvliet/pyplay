from __future__ import annotations

from abc import ABC, abstractmethod

from pyplay.ability import Abilities
from pyplay.action import Action
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.name import Name


class AssertionSuccessful(ExecutedAction):
    def __init__(self, description: str = 'asserted successfully'):
        self._description = description

    def __str__(self):
        return self._description


class AssertionFailed(ExecutedAction):
    def __init__(self, description: str = 'asserted unsuccessfully'):
        self._description = description

    def __str__(self):
        return self._description


class Assertion(Action):
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> None:
        ...
