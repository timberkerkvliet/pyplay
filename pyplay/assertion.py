from __future__ import annotations

from abc import ABC, abstractmethod

from pyplay.action import Action
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.name import Name
from pyplay.resource import Resources


class Asserted(ExecutedAction):
    def __init__(self, description: str):
        self._description = description

    def __str__(self):
        return f'asserted {self._description}'


class FailedToAssert(ExecutedAction):
    def __init__(self, description: str):
        self._description = description

    def __str__(self):
        return f'failed to assert {self._description}'


class Assertion:
    @abstractmethod
    async def execute(
        self,
        actor_name: Name,
        actor_resources: Resources,
        action_history: ActorActions
    ) -> None:
        ...
