from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Callable, Awaitable, NewType, AsyncGenerator

from pyplay.ability import Ability, Abilities
from pyplay.actor import Actor
from pyplay.actor_action import ActorActions
from pyplay.name import Name

Description = NewType('Description', str)
Part = Awaitable[Description]

NewActor = Callable[[Name], Actor]


class Play:
    def __init__(self, narrator: Callable[[str], None] | None):
        self._narrator: Callable[[str], None] | None = narrator
        self._parts: list[Part] = []
        self._actor_actions = ActorActions([])

    def new_actor(
        self,
        named: Name
    ) -> Actor:
        return Actor(
            name=named,
            abilities=Abilities(),
            add_part=self._parts.append,
            actor_actions=self._actor_actions
        )

    async def execute(self) -> None:
        for part in self._parts:
            await part

        for line in self._actor_actions.narration():
            self._narrator(line)


def pyplay_test(test_function):
    async def decorated(*args):
        play = Play(narrator=print)
        test_function(*args, new_actor=play.new_actor)
        await play.execute()

    decorated.__name__ = test_function.__name__

    return decorated
