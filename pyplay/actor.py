from __future__ import annotations

from pyplay.action import Action
from pyplay.assertion import Assertion, FailedToAssert, Asserted
from pyplay.name import Name
from pyplay.resource import Resources


class Actor:
    def __init__(
        self,
        name: Name,
        resources: Resources,
        add_part,
        actor_actions
    ) -> None:
        self._name = name
        self._resources = resources
        self._add_part = add_part
        self._action_history = actor_actions

    @property
    def name(self) -> Name:
        return self._name

    async def _perform_action(self, action: Action) -> None:
        executed_action = await action.execute(
            actor_name=self._name,
            actor_resources=self._resources,
            action_history=self._action_history
        )
        self._action_history.add(author=self._name, action=executed_action)

    async def _assert(self, assertion: Assertion) -> None:
        try:
            await assertion.execute(
                actor_name=self._name,
                actor_resources=self._resources,
                action_history=self._action_history
            )
        except AssertionError as e:
            self._action_history.add(author=self._name, action=FailedToAssert(str(assertion)))
            raise
        else:
            self._action_history.add(author=self._name, action=Asserted(str(assertion)))

    def performs(self, *actions: Action) -> Actor:
        for action in actions:
            self._add_part(self._perform_action(action))
        return self

    def asserts(self, *assertions) -> Actor:
        for assertion in assertions:
            self._add_part(self._assert(assertion))
        return self
