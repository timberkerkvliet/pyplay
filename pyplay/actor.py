from __future__ import annotations

from pyplay.action import Action
from pyplay.name import Name


class Actor:
    def __init__(self, name: Name, add_part) -> None:
        self._name = name
        self._add_part = add_part

    @property
    def name(self) -> Name:
        return self._name

    def who_can(self, ability) -> Actor:
        return self

    def performs(self, *actions: Action) -> Actor:
        for action in actions:
            self._add_part(
                action.execute(actor_name=self._name)
            )
        return self

    def expects(self, *expectations) -> Actor:
        for expectation in expectations:
            self._add_part(
                expectation.verify()
            )
        return self
