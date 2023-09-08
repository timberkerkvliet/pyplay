from typing import Self, NewType

ActorName = NewType('ActorName', str)


class Actor:
    def __init__(self, name: ActorName) -> None:
        self._name = name

    @property
    def name(self) -> ActorName:
        return self._name

    def who_can(self, ability) -> Self:
        return self

    def perform(self, *actions) -> None:
        ...

    def expect(self, *expectations) -> None:
        ...
