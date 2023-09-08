from __future__ import annotations

from typing import Callable, Self, Awaitable, NewType

from pyplay.actor import Actor, ActorName

Description = NewType('Description', str)
Part = Awaitable[Description]


class Play:
    def __init__(self, narrator: Callable[[str], None] | None):
        self._narrator: Callable[[str], None] | None = narrator
        self._parts: list[Part] = []

    def with_actor(self, actor_name: ActorName) -> Actor:
        return Actor(
            name=actor_name,
            add_part=self._parts.append
        )

    async def perform(self) -> None:
        for part in self._parts:
            narration = await part
            self._narrator(narration)
