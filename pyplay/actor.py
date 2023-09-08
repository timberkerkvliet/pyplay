from typing import Self, NewType, Callable

from pyplay.action import Action
from pyplay.play import Part

ActorName = NewType('ActorName', str)


class Actor:
    def __init__(self, name: ActorName, add_part: Callable[[Part], None]) -> None:
        self._name = name
        self._add_part = add_part

    @property
    def name(self) -> ActorName:
        return self._name

    def who_can(self, ability) -> Self:
        return self

    def performs(self, *actions: Action) -> Self:
        for action in actions:
            self._add_part(
                action.execute()
            )
        return self

    def expects(self, *expectations) -> Self:
        return self
