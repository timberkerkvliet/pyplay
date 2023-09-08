from __future__ import annotations

from typing import NewType, Callable

from pyplay.action import Action

ActorName = NewType('ActorName', str)


class Actor:
    def __init__(self, name: ActorName, add_part) -> None:
        self._name = name
        self._add_part = add_part

    @property
    def name(self) -> ActorName:
        return self._name

    def who_can(self, ability) -> Actor:
        return self

    def performs(self, *actions: Action) -> Actor:
        for action in actions:
            self._add_part(
                action.execute()
            )
        return self

    def expects(self, *expectations) -> Actor:
        return self
