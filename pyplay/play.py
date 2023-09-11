from __future__ import annotations

import logging
from contextlib import AsyncExitStack
from typing import Callable, Awaitable, NewType

from pyplay.action import Action
from pyplay.actor import Actor
from pyplay.assertion import Assertion
from pyplay.name import Name
from pyplay.play_notes import PlayNote, PlayNotes


Description = NewType('Description', str)
Part = Awaitable[Description]


class ActorAtPlay:
    def __init__(self, actor: Name, play: Play):
        self._actor = actor
        self._play = play

    def performs(self, *actions: Action) -> ActorAtPlay:
        for action in actions:
            self._play.performs(actor=self._actor, action=action)
        return self

    def asserts(self, *assertions) -> ActorAtPlay:
        for assertion in assertions:
            self._play.asserts(actor=self._actor, assertion=assertion)
        return self


ActorCall = Callable[[Name], ActorAtPlay]


class Play:
    def __init__(self, narrator: Callable[[str], None] | None):
        self._narrator: Callable[[str], None] | None = narrator
        self._actors: dict[Name, Actor] = {}
        self._parts: list[Part] = []
        self._notes: list[PlayNote] = []
        self._exit_stack = AsyncExitStack()

    def actor(self, name: Name) -> ActorAtPlay:
        if name not in self._actors:
            self._actors[name] = Actor(
                name=name,
                exit_stack=self._exit_stack
            )

        return ActorAtPlay(actor=name, play=self)

    async def _perform_action(self, actor_name: Name, action: Action) -> None:
        try:
            await action.execute(
                actor=self._actors[actor_name],
                play_notes=PlayNotes(self._notes)
            )
        finally:
            self._narrator(f'{actor_name} {action}')

    def performs(self, actor: Name, action: Action) -> None:
        self._parts.append(
            self._perform_action(actor_name=actor, action=action)
        )

    async def _perform_assert(self, actor_name: Name, assertion: Assertion) -> None:
        try:
            await assertion.execute(
                actor=self._actors[actor_name],
                play_notes=PlayNotes(self._notes)
            )
        finally:
            self._narrator(f'{actor_name} asserted {assertion}')

    def asserts(self, actor: Name, assertion: Assertion) -> None:
        self._parts.append(
            self._perform_assert(actor_name=actor, assertion=assertion)
        )

    async def execute(self) -> None:
        async with self._exit_stack:
            for part in self._parts:
                await part


def pyplay_log_narrator():
    logger = logging.getLogger('pyplay')
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter(f'[%(asctime)s] [pyplay] %(message)s')
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger.info


def pyplay_spec(narrator):
    def decorator(test_function):
        async def decorated(*args):
            play = Play(narrator=narrator)
            test_function(*args, play.actor)
            await play.execute()

        decorated.__name__ = test_function.__name__

        return decorated

    return decorator
