from __future__ import annotations

from pyplay.ability import Abilities, Ability
from pyplay.action import Action
from pyplay.name import Name


class Actor:
    def __init__(
        self,
        name: Name,
        abilities: Abilities,
        add_part
    ) -> None:
        self._name = name
        self._abilities = abilities
        self._add_part = add_part

    @property
    def name(self) -> Name:
        return self._name

    def who_can(self, *abilities: Ability) -> None:
        for ability in abilities:
            self._abilities.add(ability)

    def performs(self, *actions: Action) -> Actor:
        for action in actions:
            self._add_part(
                action.execute(
                    actor_name=self._name,
                    actor_abilities=self._abilities,
                    action_history=None
                )
            )
        return self

    def expects(self, *expectations) -> Actor:
        for expectation in expectations:
            self._add_part(
                expectation.verify(
                    actor_name=self._name,
                    actor_abilities=self._abilities,
                    action_history=None
                )
            )
        return self
