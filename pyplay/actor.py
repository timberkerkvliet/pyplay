from __future__ import annotations

from pyplay.ability import Abilities, Ability
from pyplay.action import Action
from pyplay.actor_action import ActorActions
from pyplay.assertion import Assertion, AssertionFailed
from pyplay.name import Name


class Actor:
    def __init__(
        self,
        name: Name,
        abilities: Abilities,
        add_part,
        actor_actions
    ) -> None:
        self._name = name
        self._abilities = abilities
        self._add_part = add_part
        self._action_history = actor_actions

    @property
    def name(self) -> Name:
        return self._name

    def who_can(self, *abilities: Ability) -> None:
        for ability in abilities:
            self._abilities.add(ability)

    async def _perform_action(self, action: Action) -> None:
        executed_action = await action.execute(
            actor_name=self._name,
            actor_abilities=self._abilities,
            action_history=self._action_history
        )
        self._action_history.add(author=self._name, action=executed_action)

    async def _perform_assertion(self, assertion: Assertion) -> None:
        executed_action = await assertion.execute(
            actor_name=self._name,
            actor_abilities=self._abilities,
            action_history=self._action_history
        )
        self._action_history.add(author=self._name, action=executed_action)
        if isinstance(executed_action, AssertionFailed):
            raise AssertionError(str(executed_action))

    def performs(self, *actions: Action) -> Actor:
        for action in actions:
            self._add_part(self._perform_action(action))
        return self

    def asserts(self, *assertions) -> Actor:
        for assertion in assertions:
            self._add_part(self._perform_assertion(assertion))
        return self
